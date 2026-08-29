from pathlib import Path

SRC = Path('native/app/src/main/java/com/bastonero/calculator/nativeapp/MainActivity.java')
s = SRC.read_text(encoding='utf-8')


def must(old, new, label):
    global s
    if old not in s:
        raise SystemExit(f'missing TEST 8 replacement: {label}')
    s = s.replace(old, new, 1)


def between(start, end, new, label):
    global s
    i = s.find(start)
    if i < 0:
        raise SystemExit(f'missing start for {label}: {start}')
    j = s.find(end, i)
    if j < 0:
        raise SystemExit(f'missing end for {label}: {end}')
    s = s[:i] + new.rstrip() + '\n\n' + s[j:]


# TEST 8 identity only; scoring and competition data logic remain unchanged.
s = s.replace('TEST 7', 'TEST 8').replace('bastonero_native_t7', 'bastonero_native_t8')

# Header: keep the one-line title, but change Home/About into icon-only controls.
# Home stays blue. About becomes a filled metallic-gold control.
between('    private LinearLayout navChip(String label,int iconRes,boolean active){', '\n    private Button primaryButton', '''    private LinearLayout navChip(String label,int iconRes,boolean active){
        LinearLayout x=new LinearLayout(this);
        x.setGravity(Gravity.CENTER);
        int stroke=active?mix(BLUE_2,WHITE,.42f):GOLD_LIGHT;
        int top=active?mix(BLUE_2,WHITE,.28f):GOLD_LIGHT;
        int mid=active?BLUE_2:GOLD_2;
        int bottom=active?mix(BLUE_2,BG,.30f):GOLD;
        x.setBackground(gloss(top,mid,bottom,dp(12),stroke));
        elevate(x,active?6:5);
        ImageView icon=iconView(iconRes,active?WHITE:BG,active?21:20);
        x.addView(icon,new LinearLayout.LayoutParams(dp(active?21:20),dp(active?21:20)));
        return x;
    }''', 'TEST 8 icon-only nav chips')

# Slightly larger icon-only buttons and more space for the one-line brand title.
must('toolbar.addView(home,new LinearLayout.LayoutParams(dp(52),dp(38)));',
     'toolbar.addView(home,new LinearLayout.LayoutParams(dp(44),dp(42)));',
     'Home control dimensions')
must('LinearLayout.LayoutParams ap=new LinearLayout.LayoutParams(dp(56),dp(38));ap.setMargins(dp(4),0,0,0);toolbar.addView(about,ap);',
     'LinearLayout.LayoutParams ap=new LinearLayout.LayoutParams(dp(44),dp(42));ap.setMargins(dp(5),0,0,0);toolbar.addView(about,ap);',
     'About control dimensions')

# Home screen Add Competition: remove plus icon and change the button to green.
must('Button add=primaryIconButton("Add Competition",BLUE_2,R.drawable.ic_add);',
     'Button add=primaryButton("Add Competition",GREEN);',
     'Home Add Competition button')

# Empty-state Add Competition uses the same plain green treatment.
must('Button a=outlineIconButton("Add Competition",BLUE_2,R.drawable.ic_add);',
     'Button a=primaryButton("Add Competition",GREEN);',
     'Empty-state Add Competition button')

# Competition setup submit button: new competitions use green, edits remain blue.
must('Button save=primaryButton(edit?"Save Changes":"Add Competition",BLUE_2);',
     'Button save=primaryButton(edit?"Save Changes":"Add Competition",edit?BLUE_2:GREEN);',
     'Setup Add Competition color')

# Home competition card: remove both trophy icon and right-arrow text from Open Competition.
must('Button open=primaryIconButton("Open Competition   →",BLUE_2,R.drawable.ic_trophy);',
     'Button open=primaryButton("Open Competition",BLUE_2);',
     'Open Competition button')

SRC.write_text(s, encoding='utf-8')
print('TEST 8 icon-only controls patch applied')
