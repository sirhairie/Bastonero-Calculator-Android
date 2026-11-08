package ph.com.smnhs.permiso.recorder;

/**
 * A visual-only helper for tabs that switch panels without a main-frame load.
 * This script never sees credentials, controls authentication or alters scans.
 */
final class NavigationFeedback {
    private NavigationFeedback() {}

    static String script() {
        return """
        (function () {
          if (window.__permisoRecorderNavSpinnerV14) return;
          window.__permisoRecorderNavSpinnerV14 = true;

          var overlay = null, observer = null, maxTimer = null, closeTimer = null;
          var startedAt = 0;

          function removeSpinner() {
            if (maxTimer) { clearTimeout(maxTimer); maxTimer = null; }
            if (closeTimer) { clearTimeout(closeTimer); closeTimer = null; }
            if (observer) { observer.disconnect(); observer = null; }
            if (overlay) { overlay.remove(); overlay = null; }
          }

          function showSpinner() {
            removeSpinner();
            var style = document.getElementById('permiso-app-nav-style');
            if (!style) {
              style = document.createElement('style');
              style.id = 'permiso-app-nav-style';
              style.textContent = '@keyframes permiso-app-spin{to{transform:rotate(360deg)}}';
              document.head.appendChild(style);
            }
            overlay = document.createElement('div');
            overlay.id = 'permiso-app-nav-overlay';
            overlay.setAttribute('role', 'status');
            overlay.setAttribute('aria-label', 'Loading page');
            overlay.style.cssText = 'position:fixed;inset:0;display:flex;align-items:center;justify-content:center;z-index:2147483646;background:rgba(6,25,46,.55);pointer-events:none;';
            overlay.innerHTML = '<div style="min-width:192px;max-width:85vw;background:white;border-radius:18px;padding:25px 24px;text-align:center;box-shadow:0 12px 30px rgba(0,0,0,.20);font:600 16px system-ui,sans-serif;color:#17324A">'
              + '<div style="height:42px;width:42px;border:4px solid #DAE9EE;border-top-color:#23B9A8;border-radius:50%;animation:permiso-app-spin .8s linear infinite;margin:0 auto 14px"></div>'
              + 'Loading page…<div style="font:400 13px system-ui,sans-serif;color:#637789;margin-top:5px">Please wait a moment</div></div>';
            document.body.appendChild(overlay);
            startedAt = Date.now();

            // End visual feedback after the site changes tabs/panels.
            observer = new MutationObserver(function(changes) {
              var changed = changes.some(function(record) {
                var node = record.target;
                return node && node !== overlay && !overlay.contains(node)
                    && node.id !== 'permiso-app-nav-style';
              });
              if (changed && !closeTimer) {
                closeTimer = setTimeout(removeSpinner,
                    Math.max(1, 400 - (Date.now() - startedAt)));
              }
            });
            observer.observe(document.body, {
              childList: true, subtree: true, attributes: true,
              attributeFilter: ['style','class','hidden','aria-selected']
            });
            // Fail-safe: never leave a tab transition obscured indefinitely.
            maxTimer = setTimeout(removeSpinner, 4500);
          }

          document.addEventListener('click', function(event) {
            var target = event.target && event.target.closest
              ? event.target.closest('a,button,[role="tab"]') : null;
            if (!target) return;
            var label = String(target.textContent || '').trim().toLowerCase().replace(/\\s+/g,' ');
            if (label === 'scanner' || label === 'records' || label === 'dtr') {
              showSpinner();
            }
          }, true);
          window.addEventListener('pagehide', removeSpinner);
        })();
        """;
    }
}
