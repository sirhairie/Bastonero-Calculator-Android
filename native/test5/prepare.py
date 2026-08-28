from pathlib import Path
import re

SRC = Path('native/app/src/main/java/com/bastonero/calculator/nativeapp/MainActivity.java')
DRAW = Path('native/app/src/main/res/drawable')
DRAW.mkdir(parents=True, exist_ok=True)
s = SRC.read_text(encoding='utf-8')


def between(start, end, new, label):
    global s
    i = s.find(start)
    if i < 0:
        raise SystemExit(f'missing start for {label}: {start}')
    j = s.find(end, i)
    if j < 0:
        raise SystemExit(f'missing end for {label}: {end}')
    s = s[:i] + new.rstrip() + '\n\n' + s[j:]


def must(old, new, label):
    global s
    if old not in s:
        raise SystemExit(f'missing replacement for {label}')
    s = s.replace(old, new)


# Imports and TEST marker.
must('import android.graphics.drawable.GradientDrawable;', 'import android.graphics.drawable.GradientDrawable;\nimport android.graphics.drawable.Drawable;\nimport android.graphics.drawable.LayerDrawable;', 'drawable imports')
s = s.replace('TEST 4', 'TEST 5').replace('bastonero_native_t4', 'bastonero_native_t5')

# Palette sampled/tuned from the approved dark navy + gold mockup.
s = re.sub(
    r'    private static final int BG = .*?    private static final int LINE_SOFT = .*?;\n',
    '''    private static final int BG = Color.rgb(1,10,24);\n    private static final int NAVY = Color.rgb(3,20,42);\n    private static final int CARD = Color.rgb(7,31,58);\n    private static final int CARD_2 = Color.rgb(9,41,73);\n    private static final int SURFACE = Color.rgb(11,48,84);\n    private static final int BLUE = Color.rgb(0,70,207);\n    private static final int BLUE_2 = Color.rgb(5,101,245);\n    private static final int GOLD = Color.rgb(210,157,49);\n    private static final int GOLD_2 = Color.rgb(244,194,66);\n    private static final int GOLD_LIGHT = Color.rgb(255,226,143);\n    private static final int GREEN = Color.rgb(45,133,61);\n    private static final int RED = Color.rgb(210,30,45);\n    private static final int SILVER = Color.rgb(200,211,225);\n    private static final int BRONZE = Color.rgb(197,102,43);\n    private static final int WHITE = Color.rgb(248,251,255);\n    private static final int TEXT = Color.rgb(235,243,252);\n    private static final int MUTED = Color.rgb(158,181,205);\n    private static final int LINE = Color.rgb(55,85,113);\n    private static final int LINE_SOFT = Color.rgb(34,65,94);\n''', s, count=1, flags=re.S)

between('    private void buildShell() {', '\n    private void clearContent()', '''    private void buildShell() {
        shell = new LinearLayout(this);
        shell.setOrientation(LinearLayout.VERTICAL);
        shell.setBackgroundColor(BG);
        shell.setLayoutParams(new LinearLayout.LayoutParams(-1,-1));
        shell.setOnApplyWindowInsetsListener((v, insets) -> {
            v.setPadding(insets.getSystemWindowInsetLeft(), insets.getSystemWindowInsetTop(), insets.getSystemWindowInsetRight(), insets.getSystemWindowInsetBottom());
            return insets;
        });

        LinearLayout toolbar = new LinearLayout(this);
        toolbar.setOrientation(LinearLayout.HORIZONTAL);
        toolbar.setGravity(Gravity.CENTER_VERTICAL);
        toolbar.setPadding(dp(11),dp(10),dp(9),dp(10));
        toolbar.setBackground(gloss(Color.rgb(8,37,70), NAVY, BG, dp(0), 0));
        elevate(toolbar,5);

        LinearLayout logoPlate = new LinearLayout(this);
        logoPlate.setGravity(Gravity.CENTER);
        logoPlate.setBackground(gloss(Color.rgb(27,54,74), CARD, NAVY, dp(999), GOLD));
        elevate(logoPlate,7);
        ImageView logo = new ImageView(this);
        logo.setImageResource(R.drawable.brand_logo);
        logo.setScaleType(ImageView.ScaleType.FIT_CENTER);
        logoPlate.addView(logo,new LinearLayout.LayoutParams(dp(50),dp(50)));
        toolbar.addView(logoPlate,new LinearLayout.LayoutParams(dp(56),dp(56)));

        LinearLayout brand = new LinearLayout(this);
        brand.setOrientation(LinearLayout.VERTICAL);
        brand.setPadding(dp(9),0,dp(4),0);
        TextView title = text("Bastonero Calculator",17,WHITE,true);
        title.setSingleLine(true); title.setEllipsize(TextUtils.TruncateAt.END);
        brand.addView(title);
        LinearLayout subrow=row();subrow.setGravity(Gravity.CENTER_VERTICAL);
        TextView sub=text("Native Android • TEST 5",9,MUTED,true);subrow.addView(sub);
        TextView ver=pill("v2.0",GOLD_LIGHT,Color.rgb(63,48,15));
        LinearLayout.LayoutParams vp=new LinearLayout.LayoutParams(-2,dp(25));vp.setMargins(dp(7),0,0,0);subrow.addView(ver,vp);
        brand.addView(subrow);
        toolbar.addView(brand,new LinearLayout.LayoutParams(0,-2,1f));

        Button home = primaryIconButton("Home",BLUE_2,R.drawable.ic_home);
        home.setTextSize(9);home.setOnClickListener(v->showHome());
        toolbar.addView(home,new LinearLayout.LayoutParams(dp(62),dp(40)));
        Button about = outlineIconButton("About",GOLD,R.drawable.ic_info);
        about.setTextSize(9);about.setOnClickListener(v->showAbout());
        LinearLayout.LayoutParams ap=new LinearLayout.LayoutParams(dp(66),dp(40));ap.setMargins(dp(6),0,0,0);toolbar.addView(about,ap);
        shell.addView(toolbar,new LinearLayout.LayoutParams(-1,-2));

        scroll = new ScrollView(this);
        scroll.setFillViewport(true);
        scroll.setBackgroundColor(BG);
        content = new LinearLayout(this);
        content.setOrientation(LinearLayout.VERTICAL);
        content.setPadding(dp(12),dp(14),dp(12),dp(26));
        scroll.addView(content,new ScrollView.LayoutParams(-1,-2));
        shell.addView(scroll,new LinearLayout.LayoutParams(-1,0,1f));
        setContentView(shell);
    }''', 'buildShell')

