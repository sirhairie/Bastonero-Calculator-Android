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
    escape = False
    in_char = False
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


# TEST 10 identity. Preserve TEST 9 competition/scoring behavior.
s = s.replace('TEST 9', 'TEST 10').replace('bastonero_native_t9', 'bastonero_native_t10')
s = s.replace('public class MainActivity extends Activity {',
              'public class MainActivity extends Activity {\n    // TEST 10 Unified Dropdowns + Centered Competition Information Header', 1)

# Center Competition Information title, subtitle, and gold underline.
old = '''        LinearLayout heading=new LinearLayout(this);heading.setOrientation(LinearLayout.VERTICAL);heading.setPadding(dp(2),dp(3),dp(2),dp(12));
        TextView ht=text(edit?"Edit Competition":"Competition Information",21,WHITE,true);heading.addView(ht);
        TextView hs=text(edit?"Update the competition details below":"Create the event before registration",10,MUTED,false);hs.setPadding(0,dp(3),0,dp(8));heading.addView(hs);
        View goldLine=new View(this);goldLine.setBackgroundColor(GOLD_2);heading.addView(goldLine,new LinearLayout.LayoutParams(dp(58),dp(3)));'''
new = '''        LinearLayout heading=new LinearLayout(this);heading.setOrientation(LinearLayout.VERTICAL);heading.setGravity(Gravity.CENTER_HORIZONTAL);heading.setPadding(dp(2),dp(3),dp(2),dp(12));
        TextView ht=text(edit?"Edit Competition":"Competition Information",21,WHITE,true);ht.setGravity(Gravity.CENTER);heading.addView(ht);
        TextView hs=text(edit?"Update the competition details below":"Create the event before registration",10,MUTED,false);hs.setGravity(Gravity.CENTER);hs.setPadding(0,dp(3),0,dp(8));heading.addView(hs);
        View goldLine=new View(this);goldLine.setBackgroundColor(GOLD_2);heading.addView(goldLine,new LinearLayout.LayoutParams(dp(58),dp(3)));'''
if old not in s:
    raise SystemExit('TEST 10 setup heading block not found')
s = s.replace(old, new, 1)

# Unified selector implementation. A custom PopupWindow is used for every Spinner so Android's
# default white dropdown can never appear. The popup reads the Spinner's current adapter, which
# also fixes dynamically repopulated Competition Type / Division / Anyo Category choices.
replace_method('    private Spinner spinner(String[] values,String selected){', '''    private Spinner spinner(String[] values,String selected){
        final Spinner sp=new Spinner(this,Spinner.MODE_DROPDOWN);
        applyPremiumSpinnerItems(sp,values,selected);
        sp.setBackground(gloss(Color.rgb(21,65,105),CARD_2,Color.rgb(4,27,51),dp(12),Color.rgb(68,109,148)));
        sp.setPadding(dp(2),0,dp(2),0);elevate(sp,2);
        sp.setOnTouchListener((v,e)->{
            if(e.getAction()==MotionEvent.ACTION_UP)showPremiumSpinnerPopup(sp);
            return true;
        });
        return sp;
    }

    private void applyPremiumSpinnerItems(final Spinner sp,String[] values,String selected){
        ArrayAdapter<String> adapter=new ArrayAdapter<String>(this,android.R.layout.simple_spinner_item,values){
            @Override public View getView(int position,View convertView,ViewGroup parent){
                TextView t=new TextView(MainActivity.this);
                t.setText(getItem(position)+"   ▾");
                t.setTextColor(WHITE);t.setTextSize(12);t.setGravity(Gravity.CENTER_VERTICAL);
                t.setPadding(dp(12),0,dp(10),0);t.setSingleLine(true);
                return t;
            }
            @Override public View getDropDownView(int position,View convertView,ViewGroup parent){
                TextView t=new TextView(MainActivity.this);
                t.setText(getItem(position));t.setTextColor(WHITE);t.setTextSize(12);
                t.setGravity(Gravity.CENTER_VERTICAL);t.setPadding(dp(14),0,dp(12),0);
                t.setBackground(round(CARD_2,dp(8),LINE_SOFT));t.setMinHeight(dp(44));
                return t;
            }
        };
        sp.setAdapter(adapter);
        boolean found=false;
        for(int i=0;i<values.length;i++)if(values[i].equals(selected)){sp.setSelection(i);found=true;break;}
        if(!found&&values.length>0)sp.setSelection(0);
    }

    private void showPremiumSpinnerPopup(final Spinner sp){
        SpinnerAdapter adapter=sp.getAdapter();
        if(adapter==null||adapter.getCount()==0)return;

        LinearLayout list=new LinearLayout(this);list.setOrientation(LinearLayout.VERTICAL);
        list.setPadding(dp(6),dp(6),dp(6),dp(6));
        final PopupWindow popup=new PopupWindow(this);

        for(int i=0;i<adapter.getCount();i++){
            final int index=i;
            String value=String.valueOf(adapter.getItem(i));
            boolean chosen=index==sp.getSelectedItemPosition();
            TextView option=text(value,12,chosen?GOLD_LIGHT:WHITE,chosen);
            option.setGravity(Gravity.CENTER_VERTICAL);option.setPadding(dp(14),0,dp(12),0);
            option.setSingleLine(true);
            option.setBackground(chosen
                ?gloss(Color.rgb(34,79,120),Color.rgb(20,57,94),CARD_2,dp(9),GOLD_2)
                :round(CARD_2,dp(9),LINE_SOFT));
            LinearLayout.LayoutParams op=new LinearLayout.LayoutParams(-1,dp(44));
            if(i>0)op.setMargins(0,dp(4),0,0);
            list.addView(option,op);
            option.setOnClickListener(v->{sp.setSelection(index);popup.dismiss();});
        }

        ScrollView scroller=new ScrollView(this);scroller.setFillViewport(true);scroller.addView(list);
        scroller.setBackground(round(CARD,dp(12),GOLD));
        popup.setContentView(scroller);
        int width=Math.max(sp.getWidth(),dp(210));
        int natural=dp(12)+(adapter.getCount()*dp(48));
        int maxHeight=dp(300);
        popup.setWidth(width);popup.setHeight(Math.min(natural,maxHeight));
        popup.setBackgroundDrawable(new android.graphics.drawable.ColorDrawable(Color.TRANSPARENT));
        popup.setOutsideTouchable(true);popup.setFocusable(true);popup.setClippingEnabled(true);
        if(Build.VERSION.SDK_INT>=21)popup.setElevation(dp(14));
        popup.showAsDropDown(sp,0,dp(5));
    }''', 'TEST 10 unified premium spinner')

# Any selector whose options are changed dynamically must use the same premium adapter.
replace_method('    private void setSpinnerItems(Spinner s,String[] values,String preferred){', '''    private void setSpinnerItems(Spinner s,String[] values,String preferred){
        String keep=preferred==null?selected(s):preferred;
        applyPremiumSpinnerItems(s,values,keep);
    }''', 'TEST 10 dynamic spinner items')

SRC.write_text(s,encoding='utf-8')
print('TEST 10 unified dropdowns and centered setup header applied')
