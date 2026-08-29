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


# TEST 13 identity. Preserve TEST 12 UI while changing result-commit semantics.
s = s.replace('TEST 12', 'TEST 13').replace('bastonero_native_t12', 'bastonero_native_t13')
s = s.replace('// TEST 13 Registration UX + Clean Competition Workspace',
              '// TEST 13 Result Lock Workflow', 1)

# Each competitor/team keeps editable draft values plus a separate official locked snapshot.
old_entry = '''        String[] scores = {"","","","",""};
        double penalty = 0;'''
new_entry = '''        String[] scores = {"","","","",""};
        double penalty = 0;
        boolean hasLockedResult = false;
        boolean resultLocked = false;
        String[] lockedScores = {"","","","",""};
        double lockedPenalty = 0;'''
if old_entry not in s:
    raise SystemExit('TEST 13 Entry fields marker missing')
s = s.replace(old_entry, new_entry, 1)

# Official-result persistence.
replace_method('    private JSONObject compToJson(Competition c)throws JSONException{', '''    private JSONObject compToJson(Competition c)throws JSONException{
        JSONObject o=new JSONObject();
        o.put("id",c.id);o.put("date",c.date);o.put("meet",c.meet);o.put("venue",c.venue);
        o.put("level",c.level);o.put("division",c.division);o.put("event",c.event);o.put("weapon",c.weapon);
        o.put("notes",c.notes);o.put("nextEntryId",c.nextEntryId);o.put("scoringStarted",c.scoringStarted);
        JSONArray es=new JSONArray();
        for(Entry e:c.entries){
            JSONObject j=new JSONObject();
            j.put("id",e.id);j.put("name",e.name);j.put("school",e.school);
            JSONArray ss=new JSONArray();for(String v:e.scores)ss.put(v);j.put("scores",ss);
            j.put("penalty",e.penalty);
            j.put("hasLockedResult",e.hasLockedResult);
            j.put("resultLocked",e.resultLocked);
            JSONArray ls=new JSONArray();for(String v:e.lockedScores)ls.put(v);j.put("lockedScores",ls);
            j.put("lockedPenalty",e.lockedPenalty);
            es.put(j);
        }
        o.put("entries",es);return o;
    }''', 'TEST 13 compToJson')

replace_method('    private Competition compFromJson(JSONObject o)throws JSONException{', '''    private Competition compFromJson(JSONObject o)throws JSONException{
        Competition c=new Competition();
        c.id=o.optLong("id");c.date=o.optString("date");c.meet=o.optString("meet","Intramural Meet");
        c.venue=o.optString("venue");c.level=o.optString("level","Elementary");c.division=o.optString("division","Boys");
        c.event=o.optString("event","Individual");c.weapon=o.optString("weapon","Single Weapon");c.notes=o.optString("notes");
        c.nextEntryId=o.optLong("nextEntryId",1);c.scoringStarted=o.optBoolean("scoringStarted",false);
        JSONArray es=o.optJSONArray("entries");
        if(es!=null)for(int i=0;i<es.length();i++){
            JSONObject j=es.getJSONObject(i);Entry e=new Entry();
            e.id=j.optLong("id");e.name=j.optString("name");e.school=j.optString("school");
            JSONArray ss=j.optJSONArray("scores");if(ss!=null&&ss.length()==5)for(int k=0;k<5;k++)e.scores[k]=ss.optString(k,"");
            e.penalty=j.optDouble("penalty",0);
            e.hasLockedResult=j.optBoolean("hasLockedResult",false);
            e.resultLocked=j.optBoolean("resultLocked",false);
            JSONArray ls=j.optJSONArray("lockedScores");if(ls!=null&&ls.length()==5)for(int k=0;k<5;k++)e.lockedScores[k]=ls.optString(k,"");
            e.lockedPenalty=j.optDouble("lockedPenalty",0);
            c.entries.add(e);
        }
        return c;
    }''', 'TEST 13 compFromJson')

