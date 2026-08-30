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


# TEST 16 identity. Preserve TEST 15 balanced header/classic medal and TEST 13 result locking.
s = s.replace('TEST 15', 'TEST 16').replace('bastonero_native_t15', 'bastonero_native_t16')
s = s.replace('// TEST 16 Restored Medal + Balanced Ranking Header',
              '// TEST 16 Ranking Score Grid + Tie Decision Emphasis', 1)

# Ranking cards now use the requested score-table layout:
# row 1 = Removed H&L / Valid Score / Penalty / Final Score
# row 2 = J1..J5, plus a wide golden 5-Judge Total only when tie handling is involved.
replace_method('    private View rankCard(ResultRow r){', '''    private View rankCard(ResultRow r){
        int accent=medalAccent(r);
        boolean tie=usesTieBreak(r);
        boolean repeat="REPEAT PERFORMANCE".equals(r.status);
        LinearLayout card=darkCard(accent);card.setPadding(dp(13),dp(13),dp(13),dp(13));

        LinearLayout top=row();top.setGravity(Gravity.CENTER_VERTICAL);
        FrameLayout medal=medalCoin(r.rank,accent);
        top.addView(medal,new LinearLayout.LayoutParams(dp(82),dp(86)));

        LinearLayout identity=new LinearLayout(this);identity.setOrientation(LinearLayout.VERTICAL);identity.setPadding(dp(10),0,0,0);
        LinearLayout nameRow=row();nameRow.setGravity(Gravity.CENTER_VERTICAL);
        TextView name=text(safeName(r.entry.name),18,WHITE,true);name.setSingleLine(true);name.setEllipsize(TextUtils.TruncateAt.END);
        nameRow.addView(name,new LinearLayout.LayoutParams(0,-2,1f));
        TextView medalBadge=pill(shortRemark(r),WHITE,mix(accent,BG,.42f));medalBadge.setGravity(Gravity.CENTER);
        LinearLayout.LayoutParams bp=new LinearLayout.LayoutParams(-2,dp(31));bp.setMargins(dp(8),0,0,0);nameRow.addView(medalBadge,bp);
        identity.addView(nameRow,new LinearLayout.LayoutParams(-1,-2));
        TextView school=text(r.entry.school.isEmpty()?"—":r.entry.school,11,MUTED,false);school.setPadding(0,dp(4),0,0);identity.addView(school);
        top.addView(identity,new LinearLayout.LayoutParams(0,-2,1f));
        card.addView(top);

        View div=divider();LinearLayout.LayoutParams dl=new LinearLayout.LayoutParams(-1,dp(1));dl.setMargins(0,dp(8),0,dp(10));card.addView(div,dl);

        LinearLayout main=row();
        main.addView(rankingMetric("REMOVED H&L",fmt1(r.data.high)+" | "+fmt1(r.data.low),WHITE),new LinearLayout.LayoutParams(0,dp(62),1f));
        LinearLayout.LayoutParams m2=new LinearLayout.LayoutParams(0,dp(62),1f);m2.setMargins(dp(5),0,0,0);main.addView(rankingMetric("VALID SCORE",fmt(r.data.score),r.rank<=3?accent:WHITE),m2);
        LinearLayout.LayoutParams m3=new LinearLayout.LayoutParams(0,dp(62),1f);m3.setMargins(dp(5),0,0,0);main.addView(rankingMetric("PENALTY",fmt1(r.data.penalty),WHITE),m3);
        LinearLayout.LayoutParams m4=new LinearLayout.LayoutParams(0,dp(62),1f);m4.setMargins(dp(5),0,0,0);main.addView(rankingMetric("FINAL SCORE",fmt(r.data.net),r.rank<=3?accent:WHITE),m4);
        card.addView(main);

        LinearLayout judges=row();judges.setGravity(Gravity.CENTER_VERTICAL);judges.setPadding(0,dp(8),0,0);
        for(int i=0;i<5;i++){
            LinearLayout.LayoutParams jp=new LinearLayout.LayoutParams(0,dp(62),tie?0.62f:1f);
            if(i>0)jp.setMargins(dp(4),0,0,0);
            judges.addView(rankingJudgeBox("J"+(i+1),fmt1(r.data.nums[i])),jp);
        }
        if(tie){
            LinearLayout.LayoutParams totalP=new LinearLayout.LayoutParams(0,dp(62),2.25f);totalP.setMargins(dp(6),0,0,0);
            judges.addView(rankingTieTotalBox(fmt(r.data.fiveTotal)),totalP);
        }
        card.addView(judges);

        if(repeat){
            TextView repeatBar=text("REPEAT PERFORMANCE REQUIRED",11,WHITE,true);repeatBar.setGravity(Gravity.CENTER);
            repeatBar.setBackground(gloss(mix(RED,WHITE,.14f),RED,mix(RED,BG,.30f),dp(10),mix(RED,WHITE,.25f)));
            elevate(repeatBar,4);
            card.addView(repeatBar,fullMargins(0,dp(9),0,0,dp(40)));
        }else if("TIE-BREAK WINNER".equals(r.status)||"TIE-BREAK APPLIED".equals(r.status)){
            String label="TIE-BREAK WINNER".equals(r.status)?"TIE-BREAK WINNER":"TIE-BREAK APPLIED";
            TextView tieBar=text(label,10,GOLD_LIGHT,true);tieBar.setGravity(Gravity.CENTER);
            tieBar.setBackground(gloss(Color.rgb(65,53,25),Color.rgb(47,42,27),Color.rgb(25,29,39),dp(9),GOLD));
            card.addView(tieBar,fullMargins(0,dp(9),0,0,dp(36)));
        }
        return card;
    }''', 'TEST 16 ranking score grid')

# Insert compact judge cells and a wide gold-glow tie-total cell before rankingMetric.
marker='    private View rankingMetric(String label,String value,int color){'
if marker not in s:
    raise SystemExit('TEST 16 rankingMetric marker missing')
helpers='''    private View rankingJudgeBox(String label,String value){
        LinearLayout b=new LinearLayout(this);b.setOrientation(LinearLayout.VERTICAL);b.setGravity(Gravity.CENTER);
        b.setPadding(dp(3),dp(6),dp(3),dp(6));
        b.setBackground(round(Color.rgb(8,31,57),dp(9),LINE_SOFT));
        TextView l=text(label,9,MUTED,true);l.setGravity(Gravity.CENTER);l.setSingleLine(true);
        TextView v=text(value,13,WHITE,true);v.setGravity(Gravity.CENTER);v.setPadding(0,dp(3),0,0);
        b.addView(l);b.addView(v);return b;
    }

    private View rankingTieTotalBox(String value){
        LinearLayout b=new LinearLayout(this);b.setOrientation(LinearLayout.VERTICAL);b.setGravity(Gravity.CENTER);
        b.setPadding(dp(5),dp(5),dp(5),dp(5));
        b.setBackground(gloss(Color.rgb(93,72,20),Color.rgb(48,43,28),Color.rgb(16,30,46),dp(10),GOLD_LIGHT));
        elevate(b,9);
        TextView l=text("5-JUDGE TOTAL SCORE",8,GOLD_LIGHT,true);l.setGravity(Gravity.CENTER);l.setSingleLine(true);
        TextView v=text(value,17,GOLD_2,true);v.setGravity(Gravity.CENTER);v.setPadding(0,dp(3),0,0);
        b.addView(l);b.addView(v);return b;
    }

'''
s=s.replace(marker,helpers+marker,1)

SRC.write_text(s,encoding='utf-8')
print('TEST 16 ranking score grid and tie-decision emphasis applied')
