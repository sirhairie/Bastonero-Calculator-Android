package ph.com.smnhs.permiso.recorder;

/**
 * Visual-only early navigation feedback. No credentials or record data are accessed.
 * Non-interactive overlay never consumes website taps, camera, or confirmation input.
 */
final class NavigationFeedback {
    private NavigationFeedback() {}

    static String script() {
        return """
        (function() {
          if (location.protocol !== 'https:' ||
              !['smnhs.com','www.smnhs.com'].includes(location.hostname) ||
              !(location.pathname === '/permiso' ||
                location.pathname.startsWith('/permiso/'))) return;
          if (window.__permisoNavFeedbackV15) return;
          window.__permisoNavFeedbackV15 = true;
          var overlay=null,observer=null,finishTimer=null,safetyTimer=null;
          var active=null,begin=0,pointer=null;
          function remove() {
            if (finishTimer) clearTimeout(finishTimer);
            if (safetyTimer) clearTimeout(safetyTimer);
            if (observer) observer.disconnect();
            if (overlay) overlay.remove();
            overlay=null;observer=null;finishTimer=null;safetyTimer=null;
            pointer=null;active=null;
          }
          function getControl(target) {
            var e=target && (target.nodeType===1 ? target : target.parentElement);
            return e && e.closest ? e.closest(
              'a,button,input[type=submit],input[type=button],' +
              '[role=tab],[role=button],[onclick],.nav-link,.btn') : null;
          }
          function label(el) {
            return String(el.getAttribute('aria-label') ||
              el.getAttribute('title') || el.innerText ||
              el.textContent || el.value || '').trim().toLowerCase();
          }
          function allowed(el) {
            if (!el || el.disabled || el.getAttribute('aria-disabled')==='true') return false;
            var l=label(el);
            // Do not interrupt starting, restarting or switching the QR camera.
            if (l.includes('start camera') || l.includes('camera scanner') ||
                l.includes('scan qr') || l.includes('switch camera') ||
                l.includes('restart camera') || l.includes('stop camera')) return false;
            return true;
          }
          function finishLater() {
            if (finishTimer || !overlay) return;
            finishTimer=setTimeout(remove,Math.max(70,650-(Date.now()-begin)));
          }
          function show(el) {
            if (!document.body || !allowed(el) || overlay) return;
            active=el;
            var css=document.getElementById('permiso-nav-spinner-style-v15');
            if (!css) {
              css=document.createElement('style');
              css.id='permiso-nav-spinner-style-v15';
              css.textContent='@keyframes permiso-spin-v15{to{transform:rotate(360deg)}}';
              (document.head || document.documentElement).appendChild(css);
            }
            var signout=label(el).includes('logout') ||
              label(el).includes('log out') || label(el).includes('sign out');
            overlay=document.createElement('div');
            overlay.id='permiso-app-nav-overlay';
            overlay.setAttribute('role','status');
            overlay.style.cssText='position:fixed;inset:0;z-index:2147483646;' +
              'display:flex;justify-content:center;align-items:center;' +
              'background:rgba(6,25,46,.55);pointer-events:none;';
            var box=document.createElement('div');
            box.style.cssText='min-width:192px;max-width:85vw;background:#fff;' +
              'border-radius:18px;padding:25px 24px;text-align:center;' +
              'box-shadow:0 12px 30px rgba(0,0,0,.20);' +
              'font:600 16px system-ui,sans-serif;color:#17324A';
            var circle=document.createElement('div');
            circle.style.cssText='height:42px;width:42px;' +
              'border:4px solid #DAE9EE;border-top-color:#23B9A8;' +
              'border-radius:50%;animation:permiso-spin-v15 .8s linear infinite;' +
              'margin:0 auto 14px';
            var heading=document.createElement('div');
            heading.textContent=signout ? 'Signing out…' : 'Loading page…';
            var sub=document.createElement('div');
            sub.textContent='Please wait a moment';
            sub.style.cssText='font:400 13px system-ui,sans-serif;' +
              'color:#637789;margin-top:5px';
            box.appendChild(circle);box.appendChild(heading);box.appendChild(sub);
            overlay.appendChild(box);document.body.appendChild(overlay);
            begin=Date.now();
            observer=new MutationObserver(function(records) {
              var changed=records.some(function(r) {
                var n=r.target;
                if (!n || n===overlay || overlay.contains(n)) return false;
                if (n.id==='permiso-nav-spinner-style-v15') return false;
                if (active && (n===active ||
                  (active.contains && active.contains(n))) &&
                  r.attributeName!=='aria-selected') return false;
                return true;
              });
              if (changed) finishLater();
            });
            observer.observe(document.body,{childList:true,subtree:true,
              attributes:true,attributeFilter:['class','style','hidden','aria-selected']});
            safetyTimer=setTimeout(remove,5200);
          }
          // Pointerdown occurs before click, URL navigation and AJAX handlers.
          document.addEventListener('pointerdown',function(e) {
            if (e.button!==undefined && e.button!==0) return;
            var control=getControl(e.target);
            if (!allowed(control)) return;
            pointer={x:e.clientX,y:e.clientY};
            show(control);
          },true);
          document.addEventListener('pointermove',function(e) {
            if (pointer && Math.hypot(e.clientX-pointer.x,e.clientY-pointer.y)>18) {
              remove(); // scrolling gesture, not a button tap
            }
          },true);
          document.addEventListener('pointercancel',remove,true);
          // Keyboard activation, accessibility services and synthetic clicks.
          document.addEventListener('click',function(e) {
            var control=getControl(e.target);
            if (!overlay && allowed(control)) show(control);
          },true);
          document.addEventListener('submit',function(e) {
            if (!overlay && e.target && e.target.tagName==='FORM') {
              var btn=e.submitter || e.target.querySelector(
                'button[type=submit],input[type=submit]');
              if (btn) show(btn);
            }
          },true);
          window.addEventListener('pagehide',remove,true);
        })();
        """;
    }
}
