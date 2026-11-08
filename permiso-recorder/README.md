# PERMISO Recorder v1.4.0

## Native loading popup
A centered progress spinner and message appear for initial loading, in-app full-page navigation, refresh, WebView back navigation, and saved-credential auto-login. Auto-login shows **Signing in…** while form submission is processed by the existing PERMISO website. Navigation shows **Loading page…**. The popup is automatically dismissed when navigation completes, on connection errors, if automatic login cannot find a form, or after a 14-second safety timeout. It never alters backend authentication, QR recording, records, or DTR.

## Preserved v1.3 behavior
Full-height website interface with draggable floating Settings button, pull-to-refresh (disabled while QR camera access is active), website session handling, AES-GCM encrypted saved credentials, and unchanged permissions/download handling.

## Test checklist
On Android phone test: open app with/without auto-login; navigate between Scanner, Records, DTR; reload and back; QR scanner camera with a live QR code; network interruption; invalid saved credentials; clear credentials. Website implementations that switch tabs entirely within a single document without browser navigation will not trigger native page load callbacks.

## Installation
GitHub Actions builds a debug APK (Android 8.0+). Because hosted builds may have different debug signing certificates, an update can require uninstalling the previous app, which clears locally encrypted saved credentials. Existing server records are unaffected.
