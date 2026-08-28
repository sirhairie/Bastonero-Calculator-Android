from pathlib import Path
import re

SRC = Path('native/app/src/main/java/com/bastonero/calculator/nativeapp/MainActivity.java')
DRAW = Path('native/app/src/main/res/drawable')
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


def must(old, new, label):
    global s
    if old not in s:
        raise SystemExit(f'missing replacement for {label}')
    s = s.replace(old, new)


# TEST 6 identity/state while preserving the TEST 5 scoring engine.
s = s.replace('TEST 5', 'TEST 6').replace('bastonero_native_t5', 'bastonero_native_t6')

# Brighter metallic-gold family and slightly cleaner contrast.
s = s.replace('private static final int GOLD = Color.rgb(210,157,49);', 'private static final int GOLD = Color.rgb(224,169,50);')
s = s.replace('private static final int GOLD_2 = Color.rgb(244,194,66);', 'private static final int GOLD_2 = Color.rgb(255,203,72);')
s = s.replace('private static final int GOLD_LIGHT = Color.rgb(255,226,143);', 'private static final int GOLD_LIGHT = Color.rgb(255,235,164);')
s = s.replace('private static final int SILVER = Color.rgb(200,211,225);', 'private static final int SILVER = Color.rgb(218,226,238);')
s = s.replace('private static final int BRONZE = Color.rgb(197,102,43);', 'private static final int BRONZE = Color.rgb(213,119,55);')

