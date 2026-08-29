from pathlib import Path
import re

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


# TEST 11 identity. Preserve all TEST 10 competition/scoring behavior.
s = s.replace('TEST 10', 'TEST 11').replace('bastonero_native_t10', 'bastonero_native_t11')
s = s.replace('// TEST 11 Unified Dropdowns + Centered Competition Information Header',
              '// TEST 11 Icon Actions + Premium Registration Dialog', 1)

# Reusable premium icon-only action control. Filled blue/red surface, centered vector icon.
marker = '    private Button primaryButton(String s,int color){'
if marker not in s:
    raise SystemExit('primaryButton marker missing for TEST 11 icon helper')
helper = '''    private LinearLayout iconActionButton(int iconRes,int fill){
        LinearLayout b=new LinearLayout(this);
        b.setGravity(Gravity.CENTER);
        b.setClickable(true);b.setFocusable(true);
        b.setPadding(0,0,0,0);
        int top=mix(fill,WHITE,.20f);
        int bottom=mix(fill,BG,.30f);
        b.setBackground(gloss(top,fill,bottom,dp(11),mix(fill,WHITE,.28f)));
        elevate(b,5);
        ImageView icon=iconView(iconRes,WHITE,24);
        b.addView(icon,new LinearLayout.LayoutParams(dp(24),dp(24)));
        return b;
    }
'''
s = s.replace(marker, helper + '\n' + marker, 1)

# Competition summary: Edit/Delete become equal-width icon-only filled controls.
replace_method('    private View summaryCard(Competition c){', '''    private View summaryCard(Competition c){
        LinearLayout card=darkCard();
        LinearLayout top=row();top.setGravity(Gravity.CENTER_VERTICAL);top.addView(iconSquareView(R.drawable.ic_calendar,BLUE_2,46),new LinearLayout.LayoutParams(dp(46),dp(46)));
        LinearLayout words=new LinearLayout(this);words.setOrientation(LinearLayout.VERTICAL);words.setPadding(dp(10),0,0,0);words.addView(text((c.date.isEmpty()?"No date":c.date)+(c.venue.isEmpty()?"":"  •  "+c.venue),13,WHITE,true));words.addView(text(c.notes.isEmpty()?"Tournament scoring workspace":c.notes,10,MUTED,false));top.addView(words,new LinearLayout.LayoutParams(0,-2,1f));top.addView(pill(c.scoringStarted?"SCORING":"REGISTERING",Color.WHITE,c.scoringStarted?RED:Color.rgb(62,78,101)));card.addView(top);
        View sep=divider();LinearLayout.LayoutParams sepP=new LinearLayout.LayoutParams(-1,dp(1));sepP.setMargins(0,dp(11),0,dp(10));card.addView(sep,sepP);
        LinearLayout r1=row();r1.addView(metaIconBox(R.drawable.ic_level,"LEVEL",c.level),weight());LinearLayout.LayoutParams a=weight();a.setMargins(dp(8),0,0,0);r1.addView(metaIconBox(isTeam(c)?R.drawable.ic_group:R.drawable.ic_person,"TYPE",isTeam(c)?"Team":"Individual"),a);card.addView(r1);
        LinearLayout r2=row();r2.setPadding(0,dp(8),0,0);r2.addView(metaIconBox(R.drawable.ic_group,"DIVISION",c.division),weight());LinearLayout.LayoutParams b=weight();b.setMargins(dp(8),0,0,0);r2.addView(metaIconBox(R.drawable.ic_sticks,"ANYO / WEAPON",c.weapon),b);card.addView(r2);
        LinearLayout actions=row();actions.setPadding(0,dp(12),0,0);
        LinearLayout edit=iconActionButton(R.drawable.ic_edit,BLUE_2);edit.setContentDescription("Edit Competition");edit.setOnClickListener(v->{editingCompetition=c;showSetup();});
        LinearLayout del=iconActionButton(R.drawable.ic_delete,RED);del.setContentDescription("Delete Competition");del.setOnClickListener(v->confirmDeleteCompetition(c));
        actions.addView(edit,new LinearLayout.LayoutParams(0,dp(46),1f));
        LinearLayout.LayoutParams d=new LinearLayout.LayoutParams(0,dp(46),1f);d.setMargins(dp(8),0,0,0);actions.addView(del,d);card.addView(actions);
        return card;
    }''', 'TEST 11 summary actions')