# Draft score calculator and official score calculator are deliberately separate.
replace_method('    private ScoreData scoreData(Entry e){', '''    private ScoreData scoreData(Entry e){
        return scoreDataFor(e.scores,e.penalty);
    }

    private ScoreData lockedScoreData(Entry e){
        if(!e.hasLockedResult)return new ScoreData();
        return scoreDataFor(e.lockedScores,e.lockedPenalty);
    }

    private ScoreData scoreDataFor(String[] values,double penalty){
        ScoreData d=new ScoreData();d.nums=new double[5];
        try{
            for(int i=0;i<5;i++){
                if(values==null||values.length!=5||values[i]==null||values[i].trim().isEmpty())return d;
                double n=Double.parseDouble(values[i]);if(n<7||n>10)return d;d.nums[i]=n;
            }
        }catch(Exception ex){return d;}
        double[] sorted=d.nums.clone();Arrays.sort(sorted);
        d.low=sorted[0];d.high=sorted[4];d.score=sorted[1]+sorted[2]+sorted[3];
        d.penalty=Math.max(0,penalty);d.net=d.score-d.penalty;
        for(double n:d.nums)d.fiveTotal+=n;d.complete=true;return d;
    }

    private void commitLockedResult(Entry e){
        for(int i=0;i<5;i++)e.lockedScores[i]=e.scores[i];
        e.lockedPenalty=e.penalty;
        e.hasLockedResult=true;
        e.resultLocked=true;
    }''', 'TEST 13 score calculators')

# Ranking and medals use only the committed official snapshot, never an unlocked draft edit.
replace_method('    private ArrayList<ResultRow> analyze(Competition c){', '''    private ArrayList<ResultRow> analyze(Competition c){
        ArrayList<ResultRow> rows=new ArrayList<>();
        for(Entry e:c.entries){
            ScoreData d=lockedScoreData(e);
            if(d.complete){ResultRow r=new ResultRow();r.entry=e;r.data=d;rows.add(r);}
        }
        rows.sort((a,b)->{int n=Double.compare(b.data.net,a.data.net);return n!=0?n:Double.compare(b.data.fiveTotal,a.data.fiveTotal);});
        String lastExact=null;int lastRank=0;
        for(int i=0;i<rows.size();i++){
            ResultRow x=rows.get(i);String key=String.format(Locale.US,"%.6f|%.6f",x.data.net,x.data.fiveTotal);
            x.rank=key.equals(lastExact)?lastRank:i+1;lastExact=key;lastRank=x.rank;
            int sameFinal=0,sameExact=0;double highestFive=-1;
            for(ResultRow y:rows){if(eq(y.data.net,x.data.net)){sameFinal++;highestFive=Math.max(highestFive,y.data.fiveTotal);if(eq(y.data.fiveTotal,x.data.fiveTotal))sameExact++;}}
            if(sameExact>1){x.status="REPEAT PERFORMANCE";x.accent=RED;x.detail="Final score and 5-judge total are still tied. Repeat performance is required.";}
            else if(sameFinal>1&&eq(x.data.fiveTotal,highestFive)){x.status="TIE-BREAK WINNER";x.accent=BLUE_2;x.detail="Final score tied. Won the tie-break with the higher 5-judge total of "+fmt(x.data.fiveTotal)+".";}
            else if(sameFinal>1){x.status="TIE-BREAK APPLIED";x.accent=BRONZE;x.detail="Final score tied. Ranked by the 5-judge total of "+fmt(x.data.fiveTotal)+".";}
            else{x.status="RANKED";x.accent=GREEN;x.detail="Valid Score "+fmt(x.data.score)+" minus penalty "+fmt1(x.data.penalty)+" gives Final Score "+fmt(x.data.net)+".";}
        }
        return rows;
    }''', 'TEST 13 analyze official results')

# Scored counts mean officially calculated/committed results.
replace_method('    private int completedCount(Competition c){', '''    private int completedCount(Competition c){
        int n=0;for(Entry e:c.entries)if(lockedScoreData(e).complete)n++;return n;
    }''', 'TEST 13 completed count')

