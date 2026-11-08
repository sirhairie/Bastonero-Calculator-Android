package ph.com.smnhs.permiso.recorder;

import android.Manifest;
import android.app.Activity;
import android.app.AlertDialog;
import android.app.DownloadManager;
import android.content.ActivityNotFoundException;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.net.Uri;
import android.net.http.SslError;
import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.view.View;
import android.webkit.CookieManager;
import android.webkit.JsPromptResult;
import android.webkit.JsResult;
import android.webkit.PermissionRequest;
import android.webkit.SslErrorHandler;
import android.webkit.URLUtil;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceError;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.LinearLayout;
import android.widget.ProgressBar;
import android.widget.Toast;

public final class MainActivity extends Activity {
    private static final String LOGIN_URL =
            "https://www.smnhs.com/permiso/scanner-login.php";
    private static final int CAMERA_REQUEST_CODE = 2101;
    private static final int FILE_REQUEST_CODE = 2102;
    private static final int STORAGE_REQUEST_CODE = 2103;
    private WebView webView;
    private ProgressBar loadingBar;
    private LinearLayout errorPanel;
    private PermissionRequest pendingCameraPermission;
    private ValueCallback<Uri[]> pendingFileChooser;
    private DownloadInfo pendingDownload;

    private static final class DownloadInfo {
        final String url;
        final String userAgent;
        final String disposition;
        final String mimeType;
        DownloadInfo(String url, String userAgent, String disposition, String mimeType) {
            this.url = url;
            this.userAgent = userAgent;
            this.disposition = disposition;
            this.mimeType = mimeType;
        }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        webView = findViewById(R.id.recorderWebView);
        loadingBar = findViewById(R.id.loadingBar);
        errorPanel = findViewById(R.id.errorPanel);
        ImageButton reload = findViewById(R.id.reloadButton);
        ImageButton browser = findViewById(R.id.browserButton);
        reload.setOnClickListener(v -> retry());
        findViewById(R.id.retryButton).setOnClickListener(v -> retry());
        browser.setOnClickListener(v -> openExternal(Uri.parse(LOGIN_URL)));
        configureWebView();
        if (savedInstanceState != null && webView.restoreState(savedInstanceState) != null) {
            // Retain the scanner page across screen rotations.
        } else {
            webView.loadUrl(LOGIN_URL);
        }
    }