between('    private void showHome(){', '\n    private View competitionCard', '''    private void showHome(){
        screen=Screen.HOME; activeCompetition=null; editingCompetition=null; clearContent();
        LinearLayout hero=row();hero.setGravity(Gravity.CENTER_VERTICAL);hero.addView(sectionHeading("YOUR COMPETITIONS","Create, open, and manage tournament scoring"),new LinearLayout.LayoutParams(0,-2,1f));
        TextView count=pill(String.valueOf(competitions.size()),WHITE,RED);hero.addView(count,new LinearLayout.LayoutParams(dp(32),dp(28)));content.addView(hero,fullMargins(0,0,0,dp(12)));
        Button add=primaryIconButton("Add Competition",BLUE_2,R.drawable.ic_add);add.setOnClickListener(v->{editingCompetition=null;showSetup();});content.addView(add,fullMargins(0,0,0,dp(16),dp(54)));
        if(competitions.isEmpty()){
            LinearLayout empty=darkCard(GOLD);empty.setGravity(Gravity.CENTER);empty.setPadding(dp(16),dp(34),dp(16),dp(34));
            ImageView sticks=iconView(R.drawable.ic_sticks,GOLD,74);sticks.setAlpha(.55f);empty.addView(sticks,new LinearLayout.LayoutParams(dp(74),dp(74)));
            TextView t=text("No competition yet",17,WHITE,true);t.setGravity(Gravity.CENTER);t.setPadding(0,dp(12),0,0);empty.addView(t);
            TextView b=text("Add your first competition to get started.",11,MUTED,false);b.setGravity(Gravity.CENTER);b.setPadding(0,dp(6),0,dp(18));empty.addView(b);
            Button a=outlineIconButton("Add Competition",BLUE_2,R.drawable.ic_add);a.setOnClickListener(v->showSetup());empty.addView(a,new LinearLayout.LayoutParams(dp(225),dp(46)));
            content.addView(empty);
        }else{
            for(Competition c:competitions) content.addView(competitionCard(c),fullMargins(0,0,0,dp(12)));
        }
        addFooter();
    }''', 'showHome')

between('    private View competitionCard(Competition c){', '\n    private void showSetup()', '''    private View competitionCard(Competition c){
        LinearLayout card=darkCard();
        LinearLayout top=row();top.setGravity(Gravity.CENTER_VERTICAL);
        top.addView(iconSquareView(R.drawable.ic_calendar,RED,44),new LinearLayout.LayoutParams(dp(44),dp(44)));
        LinearLayout words=new LinearLayout(this);words.setOrientation(LinearLayout.VERTICAL);words.setPadding(dp(10),0,dp(4),0);
        words.addView(text(c.meet,16,WHITE,true));
        words.addView(text((c.date.isEmpty()?"No date":c.date)+(c.venue.isEmpty()?"":"  •  "+c.venue),10,MUTED,false));
        top.addView(words,new LinearLayout.LayoutParams(0,-2,1f));
        ImageView watermark=iconView(R.drawable.ic_sticks,GOLD,34);watermark.setAlpha(.20f);top.addView(watermark,new LinearLayout.LayoutParams(dp(34),dp(34)));
        TextView phase=pill(c.scoringStarted?"SCORING":"REGISTERING",Color.WHITE,c.scoringStarted?BLUE_2:Color.rgb(62,78,101));LinearLayout.LayoutParams php=new LinearLayout.LayoutParams(-2,dp(29));php.setMargins(dp(6),0,0,0);top.addView(phase,php);card.addView(top);
        View div=divider();LinearLayout.LayoutParams dv=new LinearLayout.LayoutParams(-1,dp(1));dv.setMargins(0,dp(11),0,dp(10));card.addView(div,dv);
        LinearLayout meta1=row();meta1.addView(metaIconBox(R.drawable.ic_level,"LEVEL",c.level),weight());LinearLayout.LayoutParams m2=weight();m2.setMargins(dp(7),0,0,0);meta1.addView(metaIconBox(isTeam(c)?R.drawable.ic_group:R.drawable.ic_person,"TYPE",isTeam(c)?"Team":"Individual"),m2);card.addView(meta1);
        LinearLayout meta2=row();meta2.setPadding(0,dp(7),0,0);meta2.addView(metaIconBox(R.drawable.ic_group,"DIVISION",c.division),weight());LinearLayout.LayoutParams m4=weight();m4.setMargins(dp(7),0,0,0);meta2.addView(metaIconBox(R.drawable.ic_sticks,"ANYO / WEAPON",c.weapon),m4);card.addView(meta2);
        ArrayList<ResultRow> rows=analyze(c);String lead=rows.isEmpty()?"—":fmt(rows.get(0).data.net);
        LinearLayout stats=row();stats.setPadding(0,dp(11),0,dp(11));stats.addView(homeStatIcon(R.drawable.ic_person,String.valueOf(c.entries.size()),isTeam(c)?"Teams":"Competitors"),weight());LinearLayout.LayoutParams s2=weight();s2.setMargins(dp(5),0,0,0);stats.addView(homeStatIcon(R.drawable.ic_check,String.valueOf(completedCount(c)),"Scored"),s2);LinearLayout.LayoutParams s3=weight();s3.setMargins(dp(5),0,0,0);stats.addView(homeStatIcon(R.drawable.ic_trophy,lead,"Leader Score"),s3);card.addView(stats);
        Button open=primaryIconButton("Open Competition   →",BLUE_2,R.drawable.ic_trophy);open.setOnClickListener(v->{activeCompetition=c;showWorkspace();});card.addView(open,new LinearLayout.LayoutParams(-1,dp(50)));
        return card;
    }''', 'competitionCard')