# Compact responsive header: two-line brand, no truncation, and custom non-wrapping nav chips.
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
        toolbar.setPadding(dp(10),dp(8),dp(8),dp(8));
        toolbar.setBackground(gloss(Color.rgb(10,42,78), NAVY, BG, 0, 0));
        elevate(toolbar,5);

        LinearLayout logoPlate = new LinearLayout(this);
        logoPlate.setGravity(Gravity.CENTER);
        logoPlate.setBackground(gloss(Color.rgb(31,61,82), CARD, NAVY, dp(999), GOLD));
        elevate(logoPlate,7);
        ImageView logo = new ImageView(this);
        logo.setImageResource(R.drawable.brand_logo);
        logo.setScaleType(ImageView.ScaleType.FIT_CENTER);
        logoPlate.addView(logo,new LinearLayout.LayoutParams(dp(44),dp(44)));
        toolbar.addView(logoPlate,new LinearLayout.LayoutParams(dp(50),dp(50)));

        LinearLayout brand = new LinearLayout(this);
        brand.setOrientation(LinearLayout.VERTICAL);
        brand.setPadding(dp(8),0,dp(4),0);
        TextView title = text("Bastonero\nCalculator",15,WHITE,true);
        title.setMaxLines(2);
        title.setLineSpacing(0,.92f);
        brand.addView(title);
        LinearLayout subrow=row();subrow.setGravity(Gravity.CENTER_VERTICAL);
        TextView sub=text("Native Android • TEST 6",8,MUTED,true);sub.setSingleLine(true);subrow.addView(sub);
        TextView ver=pill("v2.0",GOLD_LIGHT,Color.rgb(70,51,13));
        ver.setTextSize(8);
        LinearLayout.LayoutParams vp=new LinearLayout.LayoutParams(-2,dp(22));vp.setMargins(dp(5),0,0,0);subrow.addView(ver,vp);
        brand.addView(subrow);
        toolbar.addView(brand,new LinearLayout.LayoutParams(0,-2,1f));

        LinearLayout home = navChip("Home",R.drawable.ic_home,true);
        home.setOnClickListener(v->showHome());
        toolbar.addView(home,new LinearLayout.LayoutParams(dp(58),dp(40)));
        LinearLayout about = navChip("About",R.drawable.ic_info,false);
        about.setOnClickListener(v->showAbout());
        LinearLayout.LayoutParams ap=new LinearLayout.LayoutParams(dp(62),dp(40));ap.setMargins(dp(5),0,0,0);toolbar.addView(about,ap);
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
    }''', 'buildShell')

# Competition count now sits directly beside the section title rather than floating at the far edge.
between('    private void showHome(){', '\n    private View competitionCard', '''    private void showHome(){
        screen=Screen.HOME; activeCompetition=null; editingCompetition=null; clearContent();
        LinearLayout hero=new LinearLayout(this);hero.setOrientation(LinearLayout.VERTICAL);
        LinearLayout titleLine=row();titleLine.setGravity(Gravity.CENTER_VERTICAL);
        titleLine.addView(text("YOUR COMPETITIONS",12,WHITE,true));
        TextView count=pill(String.valueOf(competitions.size()),WHITE,RED);
        LinearLayout.LayoutParams cp=new LinearLayout.LayoutParams(dp(30),dp(26));cp.setMargins(dp(7),0,0,0);titleLine.addView(count,cp);
        hero.addView(titleLine);
        TextView subtitle=text("Create, open, and manage tournament scoring",9,MUTED,false);subtitle.setPadding(0,dp(3),0,0);hero.addView(subtitle);
        content.addView(hero,fullMargins(0,0,0,dp(12)));
        Button add=primaryIconButton("Add Competition",BLUE_2,R.drawable.ic_add);add.setOnClickListener(v->{editingCompetition=null;showSetup();});content.addView(add,fullMargins(0,0,0,dp(16),dp(50)));
        if(competitions.isEmpty()){
            LinearLayout empty=darkCard(GOLD);empty.setGravity(Gravity.CENTER);empty.setPadding(dp(16),dp(28),dp(16),dp(28));
            ImageView sticks=iconView(R.drawable.ic_sticks,GOLD,68);sticks.setAlpha(.62f);empty.addView(sticks,new LinearLayout.LayoutParams(dp(68),dp(68)));
            TextView t=text("No competition yet",17,WHITE,true);t.setGravity(Gravity.CENTER);t.setPadding(0,dp(10),0,0);empty.addView(t);
            TextView b=text("Add your first competition to get started.",11,MUTED,false);b.setGravity(Gravity.CENTER);b.setPadding(0,dp(5),0,dp(16));empty.addView(b);
            Button a=outlineIconButton("Add Competition",BLUE_2,R.drawable.ic_add);a.setOnClickListener(v->showSetup());empty.addView(a,new LinearLayout.LayoutParams(dp(220),dp(44)));
            content.addView(empty);
        }else{
            for(Competition c:competitions) content.addView(competitionCard(c),fullMargins(0,0,0,dp(12)));
        }
        addFooter();
    }''', 'showHome')

# Stronger, crisper decorative sticks in card headers.
s = s.replace('watermark.setAlpha(.20f);', 'watermark.setAlpha(.34f);')
s = s.replace('sticks.setAlpha(.28f);', 'sticks.setAlpha(.38f);')
s = s.replace('sticks.setAlpha(.25f);', 'sticks.setAlpha(.38f);')

# Premium custom About modal; no standard gray Android dialog.
between('    private void showAbout(){', '\n    private void loadState()', '''    private void showAbout(){
        final Dialog d=new Dialog(this);
        d.requestWindowFeature(Window.FEATURE_NO_TITLE);
        ScrollView wrap=new ScrollView(this);wrap.setFillViewport(false);wrap.setVerticalScrollBarEnabled(false);wrap.setBackgroundColor(Color.TRANSPARENT);
        LinearLayout panel=darkCard(GOLD);panel.setPadding(dp(16),dp(16),dp(16),dp(16));

        LinearLayout head=row();head.setGravity(Gravity.CENTER_VERTICAL);
        LinearLayout logoPlate=new LinearLayout(this);logoPlate.setGravity(Gravity.CENTER);logoPlate.setBackground(gloss(Color.rgb(31,61,82),CARD,NAVY,dp(999),GOLD));elevate(logoPlate,7);
        ImageView logo=new ImageView(this);logo.setImageResource(R.drawable.brand_logo);logo.setScaleType(ImageView.ScaleType.FIT_CENTER);logoPlate.addView(logo,new LinearLayout.LayoutParams(dp(45),dp(45)));head.addView(logoPlate,new LinearLayout.LayoutParams(dp(52),dp(52)));
        LinearLayout hw=new LinearLayout(this);hw.setOrientation(LinearLayout.VERTICAL);hw.setPadding(dp(10),0,0,0);hw.addView(text("About Bastonero Native",19,WHITE,true));hw.addView(text("Premium native Arnis scoring application",9,MUTED,false));head.addView(hw,new LinearLayout.LayoutParams(0,-2,1f));panel.addView(head);

        View sep=divider();LinearLayout.LayoutParams sp=new LinearLayout.LayoutParams(-1,dp(1));sp.setMargins(0,dp(13),0,dp(12));panel.addView(sep,sp);
        TextView intro=text("BASTONERO CALCULATOR — NATIVE ANDROID",11,GOLD_2,true);panel.addView(intro);
        TextView body=text("TEST 6 Precision UI. Fully native Android interface and scoring engine—no WebView, HTML, CSS, or JavaScript.\n\nVISUAL SYSTEM\n• Responsive compact header\n• Mockup-matched navy, royal blue, and metallic gold\n• Custom Arnis and tournament vector icons\n• Raised gradient cards and beveled controls\n• Enhanced embossed medal ranking\n\nSCORING\n• Five judges, valid scores 7.0–10.0\n• Remove highest and lowest\n• Add the middle three scores\n• Subtract official penalty\n• Tied Final Score: use 5-judge total\n• Still tied: Repeat Performance\n\nDEVELOPER\nHairie A. Laysam\nSta. Maria National High School\n\nNative v2.0 • TEST 6",12,TEXT,false);body.setPadding(0,dp(9),0,dp(13));panel.addView(body);
        Button close=primaryIconButton("Close",BLUE_2,R.drawable.ic_check);close.setOnClickListener(v->d.dismiss());panel.addView(close,new LinearLayout.LayoutParams(-1,dp(46)));
        wrap.addView(panel,new ScrollView.LayoutParams(-1,-2));d.setContentView(wrap);d.show();
        Window w=d.getWindow();if(w!=null){w.setBackgroundDrawable(new android.graphics.drawable.ColorDrawable(Color.TRANSPARENT));w.addFlags(WindowManager.LayoutParams.FLAG_DIM_BEHIND);WindowManager.LayoutParams lp=w.getAttributes();lp.dimAmount=.76f;w.setAttributes(lp);int width=(int)(getResources().getDisplayMetrics().widthPixels*.90f);w.setLayout(width,WindowManager.LayoutParams.WRAP_CONTENT);}
    }''', 'showAbout')

# Compact setup fields and selectors while keeping notes comfortably multi-line.
between('    private LinearLayout field(String label,View input){', '\n    private void setSpinnerItems', '''    private LinearLayout field(String label,View input){
        LinearLayout f=new LinearLayout(this);f.setOrientation(LinearLayout.VERTICAL);
        TextView l=text(label,9,MUTED,true);l.setPadding(dp(2),0,0,dp(4));f.addView(l);
        int h=dp(44);
        if(input instanceof EditText && ((EditText)input).getMinLines()>1)h=dp(72);
        f.addView(input,new LinearLayout.LayoutParams(-1,h));
        LinearLayout.LayoutParams p=new LinearLayout.LayoutParams(-1,-2);p.setMargins(0,0,0,dp(9));f.setLayoutParams(p);return f;
    }''', 'compact field')

between('    private EditText input(String val,String hint,boolean number){', '\n    private Spinner spinner(', '''    private EditText input(String val,String hint,boolean number){EditText e=new EditText(this);e.setText(val==null?"":val);e.setHint(hint);e.setTextColor(WHITE);e.setHintTextColor(Color.rgb(110,139,168));e.setTextSize(12);e.setPadding(dp(10),dp(5),dp(10),dp(5));e.setBackground(gloss(Color.rgb(18,60,99),CARD_2,Color.rgb(5,29,55),dp(10),LINE));elevate(e,1);if(number)e.setInputType(android.text.InputType.TYPE_CLASS_NUMBER|android.text.InputType.TYPE_NUMBER_FLAG_DECIMAL);return e;}
    private void styleJudgeInput(EditText e,String value){boolean bad=false;String v=value==null?"":value.trim();if(!v.isEmpty()){try{double n=Double.parseDouble(v);bad=n<7||n>10;}catch(Exception ex){bad=true;}}if(bad)e.setBackground(gloss(Color.rgb(104,36,48),Color.rgb(71,22,34),Color.rgb(42,15,24),dp(9),Color.rgb(244,90,113)));else e.setBackground(gloss(Color.rgb(24,73,118),CARD_2,Color.rgb(5,29,55),dp(9),Color.rgb(68,102,137)));}
