# PERMISO Recorder v1.5.1

## Updated navy-and-gold loading design

- Native loading popup: diagonal navy gradient from #082544 to #123E6B, rounded corners, subtle gold border, white heading, soft pale-gold subtext, gold spinner.
- Web-page navigation spinner: matching gradient card, white heading, pale-gold subtext, gold spinner.
- Loading text is now **Loading...** everywhere navigation progress is displayed. **Signing in…** and **Signing out…** remain descriptive and unchanged.
- Native horizontal loading indicator and pull-to-refresh progress also use the same golden color.
- Layout, immediate navigation feedback, login behavior, scanner camera handling, QR recording, DTR, file downloads, encrypted credentials and floating Settings are retained without backend changes.

## Build and installation

GitHub Actions builds a debug-signed APK for Android 8.0+. If a new debug signing key prevents an in-place update, uninstall the old app and install this build, then re-enter locally stored credentials. Existing PERMISO server-side records are not affected.

Device-testing required: startup auto-login popup, Scanner/Records/DTR/Logout popups, pull-to-refresh, QR scanning and navigation interactions.