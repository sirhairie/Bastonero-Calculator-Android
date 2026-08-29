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


# TEST 15 identity. Preserve TEST 14 clean ranking board and TEST 13 result-lock workflow.
s = s.replace('TEST 14', 'TEST 15').replace('bastonero_native_t14', 'bastonero_native_t15')
s = s.replace('// TEST 15 Official Ranking Board Redesign',
              '// TEST 15 Restored Medal + Balanced Ranking Header', 1)

# Balance the result-card header: medal on the left, name/delegation in the middle,
# medal/status badge anchored at the upper-right. This removes the large unused right gap.
replace_method('    private View rankCard(ResultRow r){', '''    private View rankCard(ResultRow r){
        int accent=medalAccent(r);
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
    }''', 'TEST 15 balanced ranking card header')

# Restore the medal rendering used before TEST 14. The older proportions are intentionally
# retained because they read as a real medal with ribbons rather than an oval/egg shape.
# The parent supplied by rankCard is now larger than the 68dp medal, so the old clipping bug
# does not return.
replace_method('    private FrameLayout medalCoin(int rank,int accent){', '''    private FrameLayout medalCoin(int rank,int accent){
        FrameLayout f=new FrameLayout(this);f.setClipChildren(false);f.setClipToPadding(false);
        View glow=new View(this);glow.setBackground(gloss(mix(accent,WHITE,.34f),accent,mix(accent,BG,.48f),dp(999),mix(accent,WHITE,.46f)));
        FrameLayout.LayoutParams gp=new FrameLayout.LayoutParams(dp(52),dp(52),Gravity.CENTER);gp.topMargin=dp(8);f.addView(glow,gp);elevate(glow,7);
        ImageView medal=iconView(R.drawable.ic_medal,accent,68);f.addView(medal,new FrameLayout.LayoutParams(dp(68),dp(68),Gravity.CENTER));
        TextView n=text(String.valueOf(rank),16,BG,true);n.setGravity(Gravity.CENTER);n.setBackground(gloss(GOLD_LIGHT,accent,mix(accent,BG,.20f),dp(999),GOLD_LIGHT));
        FrameLayout.LayoutParams np=new FrameLayout.LayoutParams(dp(34),dp(34),Gravity.CENTER);np.topMargin=dp(9);f.addView(n,np);elevate(n,9);elevate(f,10);return f;
    }''', 'TEST 15 restored classic medal')

SRC.write_text(s,encoding='utf-8')
print('TEST 15 restored medal and balanced ranking header applied')
