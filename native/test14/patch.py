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


# TEST 14 identity. Preserve TEST 13 result-lock / official-snapshot semantics.
s = s.replace('TEST 13', 'TEST 14').replace('bastonero_native_t13', 'bastonero_native_t14')
s = s.replace('// TEST 14 Result Lock Workflow',
              '// TEST 14 Official Ranking Board Redesign', 1)

# Workspace ranking action: text-only, blue, no trophy, no arrow, larger label.
replace_method('    private void showWorkspace(){', '''    private void showWorkspace(){
        if(activeCompetition==null){showHome();return;}
        screen=Screen.WORKSPACE;clearContent();Competition c=activeCompetition;
        addScreenHeader(c.meet,c.scoringStarted?"Scoring phase":"Registration phase",false);
        content.addView(summaryCard(c),fullMargins(0,0,0,dp(10)));
        content.addView(workspaceStats(c),fullMargins(0,0,0,dp(10)));
        content.addView(rosterPanel(c),fullMargins(0,0,0,dp(10)));
        if(c.scoringStarted){
            content.addView(scoringGuide(),fullMargins(0,0,0,dp(10)));
            content.addView(scoringPanel(c),fullMargins(0,0,0,dp(10)));
            ArrayList<ResultRow> rows=analyze(c);
            Button ranking=primaryButton("View Ranking",BLUE_2);
            ranking.setTextSize(15);
            ranking.setOnClickListener(v->showRanking());
            ranking.setEnabled(!rows.isEmpty());ranking.setAlpha(rows.isEmpty()?0.45f:1f);
            content.addView(ranking,new LinearLayout.LayoutParams(-1,dp(54)));
        }
        addFooter();
    }''', 'TEST 14 View Ranking action')

# Ranking becomes a clean official-results board: centered gold header, no back/X decorations,
# no prose summary card, and text-only Save / Back controls.
replace_method('    private void showRanking(){', '''    private void showRanking(){
        if(activeCompetition==null){showHome();return;}
        screen=Screen.RANKING;clearContent();Competition c=activeCompetition;
        ArrayList<ResultRow> rows=analyze(c);

        LinearLayout header=new LinearLayout(this);
        header.setOrientation(LinearLayout.VERTICAL);header.setGravity(Gravity.CENTER_HORIZONTAL);
        header.setPadding(0,dp(3),0,dp(14));
        TextView title=text("RANKING",20,BG,true);title.setGravity(Gravity.CENTER);
        title.setPadding(dp(22),0,dp(22),0);
        title.setBackground(gloss(GOLD_LIGHT,GOLD_2,GOLD,dp(13),GOLD_LIGHT));
        elevate(title,7);
        header.addView(title,new LinearLayout.LayoutParams(dp(210),dp(50)));
        TextView meet=text(c.meet,14,WHITE,true);meet.setGravity(Gravity.CENTER);meet.setPadding(0,dp(9),0,0);header.addView(meet);
        String when=(c.date.isEmpty()?"No date":c.date)+(c.venue.isEmpty()?"":"  •  "+c.venue);
        TextView meta=text(when,10,MUTED,false);meta.setGravity(Gravity.CENTER);meta.setPadding(dp(8),dp(3),dp(8),0);header.addView(meta);
        content.addView(header);

        if(rows.isEmpty()){
            content.addView(infoCard("No official results","Calculate and lock at least one competitor/team result before viewing ranking."));
        }else{
            for(ResultRow r:rows)content.addView(rankCard(r),fullMargins(0,0,0,dp(11)));
        }

        Button back=primaryButton("Back to Scoring",BLUE_2);
        back.setTextSize(14);back.setOnClickListener(v->showWorkspace());
        content.addView(back,new LinearLayout.LayoutParams(-1,dp(52)));
        Button save=primaryButton("Save Result",RED);
        save.setTextSize(14);save.setEnabled(!rows.isEmpty());save.setAlpha(rows.isEmpty()?0.45f:1f);
        save.setOnClickListener(v->saveResultImage(c,rows));
        content.addView(save,fullMargins(0,dp(9),0,0,dp(52)));
        addFooter();
    }''', 'TEST 14 ranking screen')

