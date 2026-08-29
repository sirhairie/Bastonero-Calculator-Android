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


# TEST 12 identity. Preserve TEST 11 scoring, ranking, dropdowns, and data behavior.
s = s.replace('TEST 11', 'TEST 12').replace('bastonero_native_t11', 'bastonero_native_t12')
s = s.replace('// TEST 12 Icon Actions + Premium Registration Dialog',
              '// TEST 12 Registration UX + Clean Competition Workspace', 1)

# Workspace title: remove both the left back-arrow and crossed-sticks decoration only on the
# competition workspace. Ranking keeps its back navigation.
s = s.replace('addScreenHeader(c.meet,c.scoringStarted?"Scoring phase":"Registration phase",true);',
              'addScreenHeader(c.meet,c.scoringStarted?"Scoring phase":"Registration phase",false);', 1)

replace_method('    private void addScreenHeader(String title,String subtitle,boolean back){', '''    private void addScreenHeader(String title,String subtitle,boolean back){
        LinearLayout r=row();r.setGravity(Gravity.CENTER_VERTICAL);
        if(back){
            ImageButton b=iconOnlyButton(R.drawable.ic_back,WHITE,LINE);
            b.setOnClickListener(v->{
                if(screen==Screen.RANKING)showWorkspace();
                else if(screen==Screen.WORKSPACE)showHome();
                else if(screen==Screen.SETUP&&editingCompetition!=null){activeCompetition=editingCompetition;editingCompetition=null;showWorkspace();}
                else showHome();
            });
            r.addView(b,new LinearLayout.LayoutParams(dp(42),dp(42)));
        }
        LinearLayout words=new LinearLayout(this);words.setOrientation(LinearLayout.VERTICAL);words.setPadding(back?dp(9):0,0,0,0);
        words.addView(text(title,21,WHITE,true));words.addView(text(subtitle,10,MUTED,false));
        r.addView(words,new LinearLayout.LayoutParams(0,-2,1f));
        if(screen!=Screen.WORKSPACE){
            ImageView sticks=iconView(R.drawable.ic_sticks,GOLD,34);sticks.setAlpha(.38f);r.addView(sticks,new LinearLayout.LayoutParams(dp(34),dp(34)));
        }
        content.addView(r,fullMargins(0,0,0,dp(12)));
    }''', 'TEST 12 clean workspace header')

# Competition summary: venue gets its own line directly under the date. Edit becomes green.
replace_method('    private View summaryCard(Competition c){', '''    private View summaryCard(Competition c){
        LinearLayout card=darkCard();
        LinearLayout top=row();top.setGravity(Gravity.CENTER_VERTICAL);
        top.addView(iconSquareView(R.drawable.ic_calendar,BLUE_2,46),new LinearLayout.LayoutParams(dp(46),dp(46)));
        LinearLayout words=new LinearLayout(this);words.setOrientation(LinearLayout.VERTICAL);words.setPadding(dp(10),0,0,0);
        words.addView(text(c.date.isEmpty()?"No date":c.date,13,WHITE,true));
        if(!c.venue.isEmpty())words.addView(text(c.venue,11,WHITE,true));
        words.addView(text("Tournament scoring workspace",10,MUTED,false));
        top.addView(words,new LinearLayout.LayoutParams(0,-2,1f));
        top.addView(pill(c.scoringStarted?"SCORING":"REGISTERING",Color.WHITE,c.scoringStarted?RED:Color.rgb(62,78,101)));
        card.addView(top);
        View sep=divider();LinearLayout.LayoutParams sepP=new LinearLayout.LayoutParams(-1,dp(1));sepP.setMargins(0,dp(11),0,dp(10));card.addView(sep,sepP);
        LinearLayout r1=row();r1.addView(metaIconBox(R.drawable.ic_level,"LEVEL",c.level),weight());LinearLayout.LayoutParams a=weight();a.setMargins(dp(8),0,0,0);r1.addView(metaIconBox(isTeam(c)?R.drawable.ic_group:R.drawable.ic_person,"TYPE",isTeam(c)?"Team":"Individual"),a);card.addView(r1);
        LinearLayout r2=row();r2.setPadding(0,dp(8),0,0);r2.addView(metaIconBox(R.drawable.ic_group,"DIVISION",c.division),weight());LinearLayout.LayoutParams b=weight();b.setMargins(dp(8),0,0,0);r2.addView(metaIconBox(R.drawable.ic_sticks,"ANYO / WEAPON",c.weapon),b);card.addView(r2);
        LinearLayout actions=row();actions.setPadding(0,dp(12),0,0);
        LinearLayout edit=iconActionButton(R.drawable.ic_edit,GREEN);edit.setContentDescription("Edit Competition");edit.setOnClickListener(v->{editingCompetition=c;showSetup();});
        LinearLayout del=iconActionButton(R.drawable.ic_delete,RED);del.setContentDescription("Delete Competition");del.setOnClickListener(v->confirmDeleteCompetition(c));
        actions.addView(edit,new LinearLayout.LayoutParams(0,dp(46),1f));
        LinearLayout.LayoutParams d=new LinearLayout.LayoutParams(0,dp(46),1f);d.setMargins(dp(8),0,0,0);actions.addView(del,d);card.addView(actions);
        return card;
    }''', 'TEST 12 summary card')

