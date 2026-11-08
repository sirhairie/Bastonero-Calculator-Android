# PERMISO Recorder v1.2.0

Android companion for the existing https://www.smnhs.com/permiso/scanner-login.php

## Version 1.2 changes
- Uses the user-supplied document-approval logo as the Android launcher icon, toolbar emblem and error-panel icon.
- Removes the Open in Browser button. Refresh and Settings remain in the compact toolbar.
- Fixes a bug where incorrectly escaped JavaScript rejected the valid PERMISO login page, causing auto-login to do nothing.
- Uses exact page-origin and path checks in the WebView prior to submitting stored credentials.
- Detects username and password fields by their HTML properties and form, with retries for delayed form rendering.
- Keeps the same encrypted on-device Settings credentials saved in v1.1; no need to re-enter them if installed as an update preserving app data.

## Auto-login
Open Settings (gear) and enter an authorized Recorder username/password.
Enable Automatically sign in and tap Save.
The app submits those values through the existing first-party PERMISO login form.
Website authentication, QR scanner, Records and DTR functions are unchanged.
Authentication is not bypassed. If the site changes its form markup, its input fields
may require another selector update.

## Security
- AES-GCM encrypted credentials protected by Android Keystore.
- No credentials or login tokens in the GitHub repository.
- Auto-login is for a personal screen-locked phone; anyone able to open the unlocked phone could access its Recorder session.
- Do not use auto-login on shared phones.
- Clearing credentials does not sign out of an existing web session; use the website's sign-out control.
- Backups are disabled.

## GitHub build
GitHub Actions compiles an internally testable, debug-signed APK.
Because GitHub hosted debug signatures can change per run, an Android update may fail
due to incompatible signing. If so, uninstall the previous app and install the new one.
Uninstalling removes this app's local saved credentials, requiring Settings to be filled again.