# Structured ranking card. No visible internal ID and no explanatory paragraphs.
replace_method('    private View rankCard(ResultRow r){', '''    private View rankCard(ResultRow r){
        int accent=medalAccent(r);
        LinearLayout card=darkCard(accent);card.setPadding(dp(13),dp(13),dp(13),dp(13));

        LinearLayout top=row();top.setGravity(Gravity.CENTER_VERTICAL);
        FrameLayout medal=medalCoin(r.rank,accent);
        top.addView(medal,new LinearLayout.LayoutParams(dp(88),dp(94)));

        LinearLayout identity=new LinearLayout(this);identity.setOrientation(LinearLayout.VERTICAL);identity.setPadding(dp(10),0,0,0);
        identity.addView(text(safeName(r.entry.name),18,WHITE,true));
        TextView school=text(r.entry.school.isEmpty()?"—":r.entry.school,11,MUTED,false);school.setPadding(0,dp(3),0,dp(6));identity.addView(school);
        TextView medalBadge=pill(shortRemark(r),WHITE,mix(accent,BG,.42f));
        identity.addView(medalBadge,new LinearLayout.LayoutParams(-2,dp(29)));
        top.addView(identity,new LinearLayout.LayoutParams(0,-2,1f));
        card.addView(top);

        View div=divider();LinearLayout.LayoutParams dl=new LinearLayout.LayoutParams(-1,dp(1));dl.setMargins(0,dp(9),0,dp(10));card.addView(div,dl);

        LinearLayout scores=row();
        scores.addView(rankingMetric("VALID SCORE",fmt(r.data.score),r.rank<=3?accent:WHITE),weight());
        LinearLayout.LayoutParams p2=weight();p2.setMargins(dp(6),0,0,0);scores.addView(rankingMetric("PENALTY",fmt1(r.data.penalty),WHITE),p2);
        LinearLayout.LayoutParams p3=weight();p3.setMargins(dp(6),0,0,0);scores.addView(rankingMetric("FINAL SCORE",fmt(r.data.net),r.rank<=3?accent:WHITE),p3);
        card.addView(scores);

        LinearLayout technical=row();technical.setPadding(0,dp(8),0,0);
        technical.addView(rankingDetail("REMOVED HIGH",fmt1(r.data.high)),weight());
        LinearLayout.LayoutParams h2=weight();h2.setMargins(dp(6),0,0,0);technical.addView(rankingDetail("REMOVED LOW",fmt1(r.data.low)),h2);
        if(usesTieBreak(r)){
            LinearLayout.LayoutParams h3=weight();h3.setMargins(dp(6),0,0,0);technical.addView(rankingDetail("5-JUDGE TOTAL",fmt(r.data.fiveTotal)),h3);
        }
        card.addView(technical);

        if("REPEAT PERFORMANCE".equals(r.status)){
            TextView repeat=text("REPEAT PERFORMANCE REQUIRED",11,WHITE,true);repeat.setGravity(Gravity.CENTER);
            repeat.setBackground(gloss(mix(RED,WHITE,.14f),RED,mix(RED,BG,.30f),dp(10),mix(RED,WHITE,.25f)));
            card.addView(repeat,fullMargins(0,dp(9),0,0,dp(38)));
        }else if("TIE-BREAK WINNER".equals(r.status)||"TIE-BREAK APPLIED".equals(r.status)){
            String label="TIE-BREAK WINNER".equals(r.status)?"TIE-BREAK WINNER":"TIE-BREAK APPLIED";
            TextView tie=text(label,10,GOLD_LIGHT,true);tie.setGravity(Gravity.CENTER);
            tie.setBackground(round(Color.rgb(47,57,75),dp(9),GOLD));
            card.addView(tie,fullMargins(0,dp(9),0,0,dp(34)));
        }
        return card;
    }''', 'TEST 14 structured ranking card')

# Dedicated grid cells keep the official result visually structured and compact.
marker='    private View rankStat(String label,String value,int color){'
if marker not in s:
    raise SystemExit('TEST 14 rankStat marker missing')
helpers='''    private View rankingMetric(String label,String value,int color){
        LinearLayout b=surfaceCard();b.setPadding(dp(6),dp(8),dp(6),dp(8));b.setGravity(Gravity.CENTER);
        TextView l=text(label,8,MUTED,true);l.setGravity(Gravity.CENTER);l.setSingleLine(true);
        TextView v=text(value,17,color,true);v.setGravity(Gravity.CENTER);v.setPadding(0,dp(4),0,0);
        b.addView(l);b.addView(v);return b;
    }

    private View rankingDetail(String label,String value){
        LinearLayout b=new LinearLayout(this);b.setOrientation(LinearLayout.VERTICAL);b.setGravity(Gravity.CENTER);
        b.setPadding(dp(5),dp(7),dp(5),dp(7));b.setBackground(round(Color.rgb(8,31,57),dp(9),LINE_SOFT));
        TextView l=text(label,8,MUTED,true);l.setGravity(Gravity.CENTER);l.setSingleLine(true);
        TextView v=text(value,13,WHITE,true);v.setGravity(Gravity.CENTER);v.setPadding(0,dp(3),0,0);
        b.addView(l);b.addView(v);return b;
    }

'''
s=s.replace(marker,helpers+marker,1)

# Fix medal clipping: TEST 6 rendered a 68dp medal inside a 64dp parent in rankCard.
# TEST 14 gives the medal its own larger frame and keeps every child inside that frame.
replace_method('    private FrameLayout medalCoin(int rank,int accent){', '''    private FrameLayout medalCoin(int rank,int accent){
        FrameLayout f=new FrameLayout(this);f.setClipChildren(false);f.setClipToPadding(false);
        View glow=new View(this);glow.setBackground(gloss(mix(accent,WHITE,.34f),accent,mix(accent,BG,.48f),dp(999),mix(accent,WHITE,.46f)));
        FrameLayout.LayoutParams gp=new FrameLayout.LayoutParams(dp(64),dp(64),Gravity.TOP|Gravity.CENTER_HORIZONTAL);gp.topMargin=dp(7);f.addView(glow,gp);elevate(glow,7);
        ImageView medal=iconView(R.drawable.ic_medal,accent,82);
        FrameLayout.LayoutParams mp=new FrameLayout.LayoutParams(dp(82),dp(88),Gravity.TOP|Gravity.CENTER_HORIZONTAL);mp.topMargin=dp(1);f.addView(medal,mp);
        TextView n=text(String.valueOf(rank),17,BG,true);n.setGravity(Gravity.CENTER);n.setBackground(gloss(GOLD_LIGHT,accent,mix(accent,BG,.20f),dp(999),GOLD_LIGHT));
        FrameLayout.LayoutParams np=new FrameLayout.LayoutParams(dp(38),dp(38),Gravity.TOP|Gravity.CENTER_HORIZONTAL);np.topMargin=dp(23);f.addView(n,np);elevate(n,9);elevate(f,10);return f;
    }''', 'TEST 14 unclipped medal')

SRC.write_text(s,encoding='utf-8')
print('TEST 14 official ranking board redesign applied')