# Roster result pill always reflects the last committed official result.
replace_method('    private View rosterRow(Competition c,Entry e,int index){', '''    private View rosterRow(Competition c,Entry e,int index){
        LinearLayout row=surfaceCard();row.setPadding(dp(10),dp(9),dp(10),dp(9));
        LinearLayout top=new LinearLayout(this);top.setOrientation(LinearLayout.HORIZONTAL);top.setGravity(Gravity.CENTER_VERTICAL);
        TextView num=circleNumber(String.valueOf(index+1),BLUE_2);top.addView(num,new LinearLayout.LayoutParams(dp(36),dp(36)));
        LinearLayout info=new LinearLayout(this);info.setOrientation(LinearLayout.VERTICAL);info.setPadding(dp(9),0,0,0);info.addView(text(safeName(e.name),14,WHITE,true));info.addView(text("ID: "+String.format(Locale.US,"%03d",e.id)+(e.school.isEmpty()?"":"  •  "+e.school),10,MUTED,false));top.addView(info,new LinearLayout.LayoutParams(0,-2,1f));
        ScoreData official=lockedScoreData(e);TextView score=pill(official.complete?fmt(official.net):(c.scoringStarted?"PENDING":"REGISTERED"),Color.WHITE,official.complete?GREEN:Color.rgb(65,82,105));top.addView(score);row.addView(top);
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
    }''', 'TEST 13 roster official result')

# Penalty controls are visibly disabled while the result is locked.
replace_method('    private View penaltyBox(Entry e){', '''    private View penaltyBox(Entry e){
        LinearLayout b=surfaceCard();b.setPadding(dp(7),dp(7),dp(7),dp(7));
        TextView l=text("PENALTY",8,MUTED,true);l.setGravity(Gravity.CENTER);b.addView(l);
        LinearLayout ctr=row();ctr.setGravity(Gravity.CENTER);
        Button minus=miniSquare("−",Color.rgb(47,66,91));Button plus=miniSquare("+",BLUE_2);
        TextView v=text(fmt1(e.penalty),13,WHITE,true);v.setGravity(Gravity.CENTER);
        boolean editable=!e.resultLocked;
        minus.setEnabled(editable);plus.setEnabled(editable);minus.setAlpha(editable?1f:.32f);plus.setAlpha(editable?1f:.32f);
        minus.setOnClickListener(x->{if(e.resultLocked)return;e.penalty=Math.max(0,e.penalty-0.5);saveState();refreshAt(e.id);});
        plus.setOnClickListener(x->{if(e.resultLocked)return;e.penalty=Math.min(99,e.penalty+0.5);saveState();refreshAt(e.id);});
        ctr.addView(minus,new LinearLayout.LayoutParams(dp(30),dp(30)));ctr.addView(v,new LinearLayout.LayoutParams(0,dp(30),1f));ctr.addView(plus,new LinearLayout.LayoutParams(dp(30),dp(30)));b.addView(ctr);return b;
    }''', 'TEST 13 locked penalty')

# Judge fields are read-only after Calculate and editable again only after Update Result.
replace_method('    private View judgeCell(Entry e,int idx){', '''    private View judgeCell(Entry e,int idx){
        LinearLayout box=new LinearLayout(this);box.setOrientation(LinearLayout.VERTICAL);
        TextView label=text("J"+(idx+1),10,MUTED,true);label.setGravity(Gravity.CENTER);box.addView(label);
        EditText input=input(e.scores[idx],"—",true);input.setGravity(Gravity.CENTER);input.setTextSize(15);input.setSingleLine(true);input.setSelectAllOnFocus(true);input.setPadding(dp(2),0,dp(2),0);input.setImeOptions(idx<4?EditorInfo.IME_ACTION_NEXT:EditorInfo.IME_ACTION_DONE);styleJudgeInput(input,e.scores[idx]);
        if(e.resultLocked){input.setFocusable(false);input.setFocusableInTouchMode(false);input.setClickable(false);input.setCursorVisible(false);input.setLongClickable(false);input.setAlpha(.72f);}
        input.addTextChangedListener(new SimpleWatcher(){public void afterTextChanged(Editable s){if(e.resultLocked)return;e.scores[idx]=s.toString();styleJudgeInput(input,s.toString());saveState();}});
        input.setOnEditorActionListener((v,action,event)->{if(!e.resultLocked&&idx==4&&(action==EditorInfo.IME_ACTION_DONE||(event!=null&&event.getKeyCode()==KeyEvent.KEYCODE_ENTER))){hideKeyboard();return true;}return false;});
        LinearLayout.LayoutParams p=new LinearLayout.LayoutParams(-1,dp(48));p.setMargins(0,dp(4),0,0);box.addView(input,p);return box;
    }''', 'TEST 13 locked judge fields')