between('    private View summaryCard(Competition c){', '\n    private View workspaceStats', '''    private View summaryCard(Competition c){
        LinearLayout card=darkCard();
        LinearLayout top=row();top.setGravity(Gravity.CENTER_VERTICAL);top.addView(iconSquareView(R.drawable.ic_calendar,BLUE_2,46),new LinearLayout.LayoutParams(dp(46),dp(46)));
        LinearLayout words=new LinearLayout(this);words.setOrientation(LinearLayout.VERTICAL);words.setPadding(dp(10),0,0,0);words.addView(text((c.date.isEmpty()?"No date":c.date)+(c.venue.isEmpty()?"":"  •  "+c.venue),13,WHITE,true));words.addView(text(c.notes.isEmpty()?"Tournament scoring workspace":c.notes,10,MUTED,false));top.addView(words,new LinearLayout.LayoutParams(0,-2,1f));top.addView(pill(c.scoringStarted?"SCORING":"REGISTERING",Color.WHITE,c.scoringStarted?RED:Color.rgb(62,78,101)));card.addView(top);
        View sep=divider();LinearLayout.LayoutParams sepP=new LinearLayout.LayoutParams(-1,dp(1));sepP.setMargins(0,dp(11),0,dp(10));card.addView(sep,sepP);
        LinearLayout r1=row();r1.addView(metaIconBox(R.drawable.ic_level,"LEVEL",c.level),weight());LinearLayout.LayoutParams a=weight();a.setMargins(dp(8),0,0,0);r1.addView(metaIconBox(isTeam(c)?R.drawable.ic_group:R.drawable.ic_person,"TYPE",isTeam(c)?"Team":"Individual"),a);card.addView(r1);
        LinearLayout r2=row();r2.setPadding(0,dp(8),0,0);r2.addView(metaIconBox(R.drawable.ic_group,"DIVISION",c.division),weight());LinearLayout.LayoutParams b=weight();b.setMargins(dp(8),0,0,0);r2.addView(metaIconBox(R.drawable.ic_sticks,"ANYO / WEAPON",c.weapon),b);card.addView(r2);
        LinearLayout actions=row();actions.setPadding(0,dp(12),0,0);Button edit=outlineIconButton("Edit Competition",BLUE_2,R.drawable.ic_edit);edit.setOnClickListener(v->{editingCompetition=c;showSetup();});Button del=outlineIconButton("Delete",RED,R.drawable.ic_delete);del.setOnClickListener(v->confirmDeleteCompetition(c));actions.addView(edit,new LinearLayout.LayoutParams(0,dp(44),1.6f));LinearLayout.LayoutParams d=new LinearLayout.LayoutParams(0,dp(44),0.8f);d.setMargins(dp(8),0,0,0);actions.addView(del,d);card.addView(actions);
        return card;
    }''', 'summaryCard')

between('    private View workspaceStats(Competition c){', '\n    private View rosterPanel', '''    private View workspaceStats(Competition c){
        LinearLayout r=row();ArrayList<ResultRow> rows=analyze(c);String lead=rows.isEmpty()?"—":fmt(rows.get(0).data.net);
        r.addView(statDarkIcon(R.drawable.ic_person,"Competitors",String.valueOf(c.entries.size()),WHITE),weight());
        LinearLayout.LayoutParams a=weight();a.setMargins(dp(7),0,0,0);r.addView(statDarkIcon(R.drawable.ic_check,"Scored",String.valueOf(rows.size()),WHITE),a);
        LinearLayout.LayoutParams b=weight();b.setMargins(dp(7),0,0,0);r.addView(statDarkIcon(R.drawable.ic_trophy,"Leader Score",lead,GOLD_2),b);return r;
    }''', 'workspaceStats')

between('    private View scoringGuide(){', '\n    private View scoringPanel', '''    private View scoringGuide(){
        LinearLayout box=darkCard();box.setPadding(dp(12),dp(11),dp(12),dp(11));LinearLayout top=row();top.setGravity(Gravity.CENTER_VERTICAL);top.addView(iconSquareView(R.drawable.ic_info,Color.rgb(20,54,91),40),new LinearLayout.LayoutParams(dp(40),dp(40)));LinearLayout txt=new LinearLayout(this);txt.setOrientation(LinearLayout.VERTICAL);txt.setPadding(dp(9),0,0,0);txt.addView(text("JUDGES SCORING GUIDE",11,Color.rgb(126,170,255),true));txt.addView(text("Registration is locked. Highest and lowest are removed; the remaining three are summed, then the penalty is subtracted.",10,MUTED,false));top.addView(txt,new LinearLayout.LayoutParams(0,-2,1f));box.addView(top);return box;
    }''', 'scoringGuide')

between('    private View scoreCard(Competition c,Entry e,int index){', '\n    private View penaltyBox', '''    private View scoreCard(Competition c,Entry e,int index){
        LinearLayout card=darkCard();card.setTag("score_"+e.id);LinearLayout head=row();head.setGravity(Gravity.CENTER_VERTICAL);TextView n=numberCoin(String.valueOf(index+1),BLUE_2);head.addView(n,new LinearLayout.LayoutParams(dp(40),dp(40)));LinearLayout info=new LinearLayout(this);info.setOrientation(LinearLayout.VERTICAL);info.setPadding(dp(9),0,0,0);info.addView(text(safeName(e.name),15,WHITE,true));info.addView(text("ID: "+String.format(Locale.US,"%03d",e.id)+(e.school.isEmpty()?"":"  •  "+e.school),10,MUTED,false));head.addView(info,new LinearLayout.LayoutParams(0,-2,1f));ImageView sticks=iconView(R.drawable.ic_sticks,GOLD,34);sticks.setAlpha(.28f);head.addView(sticks,new LinearLayout.LayoutParams(dp(34),dp(34)));card.addView(head);
        LinearLayout judges=row();judges.setPadding(0,dp(12),0,0);for(int i=0;i<5;i++){LinearLayout.LayoutParams p=weight();if(i>0)p.setMargins(dp(5),0,0,0);judges.addView(judgeCell(e,i),p);}card.addView(judges);
        ScoreData d=scoreData(e);LinearLayout metrics=row();metrics.setPadding(0,dp(11),0,0);metrics.addView(metricBox("REMOVED H/L",d.complete?fmt1(d.high)+" / "+fmt1(d.low):"—",MUTED),weight());LinearLayout.LayoutParams m2=weight();m2.setMargins(dp(6),0,0,0);metrics.addView(metricBox("VALID SCORE",d.complete?fmt(d.score):"—",GOLD_2),m2);LinearLayout.LayoutParams m3=weight();m3.setMargins(dp(6),0,0,0);metrics.addView(penaltyBox(e),m3);card.addView(metrics);
        Button update=primaryIconButton(d.complete?"Update Result":"Calculate / Update",BLUE_2,R.drawable.ic_edit);update.setOnClickListener(v->{hideKeyboard();if(hasInvalidScore(e)){toast("Judge scores must be between 7.0 and 10.0");return;}refreshAt(e.id);});card.addView(update,fullMargins(0,dp(11),0,0,dp(50)));return card;
    }''', 'scoreCard')

