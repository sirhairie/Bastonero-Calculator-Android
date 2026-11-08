# PERMISO Recorder v1.1.0 (Android)

Android companion for the existing PERMISO Recorder:
https://www.smnhs.com/permiso/scanner-login.php

## v1.1 improvements
- Replaced repeated native title + subtitle with a compact icon-only toolbar (refresh, browser, settings). The site retains its own header.
- Native Settings screen for the authorized Recorder username/password.
- Option for automatic login at app launch or after saving settings.
- Encrypted local credential storage using device-backed **Android Keystore AES-256-GCM** (no server/database change and no passwords in the GitHub source).
- Auto-login only injects credential values into the exact trusted HTTPS scanner-login.php path, uses the website's own form, and attempts once per app launch to avoid failed-login loops.
- Show/hide password, clear saved login, and user-facing private-device security advisory.

## Notes and security
- This feature is opt-in: open gear icon and enter existing Recorder credentials.
- The encrypted credentials are local to the phone. Android app backup is disabled.
- **Anyone who can unlock a phone using automatic login can potentially access the Recorder account.** Enable only on a private phone with a secure screen lock.
- Clearing saved login does not log out the existing website session; use the website's logout/back control for that.
- If the website changes its HTML form, auto-login form selectors may need maintenance.
- All scanner, records, and DTR operations remain in the existing PERMISO website.
- The app never receives special backend privileges or bypasses password checks.

## Building
GitHub Actions workflow is at ../.github/workflows/build-permiso-recorder.yml.
Builds an installable **debug-signed** APK for internal sideload testing using Java 17, Gradle 8.9 and Android API 35.
Open the workflow's successful run and download its APK artifact. It isn't a Play Store production-signed release.