# Registration panel: perfectly centered vector plus; Edit Registration becomes text-only green.
replace_method('    private View rosterPanel(Competition c){', '''    private View rosterPanel(Competition c){
        LinearLayout panel=darkCard();
        LinearLayout head=row();head.setGravity(Gravity.CENTER_VERTICAL);
        LinearLayout title=new LinearLayout(this);title.setOrientation(LinearLayout.VERTICAL);
        title.addView(text(isTeam(c)?"TEAMS":"COMPETITORS",13,WHITE,true));
        title.addView(text(c.scoringStarted?"Tap a competitor to jump to scoring":"Add all competitors before scoring",10,MUTED,false));
        head.addView(title,new LinearLayout.LayoutParams(0,-2,1f));
        if(!c.scoringStarted){
            LinearLayout add=iconActionButton(R.drawable.ic_add,BLUE_2);add.setContentDescription(isTeam(c)?"Add Team":"Add Competitor");add.setOnClickListener(v->openEntryDialog(c,null));
            head.addView(add,new LinearLayout.LayoutParams(dp(46),dp(46)));
        }
        panel.addView(head);
        if(c.entries.isEmpty()){
            TextView empty=text("No "+entryLabel(c).toLowerCase()+" yet.",12,MUTED,false);empty.setGravity(Gravity.CENTER);empty.setPadding(0,dp(20),0,dp(16));panel.addView(empty);
        }else{
            for(int i=0;i<c.entries.size();i++)panel.addView(rosterRow(c,c.entries.get(i),i),fullMargins(0,dp(8),0,0));
        }
        if(c.scoringStarted){
            Button reopen=primaryButton("Edit Registration",GREEN);reopen.setOnClickListener(v->{c.scoringStarted=false;saveState();toast("Registration reopened");showWorkspace();});panel.addView(reopen,fullMargins(0,dp(10),0,0,dp(46)));
        }else{
            Button proceed=primaryButton("Proceed to Judge Scoring   →",BLUE_2);proceed.setEnabled(!c.entries.isEmpty());proceed.setAlpha(c.entries.isEmpty()?0.45f:1f);proceed.setOnClickListener(v->{if(c.entries.isEmpty())return;c.scoringStarted=true;saveState();showWorkspace();});panel.addView(proceed,fullMargins(0,dp(10),0,0,dp(48)));
        }
        return panel;
    }''', 'TEST 11 registration panel')

# Team/competitor row: Edit/Remove become equal-width icon-only filled controls.
replace_method('    private View rosterRow(Competition c,Entry e,int index){', '''    private View rosterRow(Competition c,Entry e,int index){
        LinearLayout row=surfaceCard();row.setPadding(dp(10),dp(9),dp(10),dp(9));
        LinearLayout top=new LinearLayout(this);top.setOrientation(LinearLayout.HORIZONTAL);top.setGravity(Gravity.CENTER_VERTICAL);
        TextView num=circleNumber(String.valueOf(index+1),MUTED);top.addView(num,new LinearLayout.LayoutParams(dp(36),dp(36)));
        LinearLayout info=new LinearLayout(this);info.setOrientation(LinearLayout.VERTICAL);info.setPadding(dp(9),0,0,0);info.addView(text(safeName(e.name),14,WHITE,true));info.addView(text("ID: "+String.format(Locale.US,"%03d",e.id)+(e.school.isEmpty()?"":"  •  "+e.school),10,MUTED,false));top.addView(info,new LinearLayout.LayoutParams(0,-2,1f));
        ScoreData d=scoreData(e);TextView score=pill(d.complete?fmt(d.net):(c.scoringStarted?"PENDING":"REGISTERED"),Color.WHITE,d.complete?GREEN:Color.rgb(65,82,105));top.addView(score);row.addView(top);
        if(c.scoringStarted){
            row.setClickable(true);row.setOnClickListener(v->jumpToScore(e.id));
        }else{
            LinearLayout actions=new LinearLayout(this);actions.setOrientation(LinearLayout.HORIZONTAL);actions.setPadding(0,dp(8),0,0);
            LinearLayout edit=iconActionButton(R.drawable.ic_edit,BLUE_2);edit.setContentDescription("Edit "+entryLabel(c));edit.setOnClickListener(v->openEntryDialog(c,e));
            LinearLayout remove=iconActionButton(R.drawable.ic_delete,RED);remove.setContentDescription("Remove "+entryLabel(c));remove.setOnClickListener(v->confirmDeleteEntry(c,e));
            actions.addView(edit,new LinearLayout.LayoutParams(0,dp(42),1f));
            LinearLayout.LayoutParams rp=new LinearLayout.LayoutParams(0,dp(42),1f);rp.setMargins(dp(7),0,0,0);actions.addView(remove,rp);row.addView(actions);
        }
        return row;
    }''', 'TEST 11 roster actions')