between('    private void showRanking(){', '\n    private View rankCard', '''    private void showRanking(){
        if(activeCompetition==null){showHome();return;}screen=Screen.RANKING;clearContent();Competition c=activeCompetition;addScreenHeader("Ranking",c.meet,true);ArrayList<ResultRow> rows=analyze(c);
        LinearLayout summary=darkCard(GOLD);LinearLayout sr=row();sr.setGravity(Gravity.CENTER_VERTICAL);sr.addView(iconSquareView(R.drawable.ic_trophy,Color.rgb(24,48,79),42),new LinearLayout.LayoutParams(dp(42),dp(42)));LinearLayout st=new LinearLayout(this);st.setOrientation(LinearLayout.VERTICAL);st.setPadding(dp(9),0,0,0);st.addView(text("RESULTS SUMMARY",11,Color.rgb(132,176,255),true));st.addView(text("Winners ranked after penalties. Final Score determines ranking.",10,MUTED,false));sr.addView(st,new LinearLayout.LayoutParams(0,-2,1f));summary.addView(sr);content.addView(summary,fullMargins(0,0,0,dp(10)));
        if(rows.isEmpty()){content.addView(infoCard("No completed scores","Return to scoring and complete all five judge scores."));}else{for(ResultRow r:rows)content.addView(rankCard(r),fullMargins(0,0,0,dp(10)));}
        LinearLayout tie=darkCard();LinearLayout tr=row();tr.setGravity(Gravity.CENTER_VERTICAL);tr.addView(iconView(R.drawable.ic_info,Color.rgb(126,170,255),28),new LinearLayout.LayoutParams(dp(28),dp(28)));LinearLayout tt=new LinearLayout(this);tt.setOrientation(LinearLayout.VERTICAL);tt.setPadding(dp(8),0,0,0);tt.addView(text("TIE HANDLING",11,Color.rgb(126,170,255),true));tt.addView(text("Equal Final Scores use the higher 5-judge total. If that is also equal, Repeat Performance is required.",10,MUTED,false));tr.addView(tt,new LinearLayout.LayoutParams(0,-2,1f));tie.addView(tr);content.addView(tie,fullMargins(0,0,0,dp(12)));
        Button save=primaryIconButton("Save Result",RED,R.drawable.ic_save);save.setEnabled(!rows.isEmpty());save.setAlpha(rows.isEmpty()?0.45f:1f);save.setOnClickListener(v->saveResultImage(c,rows));content.addView(save,new LinearLayout.LayoutParams(-1,dp(54)));Button back=outlineIconButton("Back to Scoring",BLUE_2,R.drawable.ic_back);back.setOnClickListener(v->showWorkspace());content.addView(back,fullMargins(0,dp(9),0,0,dp(46)));addFooter();
    }''', 'showRanking')

between('    private View rankCard(ResultRow r){', '\n    private void openEntryDialog', '''    private View rankCard(ResultRow r){
        int accent=medalAccent(r);LinearLayout card=darkCard(accent);LinearLayout top=row();top.setGravity(Gravity.CENTER_VERTICAL);top.addView(medalCoin(r.rank,accent),new LinearLayout.LayoutParams(dp(64),dp(64)));LinearLayout info=new LinearLayout(this);info.setOrientation(LinearLayout.VERTICAL);info.setPadding(dp(9),0,0,0);info.addView(text(safeName(r.entry.name),17,WHITE,true));info.addView(text("ID: "+String.format(Locale.US,"%03d",r.entry.id)+(r.entry.school.isEmpty()?"":"  •  "+r.entry.school),10,MUTED,false));top.addView(info,new LinearLayout.LayoutParams(0,-2,1f));TextView badge=pill(shortRemark(r),WHITE,mix(accent,BG,.45f));top.addView(badge);card.addView(top);
        View div=divider();LinearLayout.LayoutParams dp1=new LinearLayout.LayoutParams(-1,dp(1));dp1.setMargins(0,dp(11),0,dp(10));card.addView(div,dp1);
        LinearLayout metrics=row();metrics.addView(rankStat("Valid Score",fmt(r.data.score),WHITE),weight());LinearLayout.LayoutParams a=weight();a.setMargins(dp(6),0,0,0);metrics.addView(rankStat("Penalty",fmt1(r.data.penalty),WHITE),a);LinearLayout.LayoutParams b=weight();b.setMargins(dp(6),0,0,0);metrics.addView(rankStat("Final Score",fmt(r.data.net),r.rank<=3?accent:WHITE),b);card.addView(metrics);
        TextView removed=text("Removed High / Low     "+fmt1(r.data.high)+" / "+fmt1(r.data.low),10,MUTED,true);removed.setGravity(Gravity.CENTER);removed.setPadding(0,dp(10),0,0);card.addView(removed);if(usesTieBreak(r)){TextView five=text("5-Judge Total     "+fmt(r.data.fiveTotal),10,accent,true);five.setGravity(Gravity.CENTER);five.setPadding(0,dp(5),0,0);card.addView(five);}TextView detail=text(r.detail,10,MUTED,false);detail.setPadding(0,dp(8),0,0);card.addView(detail);return card;
    }''', 'rankCard')

