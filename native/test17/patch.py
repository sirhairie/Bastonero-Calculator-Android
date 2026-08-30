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


# TEST 17 identity. Preserve TEST 16 score-grid ranking and TEST 13 official result locking.
s = s.replace('TEST 16', 'TEST 17').replace('bastonero_native_t16', 'bastonero_native_t17')
s = s.replace('// TEST 17 Ranking Score Grid + Tie Decision Emphasis',
              '// TEST 17 Premium Confirmation UX + Ranking Action Cleanup', 1)

# Repeat-performance cards already carry a strong red REQUIRED bar at the bottom. Remove the
# redundant Repeat Performance pill beside the competitor/team name while preserving normal
# medal/place badges for every other ranking state.
old_badge = '''        TextView medalBadge=pill(shortRemark(r),WHITE,mix(accent,BG,.42f));medalBadge.setGravity(Gravity.CENTER);
        LinearLayout.LayoutParams bp=new LinearLayout.LayoutParams(-2,dp(31));bp.setMargins(dp(8),0,0,0);nameRow.addView(medalBadge,bp);'''
new_badge = '''        if(!repeat){
            TextView medalBadge=pill(shortRemark(r),WHITE,mix(accent,BG,.42f));medalBadge.setGravity(Gravity.CENTER);
            LinearLayout.LayoutParams bp=new LinearLayout.LayoutParams(-2,dp(31));bp.setMargins(dp(8),0,0,0);nameRow.addView(medalBadge,bp);
        }'''
if old_badge not in s:
    raise SystemExit('TEST 17 ranking badge marker missing')
s = s.replace(old_badge, new_badge, 1)

# Ranking footer actions belong on one compact row.
old_rank_actions = '''        Button back=primaryButton("Back to Scoring",BLUE_2);
        back.setTextSize(14);back.setOnClickListener(v->showWorkspace());
        content.addView(back,new LinearLayout.LayoutParams(-1,dp(52)));
        Button save=primaryButton("Save Result",RED);
        save.setTextSize(14);save.setEnabled(!rows.isEmpty());save.setAlpha(rows.isEmpty()?0.45f:1f);
        save.setOnClickListener(v->saveResultImage(c,rows));
        content.addView(save,fullMargins(0,dp(9),0,0,dp(52)));'''
new_rank_actions = '''        LinearLayout resultActions=row();
        Button back=primaryButton("Back to Scoring",BLUE_2);
        back.setTextSize(13);back.setOnClickListener(v->showWorkspace());
        Button save=primaryButton("Save Result",RED);
        save.setTextSize(13);save.setEnabled(!rows.isEmpty());save.setAlpha(rows.isEmpty()?0.45f:1f);
        save.setOnClickListener(v->saveResultImage(c,rows));
        resultActions.addView(back,new LinearLayout.LayoutParams(0,dp(52),1f));
        LinearLayout.LayoutParams saveP=new LinearLayout.LayoutParams(0,dp(52),1f);saveP.setMargins(dp(8),0,0,0);resultActions.addView(save,saveP);
        content.addView(resultActions);'''
if old_rank_actions not in s:
    raise SystemExit('TEST 17 ranking actions marker missing')
s = s.replace(old_rank_actions, new_rank_actions, 1)

# Update Result must never unlock an official result by accidental tap.
old_unlock = '''            if(e.resultLocked){
                e.resultLocked=false;saveState();refreshAt(e.id);return;
            }'''
new_unlock = '''            if(e.resultLocked){
                premiumConfirm("Update Result","Are you sure you want to update this result?",R.drawable.ic_edit,"No","Yes",GREEN,()->{
                    e.resultLocked=false;saveState();refreshAt(e.id);
                });
                return;
            }'''
if old_unlock not in s:
    raise SystemExit('TEST 17 Update Result unlock marker missing')
s = s.replace(old_unlock, new_unlock, 1)

# Edit Registration also requires explicit confirmation before reopening registration.
old_reopen = '''            Button reopen=primaryButton("Edit Registration",GREEN);reopen.setOnClickListener(v->{c.scoringStarted=false;saveState();toast("Registration reopened");showWorkspace();});panel.addView(reopen,fullMargins(0,dp(10),0,0,dp(46)));'''
new_reopen = '''            Button reopen=primaryButton("Edit Registration",GREEN);reopen.setOnClickListener(v->{
                premiumConfirm("Edit Registration","Are you sure you want to edit this registration?",R.drawable.ic_edit,"No","Yes",GREEN,()->{
                    c.scoringStarted=false;saveState();toast("Registration reopened");showWorkspace();
                });
            });panel.addView(reopen,fullMargins(0,dp(10),0,0,dp(46)));'''
if old_reopen not in s:
    raise SystemExit('TEST 17 Edit Registration marker missing')
