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


# TEST 9 identity. Keep all TEST 8 scoring, ranking, and native behavior intact.
s = s.replace('TEST 8', 'TEST 9').replace('bastonero_native_t8', 'bastonero_native_t9')

# Home: one green Add Competition action only. Empty-state duplicate action removed.
replace_method('    private void showHome(){', '''    private void showHome(){
        screen=Screen.HOME; activeCompetition=null; editingCompetition=null; clearContent();
        LinearLayout hero=new LinearLayout(this);hero.setOrientation(LinearLayout.VERTICAL);
        LinearLayout titleLine=row();titleLine.setGravity(Gravity.CENTER_VERTICAL);
        titleLine.addView(text("YOUR COMPETITIONS",12,WHITE,true));
        TextView count=pill(String.valueOf(competitions.size()),WHITE,RED);
        LinearLayout.LayoutParams cp=new LinearLayout.LayoutParams(dp(30),dp(26));cp.setMargins(dp(7),0,0,0);titleLine.addView(count,cp);
        hero.addView(titleLine);
        TextView subtitle=text("Create, open, and manage tournament scoring",9,MUTED,false);subtitle.setPadding(0,dp(3),0,0);hero.addView(subtitle);
        content.addView(hero,fullMargins(0,0,0,dp(12)));

        Button add=primaryButton("Add Competition",GREEN);
        add.setOnClickListener(v->{editingCompetition=null;showSetup();});
        content.addView(add,fullMargins(0,0,0,dp(16),dp(50)));

        if(competitions.isEmpty()){
            LinearLayout empty=darkCard(GOLD);empty.setGravity(Gravity.CENTER);empty.setPadding(dp(16),dp(32),dp(16),dp(32));
            ImageView sticks=iconView(R.drawable.ic_sticks,GOLD,64);sticks.setAlpha(.58f);empty.addView(sticks,new LinearLayout.LayoutParams(dp(64),dp(64)));
            TextView t=text("No competition yet",17,WHITE,true);t.setGravity(Gravity.CENTER);t.setPadding(0,dp(12),0,0);empty.addView(t);
            TextView b=text("Use Add Competition above to create your first event.",11,MUTED,false);b.setGravity(Gravity.CENTER);b.setPadding(dp(8),dp(6),dp(8),dp(4));empty.addView(b);
            content.addView(empty);
        }else{
            for(Competition c:competitions) content.addView(competitionCard(c),fullMargins(0,0,0,dp(12)));
        }
        addFooter();
    }''', 'TEST 9 home')

# Competition Information: clean title only, no back arrow, no crossed-sticks decoration,
# no Notes, no Cancel, and one full-width primary action.
replace_method('    private void showSetup(){', '''    private void showSetup(){
        screen=Screen.SETUP;clearContent();
        boolean edit=editingCompetition!=null;
        Competition src=edit?editingCompetition:new Competition();

        LinearLayout heading=new LinearLayout(this);heading.setOrientation(LinearLayout.VERTICAL);heading.setPadding(dp(2),dp(3),dp(2),dp(12));
        TextView ht=text(edit?"Edit Competition":"Competition Information",21,WHITE,true);heading.addView(ht);
        TextView hs=text(edit?"Update the competition details below":"Create the event before registration",10,MUTED,false);hs.setPadding(0,dp(3),0,dp(8));heading.addView(hs);
        View goldLine=new View(this);goldLine.setBackgroundColor(GOLD_2);heading.addView(goldLine,new LinearLayout.LayoutParams(dp(58),dp(3)));
        content.addView(heading);

        LinearLayout form=darkCard(GOLD);form.setPadding(dp(13),dp(14),dp(13),dp(8));

        EditText date=input(src.date,"Select date",false);
        date.setFocusable(false);date.setClickable(true);
        date.setOnClickListener(v->chooseDate(date));
        form.addView(field("DATE",date));

        Spinner meet=spinner(new String[]{"Intramural Meet","District Meet","Cluster Meet","Provincial Meet","Triangular Meet","Regional Meet","Palarong Pambansa","Other"},src.meet);
        form.addView(field("MEET LEVEL",meet));

        EditText venue=input(src.venue,"Enter venue",false);
        form.addView(field("VENUE",venue));

        Spinner event=spinner(new String[]{"Individual","Synchronized / Team","Synchronized Mixed"},src.event);
        form.addView(field("COMPETITION TYPE",event));

        Spinner division=spinner(new String[]{"Boys","Girls"},src.division);
        form.addView(field("DIVISION",division));

        Spinner weapon=spinner(new String[]{"Single Weapon","Identical Double Weapon","Espada y Daga"},src.weapon);
        form.addView(field("ANYO CATEGORY",weapon));

        Spinner level=spinner(new String[]{"Elementary","Secondary"},src.level);
        form.addView(field("LEVEL",level));

        syncCompetitionSpinners(level,event,division,weapon,src.event,src.division,src.weapon);
        level.setOnItemSelectedListener(new SimpleItemSelected(){public void onItemSelected(AdapterView<?> p,View v,int pos,long id){syncCompetitionSpinners(level,event,division,weapon,null,null,null);}});
        event.setOnItemSelectedListener(new SimpleItemSelected(){public void onItemSelected(AdapterView<?> p,View v,int pos,long id){syncDivisionWeapon(level,event,division,weapon,null,null);}});

        content.addView(form,fullMargins(0,0,0,dp(13)));

        Button save=primaryButton(edit?"Save Changes":"Add Competition",edit?BLUE_2:GREEN);
        save.setOnClickListener(v->{
            Competition c=edit?editingCompetition:new Competition();
            if(!edit)c.id=nextCompetitionId();
            c.date=date.getText().toString().trim();
            c.meet=selected(meet);
            c.venue=venue.getText().toString().trim();
            c.event=selected(event);
            c.division=selected(division);
            c.weapon=selected(weapon);
            c.level=selected(level);
            c.notes="";
            if(!edit)competitions.add(c);
            saveState();activeCompetition=c;editingCompetition=null;
            toast(edit?"Competition updated":"Competition created");
            showWorkspace();
        });
        content.addView(save,new LinearLayout.LayoutParams(-1,dp(54)));
        addFooter();
    }''', 'TEST 9 setup screen')