between('    private void showAbout(){', '\n    private void loadState()', '''    private void showAbout(){
        TextView t=text("BASTONERO CALCULATOR — NATIVE ANDROID\\n\\nTEST 5 Premium 3D UI. The app interface and scoring engine use native Android code—no WebView, HTML, CSS, or JavaScript.\\n\\nVisual upgrade\\n• Mockup-matched navy, blue, and gold palette\\n• Custom Arnis and tournament vector icons\\n• Raised gradient cards and beveled controls\\n• Embossed medal-style ranking\\n\\nScoring\\n• Five judges, valid scores 7.0–10.0\\n• Remove highest and lowest\\n• Add the middle three scores\\n• Subtract official penalty\\n• Tied Final Score: use 5-judge total\\n• Still tied: Repeat Performance\\n\\nDeveloper\\nHairie A. Laysam\\nSta. Maria National High School\\n\\nNative v2.0 • TEST 5",13,TEXT,false);t.setPadding(dp(18),dp(8),dp(18),dp(18));t.setMovementMethod(new ScrollingMovementMethod());new AlertDialog.Builder(this).setTitle("About Bastonero Native").setView(t).setPositiveButton("Close",null).show();
    }''', 'showAbout')

between('    private void addScreenHeader(String title,String subtitle,boolean back){', '\n    private View sectionTitle', '''    private void addScreenHeader(String title,String subtitle,boolean back){
        LinearLayout r=row();r.setGravity(Gravity.CENTER_VERTICAL);if(back){ImageButton b=iconOnlyButton(R.drawable.ic_back,WHITE,LINE);b.setOnClickListener(v->{if(screen==Screen.RANKING)showWorkspace();else if(screen==Screen.WORKSPACE)showHome();else if(screen==Screen.SETUP&&editingCompetition!=null){activeCompetition=editingCompetition;editingCompetition=null;showWorkspace();}else showHome();});r.addView(b,new LinearLayout.LayoutParams(dp(42),dp(42)));}LinearLayout words=new LinearLayout(this);words.setOrientation(LinearLayout.VERTICAL);words.setPadding(back?dp(9):0,0,0,0);words.addView(text(title,21,WHITE,true));words.addView(text(subtitle,10,MUTED,false));r.addView(words,new LinearLayout.LayoutParams(0,-2,1f));ImageView sticks=iconView(R.drawable.ic_sticks,GOLD,34);sticks.setAlpha(.25f);r.addView(sticks,new LinearLayout.LayoutParams(dp(34),dp(34)));content.addView(r,fullMargins(0,0,0,dp(12)));
    }''', 'addScreenHeader')

between('    private void addFooter(){', '\n    private LinearLayout row()', '''    private void addFooter(){
        Space gap=new Space(this);content.addView(gap,new LinearLayout.LayoutParams(1,dp(58)));LinearLayout f=row();f.setGravity(Gravity.CENTER);ImageView a=iconView(R.drawable.ic_sticks,GOLD,24);a.setRotation(-12);TextView t=text("Develop by Sir Hairie Laysam",11,MUTED,false);t.setPadding(dp(10),0,dp(10),0);ImageView b=iconView(R.drawable.ic_sticks,GOLD,24);b.setRotation(12);f.addView(a,new LinearLayout.LayoutParams(dp(24),dp(24)));f.addView(t);f.addView(b,new LinearLayout.LayoutParams(dp(24),dp(24)));content.addView(f);
    }''', 'footer')