# Registration panel: remove arrow from Proceed to Judge Scoring. Keep centered vector +.
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
            Button proceed=primaryButton("Proceed to Judge Scoring",BLUE_2);proceed.setEnabled(!c.entries.isEmpty());proceed.setAlpha(c.entries.isEmpty()?0.45f:1f);proceed.setOnClickListener(v->{if(c.entries.isEmpty())return;c.scoringStarted=true;saveState();showWorkspace();});panel.addView(proceed,fullMargins(0,dp(10),0,0,dp(48)));
        }
        return panel;
    }''', 'TEST 12 registration panel')

# Team/competitor row: numbered circle becomes blue and Edit becomes green.
replace_method('    private View rosterRow(Competition c,Entry e,int index){', '''    private View rosterRow(Competition c,Entry e,int index){
        LinearLayout row=surfaceCard();row.setPadding(dp(10),dp(9),dp(10),dp(9));
        LinearLayout top=new LinearLayout(this);top.setOrientation(LinearLayout.HORIZONTAL);top.setGravity(Gravity.CENTER_VERTICAL);
        TextView num=circleNumber(String.valueOf(index+1),BLUE_2);top.addView(num,new LinearLayout.LayoutParams(dp(36),dp(36)));
        LinearLayout info=new LinearLayout(this);info.setOrientation(LinearLayout.VERTICAL);info.setPadding(dp(9),0,0,0);info.addView(text(safeName(e.name),14,WHITE,true));info.addView(text("ID: "+String.format(Locale.US,"%03d",e.id)+(e.school.isEmpty()?"":"  •  "+e.school),10,MUTED,false));top.addView(info,new LinearLayout.LayoutParams(0,-2,1f));
        ScoreData d=scoreData(e);TextView score=pill(d.complete?fmt(d.net):(c.scoringStarted?"PENDING":"REGISTERED"),Color.WHITE,d.complete?GREEN:Color.rgb(65,82,105));top.addView(score);row.addView(top);
        if(c.scoringStarted){
            row.setClickable(true);row.setOnClickListener(v->jumpToScore(e.id));
        }else{
            LinearLayout actions=new LinearLayout(this);actions.setOrientation(LinearLayout.HORIZONTAL);actions.setPadding(0,dp(8),0,0);
            LinearLayout edit=iconActionButton(R.drawable.ic_edit,GREEN);edit.setContentDescription("Edit "+entryLabel(c));edit.setOnClickListener(v->openEntryDialog(c,e));
            LinearLayout remove=iconActionButton(R.drawable.ic_delete,RED);remove.setContentDescription("Remove "+entryLabel(c));remove.setOnClickListener(v->confirmDeleteEntry(c,e));
            actions.addView(edit,new LinearLayout.LayoutParams(0,dp(42),1f));
            LinearLayout.LayoutParams rp=new LinearLayout.LayoutParams(0,dp(42),1f);rp.setMargins(dp(7),0,0,0);actions.addView(remove,rp);row.addView(actions);
        }
        return row;
    }''', 'TEST 12 roster row')

# Add/Edit competitor/team dialog: centered heading, no duplicate field labels, Add/Save on left,
# filled red Cancel on right.
replace_method('    private void openEntryDialog(Competition c,Entry target){', '''    private void openEntryDialog(Competition c,Entry target){
        boolean edit=target!=null;
        Entry e=edit?target:new Entry();
        final Dialog d=new Dialog(this);
        d.requestWindowFeature(Window.FEATURE_NO_TITLE);

        LinearLayout panel=darkCard(GOLD);panel.setPadding(dp(16),dp(16),dp(16),dp(16));
        TextView title=text((edit?"Edit ":"Add ")+entryLabel(c),20,WHITE,true);title.setGravity(Gravity.CENTER);panel.addView(title);
        TextView sub=text(edit?"Update registration details":"Register a new "+entryLabel(c).toLowerCase(),10,MUTED,false);sub.setGravity(Gravity.CENTER);sub.setPadding(0,dp(3),0,dp(14));panel.addView(sub);

        EditText name=input(e.name,isTeam(c)?"Team name":"Competitor name",false);
        EditText school=input(e.school,"School / Delegation",false);
        LinearLayout.LayoutParams np=new LinearLayout.LayoutParams(-1,dp(50));np.setMargins(0,0,0,dp(10));panel.addView(name,np);
        LinearLayout.LayoutParams scp=new LinearLayout.LayoutParams(-1,dp(50));scp.setMargins(0,0,0,dp(14));panel.addView(school,scp);

        LinearLayout actions=row();
        Button save=primaryButton(edit?"Save":"Add",GREEN);
        save.setOnClickListener(v->{
            String n=name.getText().toString().trim();
            if(n.isEmpty()){name.setError("Required");return;}
            e.name=n;e.school=school.getText().toString().trim();
            if(!edit){e.id=c.nextEntryId++;c.entries.add(e);}
            saveState();d.dismiss();showWorkspace();
        });
        Button cancel=primaryButton("Cancel",RED);cancel.setOnClickListener(v->d.dismiss());
        actions.addView(save,new LinearLayout.LayoutParams(0,dp(46),1f));
        LinearLayout.LayoutParams cp=new LinearLayout.LayoutParams(0,dp(46),1f);cp.setMargins(dp(8),0,0,0);actions.addView(cancel,cp);panel.addView(actions);

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
    }''', 'TEST 12 registration dialog')

# Scoring action: plain text buttons. New score uses Calculate; completed score uses Update Result.
replace_method('    private View scoreCard(Competition c,Entry e,int index){', '''    private View scoreCard(Competition c,Entry e,int index){
        LinearLayout card=darkCard();card.setTag("score_"+e.id);
        LinearLayout head=row();head.setGravity(Gravity.CENTER_VERTICAL);
        TextView n=numberCoin(String.valueOf(index+1),BLUE_2);head.addView(n,new LinearLayout.LayoutParams(dp(40),dp(40)));
        LinearLayout info=new LinearLayout(this);info.setOrientation(LinearLayout.VERTICAL);info.setPadding(dp(9),0,0,0);info.addView(text(safeName(e.name),15,WHITE,true));info.addView(text("ID: "+String.format(Locale.US,"%03d",e.id)+(e.school.isEmpty()?"":"  •  "+e.school),10,MUTED,false));head.addView(info,new LinearLayout.LayoutParams(0,-2,1f));
        ImageView sticks=iconView(R.drawable.ic_sticks,GOLD,34);sticks.setAlpha(.38f);head.addView(sticks,new LinearLayout.LayoutParams(dp(34),dp(34)));card.addView(head);
        LinearLayout judges=row();judges.setPadding(0,dp(12),0,0);for(int i=0;i<5;i++){LinearLayout.LayoutParams p=weight();if(i>0)p.setMargins(dp(5),0,0,0);judges.addView(judgeCell(e,i),p);}card.addView(judges);
        ScoreData d=scoreData(e);LinearLayout metrics=row();metrics.setPadding(0,dp(11),0,0);metrics.addView(metricBox("REMOVED H/L",d.complete?fmt1(d.high)+" / "+fmt1(d.low):"—",MUTED),weight());LinearLayout.LayoutParams m2=weight();m2.setMargins(dp(6),0,0,0);metrics.addView(metricBox("VALID SCORE",d.complete?fmt(d.score):"—",GOLD_2),m2);LinearLayout.LayoutParams m3=weight();m3.setMargins(dp(6),0,0,0);metrics.addView(penaltyBox(e),m3);card.addView(metrics);
        Button update=primaryButton(d.complete?"Update Result":"Calculate",BLUE_2);update.setOnClickListener(v->{hideKeyboard();if(hasInvalidScore(e)){toast("Judge scores must be between 7.0 and 10.0");return;}refreshAt(e.id);});card.addView(update,fullMargins(0,dp(11),0,0,dp(50)));
        return card;
    }''', 'TEST 12 score action')

SRC.write_text(s,encoding='utf-8')
print('TEST 12 registration UX and clean competition workspace applied')