    private void configureWebView() {
        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setAllowFileAccess(false);
        settings.setAllowContentAccess(true);
        settings.setJavaScriptCanOpenWindowsAutomatically(false);
        settings.setSupportMultipleWindows(false);
        settings.setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW);
        settings.setCacheMode(WebSettings.LOAD_DEFAULT);
        settings.setMediaPlaybackRequiresUserGesture(false);
        settings.setBuiltInZoomControls(false);
        settings.setDisplayZoomControls(false);
        settings.setSupportZoom(false);
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            settings.setSafeBrowsingEnabled(true);
        }
        CookieManager.getInstance().setAcceptCookie(true);
        CookieManager.getInstance().setAcceptThirdPartyCookies(webView, false);

        webView.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                Uri uri = request.getUrl();
                if (isTrustedUrl(uri)) return false;
                if (isSafeExternalWebUrl(uri) && request.isForMainFrame()) {
                    openExternal(uri);
                }
                return true;
            }
            @Override
            public void onPageStarted(WebView view, String url, Bitmap favicon) {
                errorPanel.setVisibility(View.GONE);
                loadingBar.setVisibility(View.VISIBLE);
                loadingBar.setProgress(4);
            }
            @Override
            public void onPageFinished(WebView view, String url) {
                loadingBar.setProgress(100);
                loadingBar.setVisibility(View.GONE);
            }
            @Override
            public void onReceivedError(WebView view, WebResourceRequest request,
                                        WebResourceError error) {
                if (request.isForMainFrame()) showConnectionError();
            }
            @Override
            public void onReceivedHttpError(WebView view, WebResourceRequest request,
                                            WebResourceResponse response) {
                if (request.isForMainFrame() && response.getStatusCode() >= 500) {
                    showConnectionError();
                }
            }
            @Override
            public void onReceivedSslError(WebView view, SslErrorHandler handler, SslError error) {
                handler.cancel();
                showConnectionError();
            }
        });

        webView.setWebChromeClient(new WebChromeClient() {
            @Override
            public void onProgressChanged(WebView view, int newProgress) {
                loadingBar.setProgress(newProgress);
                if (newProgress >= 100) loadingBar.setVisibility(View.GONE);
            }
            @Override
            public void onPermissionRequest(PermissionRequest request) {
                runOnUiThread(() -> handleWebPermission(request));
            }
            @Override
            public void onPermissionRequestCanceled(PermissionRequest request) {
                runOnUiThread(() -> {
                    if (pendingCameraPermission == request) pendingCameraPermission = null;
                });
            }
            @Override
            public boolean onShowFileChooser(WebView view,
                                             ValueCallback<Uri[]> filePathCallback,
                                             FileChooserParams chooserParams) {
                if (pendingFileChooser != null) pendingFileChooser.onReceiveValue(null);
                pendingFileChooser = filePathCallback;
                try {
                    startActivityForResult(chooserParams.createIntent(), FILE_REQUEST_CODE);
                    return true;
                } catch (ActivityNotFoundException ex) {
                    pendingFileChooser = null;
                    Toast.makeText(MainActivity.this, "No file picker available", Toast.LENGTH_LONG).show();
                    return false;
                }
            }
            @Override
            public boolean onJsAlert(WebView view, String url, String message, JsResult result) {
                if (!isTrustedUrl(Uri.parse(url))) return false;
                new AlertDialog.Builder(MainActivity.this)
                        .setTitle("PERMISO")
                        .setMessage(message)
                        .setPositiveButton("OK", (dialog, which) -> result.confirm())
                        .setOnCancelListener(dialog -> result.cancel())
                        .show();
                return true;
            }
            @Override
            public boolean onJsConfirm(WebView view, String url, String message, JsResult result) {
                if (!isTrustedUrl(Uri.parse(url))) return false;
                new AlertDialog.Builder(MainActivity.this)
                        .setTitle("PERMISO")
                        .setMessage(message)
                        .setPositiveButton("Confirm", (dialog, which) -> result.confirm())
                        .setNegativeButton("Cancel", (dialog, which) -> result.cancel())
                        .setOnCancelListener(dialog -> result.cancel())
                        .show();
                return true;
            }
            @Override
            public boolean onJsPrompt(WebView view, String url, String message,
                                      String defaultValue, JsPromptResult result) {
                if (!isTrustedUrl(Uri.parse(url))) return false;
                EditText answer = new EditText(MainActivity.this);
                answer.setSingleLine(false);
                answer.setText(defaultValue);
                new AlertDialog.Builder(MainActivity.this)
                        .setTitle("PERMISO")
                        .setMessage(message)
                        .setView(answer)
                        .setPositiveButton("OK", (dialog, which) -> result.confirm(answer.getText().toString()))
                        .setNegativeButton("Cancel", (dialog, which) -> result.cancel())
                        .setOnCancelListener(dialog -> result.cancel())
                        .show();
                return true;
            }
        });

        webView.setDownloadListener((url, userAgent, contentDisposition, mimeType, contentLength) -> {
            Uri uri = Uri.parse(url);
            if (!isTrustedUrl(uri)) {
                Toast.makeText(this, "Download blocked: untrusted address", Toast.LENGTH_SHORT).show();
                return;
            }
            DownloadInfo info = new DownloadInfo(url, userAgent, contentDisposition, mimeType);
            if (Build.VERSION.SDK_INT < Build.VERSION_CODES.Q &&
                    checkSelfPermission(Manifest.permission.WRITE_EXTERNAL_STORAGE)
                            != PackageManager.PERMISSION_GRANTED) {
                pendingDownload = info;
                requestPermissions(new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE},
                        STORAGE_REQUEST_CODE);
            } else {
                downloadFile(info);
            }
        });
    }

    private static boolean isTrustedHost(String host) {
        return host != null && (host.equalsIgnoreCase("www.smnhs.com")
                || host.equalsIgnoreCase("smnhs.com"));
    }
    private static boolean isSafeExternalWebUrl(Uri uri) {
        return uri != null && ("https".equalsIgnoreCase(uri.getScheme())
                || "http".equalsIgnoreCase(uri.getScheme()));
    }
    private static boolean isTrustedUrl(Uri uri) {
        if (uri == null || !"https".equalsIgnoreCase(uri.getScheme())) return false;
        if (!isTrustedHost(uri.getHost())) return false;
        String path = uri.getPath();
        return path != null && (path.equals("/permiso") || path.startsWith("/permiso/"));
    }

    private void handleWebPermission(PermissionRequest request) {
        Uri origin = request.getOrigin();
        if (origin == null || !"https".equalsIgnoreCase(origin.getScheme())
                || !isTrustedHost(origin.getHost())) {
            request.deny();
            return;
        }
        boolean requestsCamera = false;
        for (String resource : request.getResources()) {
            if (PermissionRequest.RESOURCE_VIDEO_CAPTURE.equals(resource)) {
                requestsCamera = true;
            } else {
                request.deny();
                return;
            }
        }
        if (!requestsCamera) {
            request.deny();
            return;
        }
        if (pendingCameraPermission != null && pendingCameraPermission != request) {
            pendingCameraPermission.deny();
        }
        pendingCameraPermission = request;
        if (checkSelfPermission(Manifest.permission.CAMERA)
                == PackageManager.PERMISSION_GRANTED) {
            grantPendingCamera();
        } else {
            requestPermissions(new String[]{Manifest.permission.CAMERA}, CAMERA_REQUEST_CODE);
        }
    }
    private void grantPendingCamera() {
        PermissionRequest request = pendingCameraPermission;
        pendingCameraPermission = null;
        if (request != null) {
            request.grant(new String[]{PermissionRequest.RESOURCE_VIDEO_CAPTURE});
        }
    }
    private void retry() {
        errorPanel.setVisibility(View.GONE);
        String current = webView.getUrl();
        if (current != null && isTrustedUrl(Uri.parse(current))) webView.reload();
        else webView.loadUrl(LOGIN_URL);
    }
    private void showConnectionError() {
        errorPanel.setVisibility(View.VISIBLE);
        loadingBar.setVisibility(View.GONE);
    }
    private void openExternal(Uri uri) {
        if (!isSafeExternalWebUrl(uri)) return;
        try {
            startActivity(new Intent(Intent.ACTION_VIEW, uri));
        } catch (ActivityNotFoundException ex) {
            Toast.makeText(this, "No browser is installed", Toast.LENGTH_SHORT).show();
        }
    }
    private void downloadFile(DownloadInfo info) {
        try {
            DownloadManager.Request request = new DownloadManager.Request(Uri.parse(info.url));
            String filename = URLUtil.guessFileName(info.url, info.disposition, info.mimeType);
            filename = filename.replaceAll("[\\\\/:*?\"<>|\\p{Cntrl}]", "_");
            request.setTitle(filename);
            request.setDescription("PERMISO Recorder file");
            request.setNotificationVisibility(DownloadManager.Request.VISIBILITY_VISIBLE_NOTIFY_COMPLETED);
            if (info.mimeType != null && !info.mimeType.isEmpty()) request.setMimeType(info.mimeType);
            String cookie = CookieManager.getInstance().getCookie(info.url);
            if (cookie != null) request.addRequestHeader("Cookie", cookie);
            if (info.userAgent != null) request.addRequestHeader("User-Agent", info.userAgent);
            request.addRequestHeader("Referer", webView.getUrl() == null ? LOGIN_URL : webView.getUrl());
            request.setDestinationInExternalPublicDir(Environment.DIRECTORY_DOWNLOADS, filename);
            DownloadManager manager = (DownloadManager) getSystemService(Context.DOWNLOAD_SERVICE);
            if (manager == null) throw new IllegalStateException("Download service unavailable");
            manager.enqueue(request);
            Toast.makeText(this, "Downloading to Downloads", Toast.LENGTH_LONG).show();
        } catch (Exception ex) {
            Toast.makeText(this, "Download could not start", Toast.LENGTH_LONG).show();
        }
    }
    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions,
                                           int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        boolean granted = grantResults.length > 0
                && grantResults[0] == PackageManager.PERMISSION_GRANTED;
        if (requestCode == CAMERA_REQUEST_CODE) {
            if (granted) grantPendingCamera();
            else {
                PermissionRequest request = pendingCameraPermission;
                pendingCameraPermission = null;
                if (request != null) request.deny();
                Toast.makeText(this, "Camera access is required for QR scanning", Toast.LENGTH_LONG).show();
            }
        } else if (requestCode == STORAGE_REQUEST_CODE) {
            DownloadInfo info = pendingDownload;
            pendingDownload = null;
            if (granted && info != null) downloadFile(info);
            else Toast.makeText(this, "Storage permission is needed for downloads", Toast.LENGTH_LONG).show();
        }
    }
    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (requestCode == FILE_REQUEST_CODE && pendingFileChooser != null) {
            Uri[] results = WebChromeClient.FileChooserParams.parseResult(resultCode, data);
            pendingFileChooser.onReceiveValue(results);
            pendingFileChooser = null;
        }
    }
    @Override
    protected void onSaveInstanceState(Bundle outState) {
        super.onSaveInstanceState(outState);
        webView.saveState(outState);
    }
    @Override
    public void onBackPressed() {
        if (errorPanel.getVisibility() == View.VISIBLE) retry();
        else if (webView.canGoBack()) webView.goBack();
        else super.onBackPressed();
    }
    @Override
    protected void onDestroy() {
        if (pendingFileChooser != null) {
            pendingFileChooser.onReceiveValue(null);
            pendingFileChooser = null;
        }
        if (pendingCameraPermission != null) {
            pendingCameraPermission.deny();
            pendingCameraPermission = null;
        }
        if (webView != null) {
            webView.stopLoading();
            webView.setWebChromeClient(null);
            webView.setWebViewClient(null);
            webView.destroy();
        }
        super.onDestroy();
    }
}