between('    private LinearLayout row(){', '\n    private TextView text(', '''    private LinearLayout row(){LinearLayout r=new LinearLayout(this);r.setOrientation(LinearLayout.HORIZONTAL);return r;}
    private LinearLayout darkCard(){return darkCard(LINE);}
    private LinearLayout darkCard(int stroke){LinearLayout l=new LinearLayout(this);l.setOrientation(LinearLayout.VERTICAL);l.setPadding(dp(13),dp(13),dp(13),dp(13));l.setBackground(gloss(Color.rgb(14,52,88),CARD,NAVY,dp(16),stroke));elevate(l,6);return l;}
    private LinearLayout surfaceCard(){LinearLayout l=new LinearLayout(this);l.setOrientation(LinearLayout.VERTICAL);l.setBackground(gloss(Color.rgb(18,64,106),SURFACE,CARD_2,dp(12),LINE_SOFT));elevate(l,2);return l;}
    private View divider(){View v=new View(this);v.setBackgroundColor(LINE);v.setAlpha(.75f);return v;}
    private View infoCard(String title,String body){LinearLayout c=darkCard();TextView t=text(title,16,WHITE,true);t.setGravity(Gravity.CENTER);TextView b=text(body,11,MUTED,false);b.setGravity(Gravity.CENTER);b.setPadding(0,dp(6),0,0);c.addView(t);c.addView(b);return c;}
    private LinearLayout sectionHeading(String title,String sub){LinearLayout x=new LinearLayout(this);x.setOrientation(LinearLayout.VERTICAL);x.addView(text(title,12,WHITE,true));TextView s=text(sub,9,MUTED,false);s.setPadding(0,dp(2),0,0);x.addView(s);return x;}
    private View metaBox(String label,String value){return metaIconBox(0,label,value);}
    private View metaIconBox(int iconRes,String label,String value){LinearLayout b=surfaceCard();b.setPadding(dp(9),dp(8),dp(9),dp(8));LinearLayout r=row();r.setGravity(Gravity.CENTER_VERTICAL);if(iconRes!=0)r.addView(iconView(iconRes,GOLD,18),new LinearLayout.LayoutParams(dp(18),dp(18)));LinearLayout txt=new LinearLayout(this);txt.setOrientation(LinearLayout.VERTICAL);txt.setPadding(iconRes!=0?dp(7):0,0,0,0);txt.addView(text(label,8,MUTED,true));TextView v=text(value,11,WHITE,true);v.setPadding(0,dp(2),0,0);txt.addView(v);r.addView(txt,new LinearLayout.LayoutParams(0,-2,1f));b.addView(r);return b;}
    private View metaSimple(String label,String value){LinearLayout b=new LinearLayout(this);b.setOrientation(LinearLayout.VERTICAL);b.addView(text(label,8,MUTED,true));TextView v=text(value,12,WHITE,true);v.setPadding(0,dp(3),0,0);b.addView(v);return b;}
    private View homeStat(String value,String label){return homeStatIcon(0,value,label);}
    private View homeStatIcon(int iconRes,String value,String label){LinearLayout b=new LinearLayout(this);b.setOrientation(LinearLayout.VERTICAL);b.setGravity(Gravity.CENTER);if(iconRes!=0){ImageView i=iconView(iconRes,GOLD,19);b.addView(i,new LinearLayout.LayoutParams(dp(19),dp(19)));}TextView v=text(value,16,WHITE,true);v.setGravity(Gravity.CENTER);v.setPadding(0,dp(2),0,0);TextView l=text(label,8,MUTED,false);l.setGravity(Gravity.CENTER);l.setPadding(0,dp(2),0,0);b.addView(v);b.addView(l);return b;}
    private View statDark(String label,String value,int color){return statDarkIcon(0,label,value,color);}
    private View statDarkIcon(int iconRes,String label,String value,int color){LinearLayout b=darkCard();b.setPadding(dp(8),dp(8),dp(8),dp(8));b.setGravity(Gravity.CENTER);if(iconRes!=0)b.addView(iconView(iconRes,GOLD,19),new LinearLayout.LayoutParams(dp(19),dp(19)));TextView l=text(label,9,MUTED,false);l.setGravity(Gravity.CENTER);TextView v=text(value,17,color,true);v.setGravity(Gravity.CENTER);v.setPadding(0,dp(2),0,0);b.addView(l);b.addView(v);return b;}
    private View metricBox(String label,String value,int color){LinearLayout b=surfaceCard();b.setPadding(dp(7),dp(7),dp(7),dp(7));TextView l=text(label,8,MUTED,true);l.setGravity(Gravity.CENTER);TextView v=text(value,14,color,true);v.setGravity(Gravity.CENTER);v.setPadding(0,dp(4),0,0);b.addView(l);b.addView(v);return b;}
    private View rankStat(String label,String value,int color){LinearLayout b=new LinearLayout(this);b.setOrientation(LinearLayout.VERTICAL);b.setGravity(Gravity.CENTER);TextView l=text(label,9,MUTED,false);l.setGravity(Gravity.CENTER);TextView v=text(value,16,color,true);v.setGravity(Gravity.CENTER);v.setPadding(0,dp(3),0,0);b.addView(l);b.addView(v);return b;}
    private ImageView iconView(int res,int tint,int size){ImageView i=new ImageView(this);i.setImageResource(res);i.setColorFilter(tint);i.setScaleType(ImageView.ScaleType.CENTER_INSIDE);i.setPadding(dp(1),dp(1),dp(1),dp(1));return i;}
    private LinearLayout iconSquareView(int res,int fill,int size){LinearLayout x=new LinearLayout(this);x.setGravity(Gravity.CENTER);x.setBackground(gloss(mix(fill,WHITE,.18f),fill,mix(fill,BG,.28f),dp(11),mix(fill,WHITE,.18f)));elevate(x,5);x.addView(iconView(res,WHITE,size-18),new LinearLayout.LayoutParams(dp(size-18),dp(size-18)));return x;}
    private TextView numberCoin(String value,int accent){TextView t=text(value,14,WHITE,true);t.setGravity(Gravity.CENTER);t.setBackground(gloss(mix(accent,WHITE,.26f),accent,mix(accent,BG,.38f),dp(999),mix(accent,WHITE,.35f)));elevate(t,6);return t;}
    private FrameLayout medalCoin(int rank,int accent){FrameLayout f=new FrameLayout(this);ImageView medal=iconView(R.drawable.ic_medal,accent,64);f.addView(medal,new FrameLayout.LayoutParams(dp(64),dp(64),Gravity.CENTER));TextView n=text(String.valueOf(rank),15,rank==2?BG:Color.rgb(65,37,4),true);n.setGravity(Gravity.CENTER);FrameLayout.LayoutParams np=new FrameLayout.LayoutParams(dp(34),dp(34),Gravity.CENTER);np.topMargin=dp(7);f.addView(n,np);elevate(f,8);return f;}
    private TextView textIconLabel(int res,String s,int tint,int sp){TextView t=text(s,sp,WHITE,true);Drawable d=getDrawable(res);d.setTint(tint);d.setBounds(0,0,dp(18),dp(18));t.setCompoundDrawables(d,null,null,null);t.setCompoundDrawablePadding(dp(6));return t;}
    private GradientDrawable gloss(int top,int mid,int bottom,int radius,int stroke){GradientDrawable g=new GradientDrawable(GradientDrawable.Orientation.TOP_BOTTOM,new int[]{top,mid,bottom});g.setCornerRadius(radius);if(stroke!=0)g.setStroke(dp(1),stroke);return g;}
    private int mix(int a,int b,float t){t=Math.max(0f,Math.min(1f,t));int r=(int)(Color.red(a)*(1-t)+Color.red(b)*t);int g=(int)(Color.green(a)*(1-t)+Color.green(b)*t);int bl=(int)(Color.blue(a)*(1-t)+Color.blue(b)*t);return Color.rgb(r,g,bl);}
    private void elevate(View v,int amount){if(Build.VERSION.SDK_INT>=21){v.setElevation(dp(amount));v.setTranslationZ(dp(Math.max(0,amount/4)));}}
''', 'card helper group')