''', 'compact inputs')

# Stronger medal: filled metallic center + ribbon outline, readable dark rank number, and layered depth.
between('    private FrameLayout medalCoin(int rank,int accent){', '\n    private TextView textIconLabel', '''    private FrameLayout medalCoin(int rank,int accent){
        FrameLayout f=new FrameLayout(this);f.setClipChildren(false);f.setClipToPadding(false);
        View glow=new View(this);glow.setBackground(gloss(mix(accent,WHITE,.34f),accent,mix(accent,BG,.48f),dp(999),mix(accent,WHITE,.46f)));FrameLayout.LayoutParams gp=new FrameLayout.LayoutParams(dp(52),dp(52),Gravity.CENTER);gp.topMargin=dp(8);f.addView(glow,gp);elevate(glow,7);
        ImageView medal=iconView(R.drawable.ic_medal,accent,68);f.addView(medal,new FrameLayout.LayoutParams(dp(68),dp(68),Gravity.CENTER));
        TextView n=text(String.valueOf(rank),16,BG,true);n.setGravity(Gravity.CENTER);n.setBackground(gloss(GOLD_LIGHT,accent,mix(accent,BG,.20f),dp(999),GOLD_LIGHT));FrameLayout.LayoutParams np=new FrameLayout.LayoutParams(dp(34),dp(34),Gravity.CENTER);np.topMargin=dp(9);f.addView(n,np);elevate(n,9);elevate(f,10);return f;
    }''', 'medalCoin')

# Tighter footer spacing, with crisp Arnis ornaments.
between('    private void addFooter(){', '\n    private LinearLayout row()', '''    private void addFooter(){
        Space gap=new Space(this);content.addView(gap,new LinearLayout.LayoutParams(1,dp(34)));
        LinearLayout f=row();f.setGravity(Gravity.CENTER);ImageView a=iconView(R.drawable.ic_sticks,GOLD_2,25);a.setRotation(-12);TextView t=text("Develop by Sir Hairie Laysam",11,MUTED,false);t.setPadding(dp(9),0,dp(9),0);ImageView b=iconView(R.drawable.ic_sticks,GOLD_2,25);b.setRotation(12);f.addView(a,new LinearLayout.LayoutParams(dp(25),dp(25)));f.addView(t);f.addView(b,new LinearLayout.LayoutParams(dp(25),dp(25)));content.addView(f);
    }''', 'footer')

# Insert a purpose-built header navigation chip helper immediately before button helpers.
marker='    private Button primaryButton(String s,int color){'
if marker not in s:
    raise SystemExit('button marker missing for navChip')
nav='''    private LinearLayout navChip(String label,int iconRes,boolean active){
        LinearLayout x=new LinearLayout(this);x.setOrientation(LinearLayout.HORIZONTAL);x.setGravity(Gravity.CENTER);x.setPadding(dp(6),0,dp(6),0);
        int stroke=active?mix(BLUE_2,WHITE,.35f):GOLD;
        int top=active?mix(BLUE_2,WHITE,.24f):Color.rgb(19,47,75);
        int mid=active?BLUE_2:CARD;
        int bottom=active?mix(BLUE_2,BG,.34f):NAVY;
        x.setBackground(gloss(top,mid,bottom,dp(12),stroke));elevate(x,active?5:3);
        ImageView icon=iconView(iconRes,active?WHITE:GOLD,15);x.addView(icon,new LinearLayout.LayoutParams(dp(15),dp(15)));
        TextView txt=text(label,9,active?WHITE:GOLD,true);txt.setSingleLine(true);txt.setPadding(dp(4),0,0,0);x.addView(txt);
        x.setClickable(true);x.setFocusable(true);return x;
    }\n'''
s=s.replace(marker,nav+marker,1)

# Refine Arnis-sticks vector: thicker main sticks and clearer grip bands.
(DRAW/'ic_sticks.xml').write_text('''<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24">
<path android:fillColor="#00000000" android:strokeColor="#FFFFFFFF" android:strokeWidth="2.65" android:strokeLineCap="round" android:pathData="M4,20 L20,4"/>
<path android:fillColor="#00000000" android:strokeColor="#FFFFFFFF" android:strokeWidth="2.65" android:strokeLineCap="round" android:pathData="M4,4 L20,20"/>
<path android:fillColor="#00000000" android:strokeColor="#FFFFFFFF" android:strokeWidth="1.2" android:pathData="M3.2,16.8 L7.2,20.8 M4.2,15.8 L8.2,19.8 M16.8,3.2 L20.8,7.2 M15.8,4.2 L19.8,8.2 M3.2,7.2 L7.2,3.2 M4.2,8.2 L8.2,4.2 M16.8,20.8 L20.8,16.8 M15.8,19.8 L19.8,15.8"/>
</vector>''',encoding='utf-8')

# Result-sheet marker.
s=s.replace('TEST 6 • PREMIUM 3D','TEST 6 • PRECISION 3D')

SRC.write_text(s,encoding='utf-8')
print('TEST 6 precision UI patch applied')
