from pathlib import Path

SRC = Path('native/app/src/main/java/com/bastonero/calculator/nativeapp/MainActivity.java')
s = SRC.read_text(encoding='utf-8')


def replace_method(signature, new_body, label):
    global s
    start = s.find(signature)
    if start < 0:
        raise SystemExit(f'missing method for {label}: {signature}')
    brace = s.find('{', start)
    if brace < 0:
        raise SystemExit(f'missing opening brace for {label}')
    depth = 0
    end = None
    in_string = False
    in_char = False
    escape = False
    for i in range(brace, len(s)):
        ch = s[i]
        if in_string:
            if escape:
                escape = False
            elif ch == '\\':
                escape = True
            elif ch == '"':
                in_string = False
            continue
        if in_char:
            if escape:
                escape = False
            elif ch == '\\':
                escape = True
            elif ch == "'":
                in_char = False
            continue
        if ch == '"':
            in_string = True
            continue
        if ch == "'":
            in_char = True
            continue
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                end = i + 1
                break
    if end is None:
        raise SystemExit(f'unclosed method for {label}')
    s = s[:start] + new_body.rstrip() + s[end:]


# TEST 25 identity. Preserve TEST 24 portrait result layout and TEST 23 About page.
s = s.replace('TEST 24', 'TEST 25').replace('bastonero_native_t24', 'bastonero_native_t25')
s = s.replace('// TEST 25 Portrait Saved Result Redesign',
              '// TEST 25 Ranking-Matched Medal + 2X HD Result Export', 1)

# Render the existing logical 1080px portrait layout at 2X resolution (2160px wide).
# All Canvas coordinates stay the same, so the approved TEST 24 composition is preserved
# while text, vector medals, lines and cards gain four times the pixel count.
old_bitmap = '''                bmp=Bitmap.createBitmap(width,height,Bitmap.Config.ARGB_8888);
                Canvas cv=new Canvas(bmp);
                Paint p=new Paint(Paint.ANTI_ALIAS_FLAG);'''
new_bitmap = '''                final int exportScale=2;
                bmp=Bitmap.createBitmap(width*exportScale,height*exportScale,Bitmap.Config.ARGB_8888);
                Canvas cv=new Canvas(bmp);
                cv.scale(exportScale,exportScale);
                Paint p=new Paint(Paint.ANTI_ALIAS_FLAG);'''
if old_bitmap not in s:
    raise SystemExit('TEST 25 bitmap export marker missing')
s = s.replace(old_bitmap,new_bitmap,1)

# Match the export medal to the actual Ranking medal design: same ic_medal vector,
# accent tint, rear glow and front number coin proportions used by medalCoin().
replace_method('    private void drawExportMedal(Canvas cv,Paint p,int rank,int accent,float x,float y,float w,float h){', '''    private void drawExportMedal(Canvas cv,Paint p,int rank,int accent,float x,float y,float w,float h){
        float unit=Math.min(w/82f,h/86f);
        float cx=x+w/2f;
        float iconSize=68f*unit;
        float glowR=26f*unit;
        float coinR=17f*unit;
        float iconTop=y+(h-iconSize)/2f;
        float medalCy=y+h/2f+4f*unit;

        // Ranking-style metallic glow behind the medal.
        p.setShadowLayer(9f*unit,0,3f*unit,Color.argb(115,0,0,0));
        p.setColor(mix(accent,WHITE,.34f));
        cv.drawCircle(cx,medalCy,glowR,p);
        p.clearShadowLayer();
        p.setColor(accent);cv.drawCircle(cx,medalCy,glowR-3f*unit,p);

        // Use the same vector medal resource used by the live Ranking screen.
        try{
            Drawable medal=getDrawable(R.drawable.ic_medal);
            if(medal!=null){
                medal=medal.mutate();
                medal.setTint(accent);
                medal.setBounds(Math.round(cx-iconSize/2f),Math.round(iconTop),Math.round(cx+iconSize/2f),Math.round(iconTop+iconSize));
                medal.draw(cv);
            }
        }catch(Exception ignored){}

        // Same front number-coin visual language as medalCoin().
        p.setShadowLayer(7f*unit,0,2f*unit,Color.argb(145,0,0,0));
        p.setColor(GOLD_LIGHT);cv.drawCircle(cx,medalCy,coinR+2f*unit,p);
        p.clearShadowLayer();
        p.setColor(accent);cv.drawCircle(cx,medalCy,coinR,p);
        p.setColor(mix(accent,GOLD_LIGHT,.58f));cv.drawCircle(cx,medalCy,coinR-3f*unit,p);
        p.setStyle(Paint.Style.STROKE);p.setStrokeWidth(1.8f*unit);p.setColor(GOLD_LIGHT);
        cv.drawCircle(cx,medalCy,coinR-3f*unit,p);p.setStyle(Paint.Style.FILL);
        drawText(cv,p,String.valueOf(rank),cx,medalCy+6f*unit,16f*unit,BG,true,Paint.Align.CENTER);
    }''', 'TEST 25 ranking-matched export medal')

SRC.write_text(s,encoding='utf-8')
print('TEST 25 ranking-matched medal and 2X HD result export applied')