between('    private Button primaryButton(String s,int color){', '\n    private EditText input(', '''    private Button primaryButton(String s,int color){Button b=new Button(this);b.setAllCaps(false);b.setText(s);b.setTextColor(Color.WHITE);b.setTextSize(12);b.setTypeface(Typeface.DEFAULT,Typeface.BOLD);b.setBackground(gloss(mix(color,WHITE,.22f),color,mix(color,BG,.30f),dp(12),mix(color,WHITE,.22f)));b.setPadding(dp(9),0,dp(9),0);b.setMinWidth(0);b.setMinimumWidth(0);elevate(b,5);return b;}
    private Button primaryIconButton(String s,int color,int res){Button b=primaryButton(s,color);applyButtonIcon(b,res,Color.WHITE);return b;}
    private Button smallButton(String s,int color){Button b=primaryButton(s,color);b.setTextSize(10);return b;}
    private Button outlineButton(String s,int color){Button b=new Button(this);b.setAllCaps(false);b.setText(s);b.setTextColor(color);b.setTextSize(10);b.setTypeface(Typeface.DEFAULT,Typeface.BOLD);b.setBackground(gloss(Color.rgb(18,47,78),CARD,NAVY,dp(11),color));b.setPadding(dp(7),0,dp(7),0);b.setMinWidth(0);b.setMinimumWidth(0);elevate(b,3);return b;}
    private Button outlineIconButton(String s,int color,int res){Button b=outlineButton(s,color);applyButtonIcon(b,res,color);return b;}
    private Button iconButton(String s){Button b=outlineButton(s,LINE);b.setTextColor(WHITE);b.setTextSize(24);b.setPadding(0,0,0,dp(3));return b;}
    private ImageButton iconOnlyButton(int res,int tint,int stroke){ImageButton b=new ImageButton(this);b.setImageResource(res);b.setColorFilter(tint);b.setScaleType(ImageView.ScaleType.CENTER_INSIDE);b.setPadding(dp(10),dp(10),dp(10),dp(10));b.setBackground(gloss(Color.rgb(20,50,82),CARD,NAVY,dp(12),stroke));elevate(b,4);return b;}
    private Button miniSquare(String s,int fill){Button b=primaryButton(s,fill);b.setTextSize(17);b.setPadding(0,0,0,0);return b;}
    private void applyButtonIcon(Button b,int res,int tint){Drawable d=getDrawable(res);d.setTint(tint);d.setBounds(0,0,dp(17),dp(17));b.setCompoundDrawables(d,null,null,null);b.setCompoundDrawablePadding(dp(6));}
''', 'button helpers')

between('    private EditText input(String val,String hint,boolean number){', '\n    private Spinner spinner(', '''    private EditText input(String val,String hint,boolean number){EditText e=new EditText(this);e.setText(val==null?"":val);e.setHint(hint);e.setTextColor(WHITE);e.setHintTextColor(Color.rgb(105,132,158));e.setTextSize(13);e.setPadding(dp(10),dp(8),dp(10),dp(8));e.setBackground(gloss(Color.rgb(18,60,99),CARD_2,Color.rgb(5,29,55),dp(10),LINE));elevate(e,2);if(number)e.setInputType(android.text.InputType.TYPE_CLASS_NUMBER|android.text.InputType.TYPE_NUMBER_FLAG_DECIMAL);return e;}
    private void styleJudgeInput(EditText e,String value){boolean bad=false;String v=value==null?"":value.trim();if(!v.isEmpty()){try{double n=Double.parseDouble(v);bad=n<7||n>10;}catch(Exception ex){bad=true;}}if(bad)e.setBackground(gloss(Color.rgb(104,36,48),Color.rgb(71,22,34),Color.rgb(42,15,24),dp(9),Color.rgb(244,90,113)));else e.setBackground(gloss(Color.rgb(22,70,114),CARD_2,Color.rgb(5,29,55),dp(9),Color.rgb(58,91,124)));}
''', 'input helpers')

# Upgrade visible action buttons that remain in untouched methods.
s = s.replace('Button add=smallButton("＋",BLUE_2);', 'Button add=primaryIconButton("",BLUE_2,R.drawable.ic_add);')
s = s.replace('Button reopen=outlineButton("Edit Registration",BLUE_2);', 'Button reopen=outlineIconButton("Edit Registration",BLUE_2,R.drawable.ic_edit);')
s = s.replace('Button proceed=primaryButton("Proceed to Judge Scoring   →",BLUE_2);', 'Button proceed=primaryIconButton("Proceed to Judge Scoring   →",BLUE_2,R.drawable.ic_arrow_right);')
s = s.replace('Button ranking=primaryButton("View Ranking / Results   →",GOLD);', 'Button ranking=primaryIconButton("View Ranking / Results   →",GOLD,R.drawable.ic_trophy);')
s = s.replace('Button edit=outlineButton("Edit",GREEN);', 'Button edit=outlineIconButton("Edit",GREEN,R.drawable.ic_edit);')
s = s.replace('Button remove=outlineButton("Remove",RED);', 'Button remove=outlineIconButton("Remove",RED,R.drawable.ic_delete);')

# Result-image marker.
s = s.replace('drawText(cv,p,"TEST 5",235,190,21,GOLD_2,true);', 'drawText(cv,p,"TEST 5 • PREMIUM 3D",235,190,21,GOLD_2,true);')

SRC.write_text(s,encoding='utf-8')

