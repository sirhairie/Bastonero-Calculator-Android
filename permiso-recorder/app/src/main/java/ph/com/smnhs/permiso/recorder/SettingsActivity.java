package ph.com.smnhs.permiso.recorder;

import android.app.Activity;
import android.app.AlertDialog;
import android.graphics.Color;
import android.os.Bundle;
import android.text.InputType;
import android.text.method.HideReturnsTransformationMethod;
import android.text.method.PasswordTransformationMethod;
import android.view.View;
import android.view.Window;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

public final class SettingsActivity extends Activity {
    private EditText usernameInput;
    private EditText passwordInput;
    private CheckBox autoLoginInput;
    private CheckBox showPasswordInput;
    private TextView statusText;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        getWindow().setStatusBarColor(getColor(R.color.navy_dark));
        getWindow().getDecorView().setSystemUiVisibility(0);
        getWindow().setNavigationBarColor(getColor(R.color.navy_dark));
        setContentView(R.layout.activity_settings);

        usernameInput = findViewById(R.id.savedUsername);
        passwordInput = findViewById(R.id.savedPassword);
        autoLoginInput = findViewById(R.id.autoLoginToggle);
        showPasswordInput = findViewById(R.id.showPasswordToggle);
        statusText = findViewById(R.id.credentialStatus);

        findViewById(R.id.backButton).setOnClickListener(view -> finish());
        Button save = findViewById(R.id.saveCredentials);
        Button clear = findViewById(R.id.clearCredentials);
        save.setOnClickListener(view -> saveCredentials());
        clear.setOnClickListener(view -> confirmClear());

        showPasswordInput.setOnCheckedChangeListener((button, checked) -> {
            int selection = passwordInput.getSelectionStart();
            passwordInput.setTransformationMethod(checked
                    ? HideReturnsTransformationMethod.getInstance()
                    : PasswordTransformationMethod.getInstance());
            passwordInput.setSelection(Math.max(0,
                    Math.min(selection, passwordInput.length())));
        });
        CredentialVault.SavedLogin saved = CredentialVault.load(this);
        if (saved != null) {
            usernameInput.setText(saved.username);
            passwordInput.setText(saved.password);
            autoLoginInput.setChecked(saved.autoLogin);
            statusText.setText("Saved login is encrypted on this device.");
        } else {
            autoLoginInput.setChecked(true);
            statusText.setText("No saved login. Enter your Recorder account to begin.");
        }
    }

    private void saveCredentials() {
        String username = usernameInput.getText().toString().trim();
        String password = passwordInput.getText().toString();
        if (username.isEmpty()) {
            usernameInput.setError("Enter your Recorder username");
            usernameInput.requestFocus();
            return;
        }
        if (password.isEmpty()) {
            passwordInput.setError("Enter your Recorder password");
            passwordInput.requestFocus();
            return;
        }
        try {
            CredentialVault.save(this, username, password, autoLoginInput.isChecked());
            setResult(RESULT_OK);
            Toast.makeText(this, "Recorder settings saved", Toast.LENGTH_SHORT).show();
            finish();
        } catch (Exception e) {
            new AlertDialog.Builder(this)
                    .setTitle("Could not save credentials")
                    .setMessage("Secure device storage is unavailable. No new credentials were saved.")
                    .setPositiveButton("OK", null)
                    .show();
        }
    }

    private void confirmClear() {
        new AlertDialog.Builder(this)
                .setTitle("Clear saved login?")
                .setMessage("This removes the stored username and password and disables automatic login. It does not log out of the current website session.")
                .setNegativeButton("Cancel", null)
                .setPositiveButton("Clear login", (dialog, which) -> {
                    CredentialVault.clear(this);
                    usernameInput.setText("");
                    passwordInput.setText("");
                    autoLoginInput.setChecked(false);
                    showPasswordInput.setChecked(false);
                    statusText.setText("No saved login on this device.");
                    setResult(RESULT_OK);
                    Toast.makeText(this, "Saved login cleared", Toast.LENGTH_SHORT).show();
                })
                .show();
    }
}
