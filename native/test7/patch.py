from pathlib import Path
import re

SRC = Path('native/app/src/main/java/com/bastonero/calculator/nativeapp/MainActivity.java')
s = SRC.read_text(encoding='utf-8')


def between(start, end, new, label):
    global s
    i = s.find(start)
    if i < 0:
        raise SystemExit(f'missing start for {label}: {start}')
    j = s.find(end, i)
    if j < 0:
        raise SystemExit(f'missing end for {label}: {end}')
    s = s[:i] + new.rstrip() + '\n\n' + s[j:]


# TEST 7 identity while preserving the working TEST 6 scoring and UI engine.
s = s.replace('TEST 6', 'TEST 7').replace('bastonero_native_t6', 'bastonero_native_t7')

# Clean production-style header:
# - Bastonero Calculator stays on one line
# - no Native Android / TEST / version badge in the visible header
# - compact Home and About chips leave maximum width for the brand title
between('    private void buildShell() {', '\n    private void clearContent()', '''    private void buildShell() {
        shell = new LinearLayout(this);
        shell.setOrientation(LinearLayout.VERTICAL);
        shell.setBackgroundColor(BG);
        shell.setLayoutParams(new LinearLayout.LayoutParams(-1,-1));
        shell.setOnApplyWindowInsetsListener((v, insets) -> {
            v.setPadding(insets.getSystemWindowInsetLeft(), insets.getSystemWindowInsetTop(), insets.getSystemWindowInsetRight(), insets.getSystemWindowInsetBottom());
            return insets;
        });

        LinearLayout toolbar = new LinearLayout(this);
        toolbar.setOrientation(LinearLayout.HORIZONTAL);
        toolbar.setGravity(Gravity.CENTER_VERTICAL);
        toolbar.setPadding(dp(8),dp(8),dp(7),dp(8));
        toolbar.setBackground(gloss(Color.rgb(10,42,78), NAVY, BG, 0, 0));
        elevate(toolbar,5);

        LinearLayout logoPlate = new LinearLayout(this);
        logoPlate.setGravity(Gravity.CENTER);
        logoPlate.setBackground(gloss(Color.rgb(31,61,82), CARD, NAVY, dp(999), GOLD));
        elevate(logoPlate,7);
        ImageView logo = new ImageView(this);
        logo.setImageResource(R.drawable.brand_logo);
        logo.setScaleType(ImageView.ScaleType.FIT_CENTER);
        logoPlate.addView(logo,new LinearLayout.LayoutParams(dp(40),dp(40)));
        toolbar.addView(logoPlate,new LinearLayout.LayoutParams(dp(46),dp(46)));

        TextView title = text("Bastonero Calculator",16,WHITE,true);
        title.setSingleLine(true);
        title.setGravity(Gravity.CENTER_VERTICAL);
        title.setPadding(dp(7),0,dp(4),0);
        if(Build.VERSION.SDK_INT >= 26){
            title.setAutoSizeTextTypeUniformWithConfiguration(12,16,1,android.util.TypedValue.COMPLEX_UNIT_SP);
        }
        toolbar.addView(title,new LinearLayout.LayoutParams(0,dp(46),1f));

        LinearLayout home = navChip("Home",R.drawable.ic_home,true);
        home.setOnClickListener(v->showHome());
        toolbar.addView(home,new LinearLayout.LayoutParams(dp(52),dp(38)));
        LinearLayout about = navChip("About",R.drawable.ic_info,false);
        about.setOnClickListener(v->showAbout());
        LinearLayout.LayoutParams ap=new LinearLayout.LayoutParams(dp(56),dp(38));ap.setMargins(dp(4),0,0,0);toolbar.addView(about,ap);
        shell.addView(toolbar,new LinearLayout.LayoutParams(-1,-2));

        scroll = new ScrollView(this);
        scroll.setFillViewport(true);
        scroll.setBackgroundColor(BG);
        content = new LinearLayout(this);
        content.setOrientation(LinearLayout.VERTICAL);
        content.setPadding(dp(12),dp(13),dp(12),dp(24));
        scroll.addView(content,new ScrollView.LayoutParams(-1,-2));
        shell.addView(scroll,new LinearLayout.LayoutParams(-1,0,1f));
        setContentView(shell);
    }''', 'TEST 7 clean header')

# More compact header navigation chips to prevent title compression.
between('    private LinearLayout navChip(String label,int iconRes,boolean active){', '\n    private Button primaryButton', '''    private LinearLayout navChip(String label,int iconRes,boolean active){
        LinearLayout x=new LinearLayout(this);x.setOrientation(LinearLayout.HORIZONTAL);x.setGravity(Gravity.CENTER);x.setPadding(dp(4),0,dp(4),0);
        int stroke=active?mix(BLUE_2,WHITE,.35f):GOLD;
        int top=active?mix(BLUE_2,WHITE,.24f):Color.rgb(19,47,75);
        int mid=active?BLUE_2:CARD;
        int bottom=active?mix(BLUE_2,BG,.34f):NAVY;
        x.setBackground(gloss(top,mid,bottom,dp(11),stroke));elevate(x,active?5:3);
        ImageView icon=iconView(iconRes,active?WHITE:GOLD,14);x.addView(icon,new LinearLayout.LayoutParams(dp(14),dp(14)));
        TextView txt=text(label,8,active?WHITE:GOLD,true);txt.setSingleLine(true);txt.setGravity(Gravity.CENTER);txt.setPadding(dp(3),0,0,0);x.addView(txt);
        return x;
    }''', 'TEST 7 compact nav chips')

# Remove the crossed-sticks/X decoration that sat immediately before SCORING / REGISTERING
# on Home competition cards. Other intentional Arnis decorations remain intact.
pattern = (r'\s*ImageView watermark=iconView\(R\.drawable\.ic_sticks,GOLD,34\);'
           r'watermark\.setAlpha\(\.34f\);'
           r'top\.addView\(watermark,new LinearLayout\.LayoutParams\(dp\(34\),dp\(34\)\)\);')
s, removed = re.subn(pattern, '', s, count=1)
if removed != 1:
    raise SystemExit(f'expected to remove exactly one competition-card status watermark, removed {removed}')

SRC.write_text(s, encoding='utf-8')
print('TEST 7 clean header/status patch applied')