# Custom vector icon family used by TEST 5. These are native VectorDrawables, not text glyphs.
icons = {
'ic_home.xml': '''<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24"><path android:fillColor="#FFFFFFFF" android:pathData="M12,3 L2,12 H5 V21 H10 V15 H14 V21 H19 V12 H22 Z"/></vector>''',
'ic_info.xml': '''<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24"><path android:fillColor="#FFFFFFFF" android:pathData="M12,2 C6.48,2 2,6.48 2,12 C2,17.52 6.48,22 12,22 C17.52,22 22,17.52 22,12 C22,6.48 17.52,2 12,2 Z M11,7 H13 V9 H11 Z M11,11 H13 V17 H11 Z"/></vector>''',
'ic_calendar.xml': '''<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24"><path android:fillColor="#FFFFFFFF" android:pathData="M7,2 H9 V4 H15 V2 H17 V4 H19 C20.1,4 21,4.9 21,6 V20 C21,21.1 20.1,22 19,22 H5 C3.9,22 3,21.1 3,20 V6 C3,4.9 3.9,4 5,4 H7 Z M5,9 V20 H19 V9 Z M7,11 H11 V15 H7 Z"/></vector>''',
'ic_level.xml': '''<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24"><path android:fillColor="#FFFFFFFF" android:pathData="M12,3 L1.5,8.5 L12,14 L20,9.8 V16 H22 V8.5 Z M5,12.2 V17.5 C7,19.2 9.3,20 12,20 C14.7,20 17,19.2 19,17.5 V12.2 L12,16 Z"/></vector>''',
'ic_person.xml': '''<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24"><path android:fillColor="#FFFFFFFF" android:pathData="M12,3 C9.79,3 8,4.79 8,7 C8,9.21 9.79,11 12,11 C14.21,11 16,9.21 16,7 C16,4.79 14.21,3 12,3 Z M12,13 C8.67,13 5,14.67 5,17 V21 H19 V17 C19,14.67 15.33,13 12,13 Z"/></vector>''',
'ic_group.xml': '''<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24"><path android:fillColor="#FFFFFFFF" android:pathData="M8,4 C6.07,4 4.5,5.57 4.5,7.5 C4.5,9.43 6.07,11 8,11 C9.93,11 11.5,9.43 11.5,7.5 C11.5,5.57 9.93,4 8,4 Z M16.5,5 C14.84,5 13.5,6.34 13.5,8 C13.5,9.66 14.84,11 16.5,11 C18.16,11 19.5,9.66 19.5,8 C19.5,6.34 18.16,5 16.5,5 Z M8,13 C4.67,13 2,14.67 2,17 V20 H14 V17 C14,14.67 11.33,13 8,13 Z M16.5,13 C15.8,13 15.05,13.08 14.35,13.25 C15.4,14.22 16,15.43 16,17 V20 H22 V17.5 C22,15.13 19.55,13 16.5,13 Z"/></vector>''',
'ic_sticks.xml': '''<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24"><path android:fillColor="#00000000" android:strokeColor="#FFFFFFFF" android:strokeWidth="2.2" android:strokeLineCap="round" android:pathData="M4,20 L20,4"/><path android:fillColor="#00000000" android:strokeColor="#FFFFFFFF" android:strokeWidth="2.2" android:strokeLineCap="round" android:pathData="M4,4 L20,20"/><path android:fillColor="#00000000" android:strokeColor="#FFFFFFFF" android:strokeWidth="1.4" android:pathData="M3,17 L7,21 M17,3 L21,7 M3,7 L7,3 M17,21 L21,17"/></vector>''',
'ic_trophy.xml': '''<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24"><path android:fillColor="#FFFFFFFF" android:pathData="M7,3 H17 V5 H20 C21.1,5 22,5.9 22,7 V8 C22,10.4 20.2,12.4 17.9,12.8 C17.25,14.35 15.8,15.5 14,15.85 V19 H18 V21 H6 V19 H10 V15.85 C8.2,15.5 6.75,14.35 6.1,12.8 C3.8,12.4 2,10.4 2,8 V7 C2,5.9 2.9,5 4,5 H7 Z M4,7 V8 C4,9.25 4.8,10.32 5.92,10.72 C5.87,10.38 5.84,10.04 5.84,9.68 V7 Z M18.16,7 V9.68 C18.16,10.04 18.13,10.38 18.08,10.72 C19.2,10.32 20,9.25 20,8 V7 Z"/></vector>''',
'ic_edit.xml': '''<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24"><path android:fillColor="#FFFFFFFF" android:pathData="M3,17.25 V21 H6.75 L17.81,9.94 L14.06,6.19 Z M20.71,7.04 C21.1,6.65 21.1,6.02 20.71,5.63 L18.37,3.29 C17.98,2.9 17.35,2.9 16.96,3.29 L15.13,5.12 L18.88,8.87 Z"/></vector>''',
'ic_delete.xml': '''<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24"><path android:fillColor="#FFFFFFFF" android:pathData="M6,7 H18 L17,21 H7 Z M9,3 H15 L16,5 H20 V7 H4 V5 H8 Z"/></vector>''',
'ic_save.xml': '''<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24"><path android:fillColor="#FFFFFFFF" android:pathData="M5,3 H17 L21,7 V21 H3 V5 C3,3.9 3.9,3 5,3 Z M6,5 V10 H16 V5 Z M12,13 C9.79,13 8,14.79 8,17 C8,19.21 9.79,21 12,21 C14.21,21 16,19.21 16,17 C16,14.79 14.21,13 12,13 Z"/></vector>''',
'ic_add.xml': '''<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24"><path android:fillColor="#FFFFFFFF" android:pathData="M11,4 H13 V11 H20 V13 H13 V20 H11 V13 H4 V11 H11 Z"/></vector>''',
'ic_arrow_right.xml': '''<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24"><path android:fillColor="#FFFFFFFF" android:pathData="M9,5 L16,12 L9,19 L10.5,20.5 L19,12 L10.5,3.5 Z"/></vector>''',
'ic_back.xml': '''<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24"><path android:fillColor="#FFFFFFFF" android:pathData="M20,11 H7.83 L13.42,5.41 L12,4 L4,12 L12,20 L13.42,18.59 L7.83,13 H20 Z"/></vector>''',
'ic_check.xml': '''<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24"><path android:fillColor="#FFFFFFFF" android:pathData="M12,2 C6.48,2 2,6.48 2,12 C2,17.52 6.48,22 12,22 C17.52,22 22,17.52 22,12 C22,6.48 17.52,2 12,2 Z M10,17 L5,12 L6.41,10.59 L10,14.17 L17.59,6.58 L19,8 Z"/></vector>''',
'ic_medal.xml': '''<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="64dp" android:height="64dp" android:viewportWidth="64" android:viewportHeight="64"><path android:fillColor="#FFFFFFFF" android:pathData="M13,4 L27,4 L34,21 L22,27 Z"/><path android:fillColor="#FFFFFFFF" android:pathData="M37,4 L51,4 L42,27 L30,21 Z"/><path android:fillColor="#FFFFFFFF" android:pathData="M32,18 C19.3,18 9,28.3 9,41 C9,53.7 19.3,64 32,64 C44.7,64 55,53.7 55,41 C55,28.3 44.7,18 32,18 Z M32,25 C40.84,25 48,32.16 48,41 C48,49.84 40.84,57 32,57 C23.16,57 16,49.84 16,41 C16,32.16 23.16,25 32,25 Z"/></vector>'''
}
for name, data in icons.items():
    (DRAW/name).write_text(data,encoding='utf-8')

print('TEST 5 source and vector assets prepared')