s = s.replace(old_reopen, new_reopen, 1)

# Replace stock Android remove/delete prompts with the same premium navy/gold visual language
# used throughout Bastonero. Destructive actions remain red; cancellation remains blue.
replace_method('    private void confirmDeleteEntry(Competition c,Entry e){', '''    private void confirmDeleteEntry(Competition c,Entry e){
        premiumConfirm("Remove "+entryLabel(c),"Remove "+safeName(e.name)+" from this competition?",isTeam(c)?R.drawable.ic_group:R.drawable.ic_person,"Cancel","Remove",RED,()->{
            c.entries.remove(e);saveState();showWorkspace();
        });
    }''', 'TEST 17 premium remove entry confirmation')

replace_method('    private void confirmDeleteCompetition(Competition c){', '''    private void confirmDeleteCompetition(Competition c){
        premiumConfirm("Delete Competition","Delete "+c.meet+" and all scoring data?",R.drawable.ic_delete,"Cancel","Delete",RED,()->{
            competitions.remove(c);activeCompetition=null;saveState();showHome();
        });
    }''', 'TEST 17 premium delete competition confirmation')

marker='    private void confirmDeleteEntry(Competition c,Entry e){'
if marker not in s:
    raise SystemExit('TEST 17 premium-confirm insertion marker missing')
helper='''    private void premiumConfirm(String title,String message,int iconRes,String negativeLabel,String positiveLabel,int positiveColor,Runnable onConfirm){
        final Dialog d=new Dialog(this);
        d.requestWindowFeature(Window.FEATURE_NO_TITLE);
        d.setCancelable(true);

        LinearLayout panel=darkCard(GOLD);panel.setPadding(dp(16),dp(16),dp(16),dp(16));
        LinearLayout top=row();top.setGravity(Gravity.CENTER_VERTICAL);

        LinearLayout iconBadge=new LinearLayout(this);iconBadge.setGravity(Gravity.CENTER);
        iconBadge.setBackground(gloss(Color.rgb(20,54,91),Color.rgb(8,31,57),Color.rgb(4,19,36),dp(999),GOLD));
        iconBadge.addView(iconView(iconRes,GOLD_2,28),new LinearLayout.LayoutParams(dp(28),dp(28)));
        elevate(iconBadge,7);
        top.addView(iconBadge,new LinearLayout.LayoutParams(dp(56),dp(56)));

        LinearLayout words=new LinearLayout(this);words.setOrientation(LinearLayout.VERTICAL);words.setPadding(dp(12),0,0,0);
        TextView heading=text(title,20,WHITE,true);heading.setSingleLine(false);words.addView(heading);
        TextView msg=text(message,13,TEXT,false);msg.setPadding(0,dp(5),0,0);msg.setLineSpacing(0,1.08f);words.addView(msg);
        top.addView(words,new LinearLayout.LayoutParams(0,-2,1f));
        panel.addView(top);

        View div=divider();LinearLayout.LayoutParams divP=new LinearLayout.LayoutParams(-1,dp(1));divP.setMargins(0,dp(14),0,dp(14));panel.addView(div,divP);

        LinearLayout actions=row();
        Button negative=primaryButton(negativeLabel,BLUE_2);negative.setTextSize(13);negative.setTextColor(BLUE_2);
        negative.setBackground(round(Color.rgb(7,27,48),dp(11),BLUE_2));negative.setOnClickListener(v->d.dismiss());
        Button positive=primaryButton(positiveLabel,positiveColor);positive.setTextSize(13);positive.setOnClickListener(v->{d.dismiss();if(onConfirm!=null)onConfirm.run();});
        actions.addView(negative,new LinearLayout.LayoutParams(0,dp(48),1f));
        LinearLayout.LayoutParams pp=new LinearLayout.LayoutParams(0,dp(48),1f);pp.setMargins(dp(9),0,0,0);actions.addView(positive,pp);
        panel.addView(actions);

        d.setContentView(panel);d.show();
        Window w=d.getWindow();
        if(w!=null){
            w.setBackgroundDrawable(new android.graphics.drawable.ColorDrawable(Color.TRANSPARENT));
            w.addFlags(WindowManager.LayoutParams.FLAG_DIM_BEHIND);
            WindowManager.LayoutParams lp=w.getAttributes();lp.dimAmount=.80f;w.setAttributes(lp);
            int width=(int)(getResources().getDisplayMetrics().widthPixels*.88f);
            w.setLayout(width,WindowManager.LayoutParams.WRAP_CONTENT);
        }
    }

'''
s = s.replace(marker, helper + marker, 1)

SRC.write_text(s,encoding='utf-8')
print('TEST 17 premium confirmation UX and ranking action cleanup applied')
