# PERMISO Recorder v1.3.0

## Interface
- No native app title bar or repeated PERMISO branding: the website uses the available screen height, below the Android system status bar.
- A discreet round floating Settings button replaces the entire native toolbar. Tap for the existing native Settings screen; drag the bubble away from the website's scanner/action controls.
- Pull down from the top of the page to refresh; refresh is disabled while the QR camera stream is granted/active to avoid unexpected scanner interruptions.
- Small loading bar and existing connection-error retry remain.

## Unchanged operations
- Auto-login through the existing authorized HTTPS PERMISO Recorder login form, with opt-in encrypted credentials stored only on-device using Android Keystore.
- Camera permissions and QR scan, Recorder records, DTR and download handling use the existing live PERMISO backend.
- No website or database modifications.

## Installing
GitHub Actions compiles a debug-signed Android APK (Android 8.0+). Android may reject an update if debug signatures differ across GitHub builds. If this happens, uninstall the previous app, install v1.3.0 and enter your saved login again in Settings. Uninstallation removes saved login from the phone but does not affect server-side PERMISO data.
Use auto-login only on a private phone protected by a screen lock.

## Validation
After installation, test dragging the floating gear, pull-to-refresh, automatic sign-in, camera QR scanning, Records and DTR on a physical Android device. A GitHub build success is not proof of runtime functionality.
