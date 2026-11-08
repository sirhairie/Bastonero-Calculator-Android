# PERMISO Recorder (Android)
Android WebView companion for the existing PERMISO Recorder scanner login:
https://www.smnhs.com/permiso/scanner-login.php

- Uses the existing PERMISO Recorder login and backend.
- Camera access is requested for trusted PERMISO QR scanning, with Android runtime permission.
- Permits authenticated PDF/document downloads.
- Restricts WebView navigation to HTTPS and the PERMISO path on smnhs.com.
- Contains no database credentials or embedded user passwords.

## GitHub Actions build
The workflow at ../.github/workflows/build-permiso-recorder.yml compiles a debug APK with Java 17, Android API 35, Gradle 8.9 and Android Gradle Plugin 8.7.3.
Open the Actions tab and download the artifact named PERMISO-Recorder-v1.0-debug-APK.
This is a debug-signed sideload APK for internal testing, not a production-signed Play Store release.
The vector app icon is a lightweight alternative to the raster icon from the original source ZIP.
The original website and database are not changed.