# Calculate commits and locks. Red Update Result only unlocks for correction; it does not change ranking.
replace_method('    private View scoreCard(Competition c,Entry e,int index){', '''    private View scoreCard(Competition c,Entry e,int index){
        LinearLayout card=darkCard();card.setTag("score_"+e.id);
        LinearLayout head=row();head.setGravity(Gravity.CENTER_VERTICAL);
        TextView n=numberCoin(String.valueOf(index+1),BLUE_2);head.addView(n,new LinearLayout.LayoutParams(dp(40),dp(40)));
        LinearLayout info=new LinearLayout(this);info.setOrientation(LinearLayout.VERTICAL);info.setPadding(dp(9),0,0,0);info.addView(text(safeName(e.name),15,WHITE,true));info.addView(text("ID: "+String.format(Locale.US,"%03d",e.id)+(e.school.isEmpty()?"":"  •  "+e.school),10,MUTED,false));head.addView(info,new LinearLayout.LayoutParams(0,-2,1f));
        TextView state=pill(e.resultLocked?"RESULT LOCKED":"EDITING",WHITE,e.resultLocked?GREEN:BLUE_2);head.addView(state);
        card.addView(head);

        LinearLayout judges=row();judges.setPadding(0,dp(12),0,0);for(int i=0;i<5;i++){LinearLayout.LayoutParams p=weight();if(i>0)p.setMargins(dp(5),0,0,0);judges.addView(judgeCell(e,i),p);}card.addView(judges);

        ScoreData draft=scoreData(e);
        LinearLayout metrics=row();metrics.setPadding(0,dp(11),0,0);
        metrics.addView(metricBox("REMOVED H/L",draft.complete?fmt1(draft.high)+" / "+fmt1(draft.low):"—",MUTED),weight());
        LinearLayout.LayoutParams m2=weight();m2.setMargins(dp(6),0,0,0);metrics.addView(metricBox("VALID SCORE",draft.complete?fmt(draft.score):"—",GOLD_2),m2);
        LinearLayout.LayoutParams m3=weight();m3.setMargins(dp(6),0,0,0);metrics.addView(penaltyBox(e),m3);card.addView(metrics);

        if(e.hasLockedResult&&!e.resultLocked){
            ScoreData official=lockedScoreData(e);
            TextView note=text("Official ranking still uses locked Final Score "+fmt(official.net)+" until Calculate is pressed.",9,MUTED,false);note.setGravity(Gravity.CENTER);note.setPadding(dp(4),dp(8),dp(4),0);card.addView(note);
        }

        Button action=primaryButton(e.resultLocked?"Update Result":"Calculate",e.resultLocked?RED:BLUE_2);
        action.setOnClickListener(v->{
            hideKeyboard();
            if(e.resultLocked){
                e.resultLocked=false;saveState();refreshAt(e.id);return;
            }
            if(hasInvalidScore(e)){toast("Judge scores must be between 7.0 and 10.0");return;}
            ScoreData check=scoreData(e);
            if(!check.complete){toast("Enter all five judge scores before calculating");return;}
            commitLockedResult(e);saveState();toast("Result calculated and locked");refreshAt(e.id);
        });
        card.addView(action,fullMargins(0,dp(11),0,0,dp(50)));
        return card;
    }''', 'TEST 13 result-lock score card')

SRC.write_text(s,encoding='utf-8')
print('TEST 13 result lock workflow applied')