# Premium field treatment: tighter spacing, luminous label, dark raised input surface.
replace_method('    private LinearLayout field(String label,View input){', '''    private LinearLayout field(String label,View input){
        LinearLayout f=new LinearLayout(this);f.setOrientation(LinearLayout.VERTICAL);
        TextView l=text(label,9,Color.rgb(174,196,222),true);l.setPadding(dp(3),0,0,dp(6));f.addView(l);
        int h=dp(48);
        f.addView(input,new LinearLayout.LayoutParams(-1,h));
        LinearLayout.LayoutParams p=new LinearLayout.LayoutParams(-1,-2);p.setMargins(0,0,0,dp(12));f.setLayoutParams(p);
        return f;
    }''', 'TEST 9 field styling')

# Premium editable/date input styling.
replace_method('    private EditText input(String val,String hint,boolean number){', '''    private EditText input(String val,String hint,boolean number){
        EditText e=new EditText(this);
        e.setText(val==null?"":val);e.setHint(hint);
        e.setTextColor(WHITE);e.setHintTextColor(Color.rgb(104,137,170));e.setTextSize(12);
        e.setPadding(dp(12),dp(6),dp(12),dp(6));
        e.setBackground(gloss(Color.rgb(21,65,105),CARD_2,Color.rgb(4,27,51),dp(12),Color.rgb(68,109,148)));
        elevate(e,2);
        if(number)e.setInputType(android.text.InputType.TYPE_CLASS_NUMBER|android.text.InputType.TYPE_NUMBER_FLAG_DECIMAL);
        return e;
    }''', 'TEST 9 input styling')

# Custom dark native Spinner. This removes the white Android dropdown panel and keeps choices
# consistent with Bastonero's navy/gold visual system.
replace_method('    private Spinner spinner(', '''    private Spinner spinner(String[] values,String selected){
        final Spinner sp=new Spinner(this,Spinner.MODE_DROPDOWN);
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
                t.setText(getItem(position));
                t.setTextSize(13);t.setGravity(Gravity.CENTER_VERTICAL);t.setPadding(dp(16),0,dp(12),0);
                t.setMinHeight(dp(50));
                boolean chosen=position==sp.getSelectedItemPosition();
                t.setTextColor(chosen?GOLD_LIGHT:WHITE);
                t.setBackground(chosen?gloss(Color.rgb(28,72,111),Color.rgb(16,52,88),CARD,dp(8),GOLD):round(CARD_2,dp(8),0));
                return t;
            }
        };
        sp.setAdapter(adapter);
        for(int i=0;i<values.length;i++)if(values[i].equals(selected)){sp.setSelection(i);break;}
        sp.setBackground(gloss(Color.rgb(21,65,105),CARD_2,Color.rgb(4,27,51),dp(12),Color.rgb(68,109,148)));
        sp.setPopupBackgroundDrawable(round(CARD,dp(12),GOLD));
        sp.setDropDownVerticalOffset(dp(5));
        sp.setPadding(dp(2),0,dp(2),0);elevate(sp,2);
        return sp;
    }''', 'TEST 9 spinner styling')

# Dark-theme date picker with existing date pre-selected when available.
replace_method('    private void chooseDate(EditText target){', '''    private void chooseDate(EditText target){
        Calendar cal=Calendar.getInstance();
        String current=target.getText().toString().trim();
        if(current.matches("\\d{4}-\\d{2}-\\d{2}")){
            try{
                String[] p=current.split("-");
                cal.set(Integer.parseInt(p[0]),Integer.parseInt(p[1])-1,Integer.parseInt(p[2]));
            }catch(Exception ignored){}
        }
        DatePickerDialog dlg=new DatePickerDialog(this,AlertDialog.THEME_DEVICE_DEFAULT_DARK,
            (v,y,m,d)->target.setText(String.format(Locale.US,"%04d-%02d-%02d",y,m+1,d)),
            cal.get(Calendar.YEAR),cal.get(Calendar.MONTH),cal.get(Calendar.DAY_OF_MONTH));
        dlg.setTitle("Select Competition Date");
        dlg.setOnShowListener(x->{
            if(dlg.getButton(DatePickerDialog.BUTTON_POSITIVE)!=null)dlg.getButton(DatePickerDialog.BUTTON_POSITIVE).setTextColor(GOLD_2);
            if(dlg.getButton(DatePickerDialog.BUTTON_NEGATIVE)!=null)dlg.getButton(DatePickerDialog.BUTTON_NEGATIVE).setTextColor(Color.rgb(126,170,255));
            Window w=dlg.getWindow();if(w!=null)w.setBackgroundDrawable(round(CARD,dp(14),GOLD));
        });
        dlg.show();
    }''', 'TEST 9 date picker')

SRC.write_text(s,encoding='utf-8')
print('TEST 9 competition setup redesign applied')
