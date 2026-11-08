package ph.com.smnhs.permiso.recorder;

import android.content.Context;
import android.content.SharedPreferences;
import android.security.keystore.KeyGenParameterSpec;
import android.security.keystore.KeyProperties;
import android.util.Base64;
import java.nio.charset.StandardCharsets;
import java.security.KeyStore;
import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.GCMParameterSpec;
import org.json.JSONObject;

/**
 * User credentials are kept only on this Android device.
 * AES-GCM key material is non-exportable and managed by Android Keystore.
 * No login details are compiled into the APK, stored in GitHub or logged.
 */
final class CredentialVault {
    private static final String PREFS = "recorder_local_settings";
    private static final String RECORD = "encrypted_credentials";
    private static final String KEY_ALIAS = "permiso_recorder_credentials_v1";
    private static final String KEYSTORE = "AndroidKeyStore";

    static final class SavedLogin {
        final String username;
        final String password;
        final boolean autoLogin;
        SavedLogin(String username, String password, boolean autoLogin) {
            this.username = username;
            this.password = password;
            this.autoLogin = autoLogin;
        }
    }

    private CredentialVault() {}

    private static SharedPreferences preferences(Context context) {
        return context.getSharedPreferences(PREFS, Context.MODE_PRIVATE);
    }

    private static SecretKey secretKey() throws Exception {
        KeyStore store = KeyStore.getInstance(KEYSTORE);
        store.load(null);
        if (store.containsAlias(KEY_ALIAS)) {
            return (SecretKey) store.getKey(KEY_ALIAS, null);
        }
        KeyGenerator generator = KeyGenerator.getInstance(KeyProperties.KEY_ALGORITHM_AES, KEYSTORE);
        KeyGenParameterSpec spec = new KeyGenParameterSpec.Builder(
                KEY_ALIAS, KeyProperties.PURPOSE_ENCRYPT | KeyProperties.PURPOSE_DECRYPT)
                .setBlockModes(KeyProperties.BLOCK_MODE_GCM)
                .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
                .setKeySize(256)
                .build();
        generator.init(spec);
        return generator.generateKey();
    }

    static void save(Context context, String username, String password, boolean autoLogin)
            throws Exception {
        JSONObject object = new JSONObject();
        object.put("username", username);
        object.put("password", password);
        object.put("autoLogin", autoLogin);
        Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
        cipher.init(Cipher.ENCRYPT_MODE, secretKey());
        byte[] iv = cipher.getIV();
        byte[] ciphertext = cipher.doFinal(object.toString().getBytes(StandardCharsets.UTF_8));
        byte[] combined = new byte[iv.length + ciphertext.length];
        System.arraycopy(iv, 0, combined, 0, iv.length);
        System.arraycopy(ciphertext, 0, combined, iv.length, ciphertext.length);
        if (!preferences(context).edit().putString(RECORD,
                Base64.encodeToString(combined, Base64.NO_WRAP)).commit()) {
            throw new IllegalStateException("Unable to persist protected login");
        }
    }

    static SavedLogin load(Context context) {
        String saved = preferences(context).getString(RECORD, null);
        if (saved == null) return null;
        try {
            byte[] combined = Base64.decode(saved, Base64.DEFAULT);
            if (combined.length <= 28) throw new IllegalStateException("Invalid encrypted data");
            byte[] iv = new byte[12];
            byte[] ciphertext = new byte[combined.length - 12];
            System.arraycopy(combined, 0, iv, 0, 12);
            System.arraycopy(combined, 12, ciphertext, 0, ciphertext.length);
            Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
            cipher.init(Cipher.DECRYPT_MODE, secretKey(), new GCMParameterSpec(128, iv));
            JSONObject object = new JSONObject(new String(
                    cipher.doFinal(ciphertext), StandardCharsets.UTF_8));
            return new SavedLogin(
                    object.getString("username"),
                    object.getString("password"),
                    object.optBoolean("autoLogin", false));
        } catch (Exception e) {
            // Device restore or invalidated Keystore key: never use undecipherable credentials.
            clear(context);
            return null;
        }
    }

    static void clear(Context context) {
        preferences(context).edit().remove(RECORD).commit();
    }
}
