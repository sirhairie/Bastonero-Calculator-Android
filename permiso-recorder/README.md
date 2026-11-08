# PERMISO Recorder v1.5.0

## Immediate loading feedback
The v1.4 spinner could appear late because it waited for a full-page navigation callback and recognized only exact tab labels. Version 1.5 installs a first-party, capture-phase pointerdown listener, showing a visual-only loading popup before the page handles button clicks or navigation. Covers Scanner, Records, DTR, Logout, links, and other web buttons. A fallback click handler supports keyboard and accessibility interactions. The popup is non-interactive so it does not consume touches or change PERMISO actions. Camera-start/restart controls are excluded to keep the live QR scanner unobstructed.

The in-page indicator closes on a meaningful page update (with ~650 ms minimum visibility), on navigation, or at a 5.2-second fail-safe timeout. Native loading feedback remains for application launch, auto-login, full page navigation, and refresh.

## Preserved features
Full-height web UI, floating draggable Settings button, pull-to-refresh, locally encrypted saved credentials, QR scanning, Recorder records, DTR, download handling. No PERMISO website/database changes.

## Testing
Test Scanner, Records, DTR, Logout, other buttons, dialogs and QR camera on a phone. GitHub build success proves compilation only. Hosted debug signing might differ; reinstalling may remove saved local login information.