# Slightly larger J1-J5 labels.
s, count = re.subn(r'TextView label=text\("J"\+\(idx\+1\),\d+,MUTED,true\);',
                   'TextView label=text("J"+(idx+1),10,MUTED,true);', s, count=1)
if count != 1:
    raise SystemExit('TEST 11 judge label size replacement failed')

# Fully custom Bastonero Add/Edit Player/Team dialog. No default gray AlertDialog surface.
replace_method('    private void openEntryDialog(Competition c,Entry target){', '''    private void openEntryDialog(Competition c,Entry target){
        boolean edit=target!=null;
        Entry e=edit?target:new Entry();
        final Dialog d=new Dialog(this);
        d.requestWindowFeature(Window.FEATURE_NO_TITLE);

        LinearLayout panel=darkCard(GOLD);panel.setPadding(dp(16),dp(16),dp(16),dp(16));
        TextView title=text((edit?"Edit ":"Add ")+entryLabel(c),20,WHITE,true);panel.addView(title);
        TextView sub=text(edit?"Update registration details":"Register a new "+entryLabel(c).toLowerCase(),10,MUTED,false);sub.setPadding(0,dp(3),0,dp(13));panel.addView(sub);

        EditText name=input(e.name,isTeam(c)?"Team name":"Competitor name",false);
        EditText school=input(e.school,"School / Delegation",false);
        panel.addView(field(isTeam(c)?"TEAM NAME":"COMPETITOR NAME",name));
        panel.addView(field("SCHOOL / DELEGATION",school));

        LinearLayout actions=row();
        Button cancel=outlineButton("Cancel",RED);cancel.setOnClickListener(v->d.dismiss());
        Button save=primaryButton(edit?"Save":"Add",GREEN);
        save.setOnClickListener(v->{
            String n=name.getText().toString().trim();
            if(n.isEmpty()){name.setError("Required");return;}
            e.name=n;e.school=school.getText().toString().trim();
            if(!edit){e.id=c.nextEntryId++;c.entries.add(e);}
            saveState();d.dismiss();showWorkspace();
        });
        actions.addView(cancel,new LinearLayout.LayoutParams(0,dp(46),1f));
        LinearLayout.LayoutParams sp=new LinearLayout.LayoutParams(0,dp(46),1.25f);sp.setMargins(dp(8),0,0,0);actions.addView(save,sp);panel.addView(actions);

        d.setContentView(panel);d.show();
        Window w=d.getWindow();
        if(w!=null){
            w.setBackgroundDrawable(new android.graphics.drawable.ColorDrawable(Color.TRANSPARENT));
            w.addFlags(WindowManager.LayoutParams.FLAG_DIM_BEHIND);
            WindowManager.LayoutParams lp=w.getAttributes();lp.dimAmount=.78f;w.setAttributes(lp);
            w.setSoftInputMode(WindowManager.LayoutParams.SOFT_INPUT_ADJUST_RESIZE);
            int width=(int)(getResources().getDisplayMetrics().widthPixels*.90f);
            w.setLayout(width,WindowManager.LayoutParams.WRAP_CONTENT);
        }
    }''', 'TEST 11 themed entry dialog')

SRC.write_text(s,encoding='utf-8')
print('TEST 11 icon actions, judge labels, centered add icon, and themed registration dialog applied')
