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


# TEST 18 identity. Preserve TEST 17 confirmations and TEST 16 ranking logic.
s = s.replace('TEST 17', 'TEST 18').replace('bastonero_native_t17', 'bastonero_native_t18')
s = s.replace('// TEST 18 Premium Confirmation UX + Ranking Action Cleanup',
              '// TEST 18 Premium Save Experience + Portrait Result Export', 1)

# Cancel / No controls are now filled blue, not blue-outline-on-dark.
old_negative = '''        Button negative=primaryButton(negativeLabel,BLUE_2);negative.setTextSize(13);negative.setTextColor(BLUE_2);
        negative.setBackground(round(Color.rgb(7,27,48),dp(11),BLUE_2));negative.setOnClickListener(v->d.dismiss());'''
new_negative = '''        Button negative=primaryButton(negativeLabel,BLUE_2);negative.setTextSize(13);negative.setTextColor(WHITE);
        negative.setOnClickListener(v->d.dismiss());'''
if old_negative not in s:
    raise SystemExit('TEST 18 premium-confirm negative button marker missing')
s = s.replace(old_negative, new_negative, 1)

# Saving now uses an actual background save operation, a minimum 2-second premium loading
# experience, and only reports success after the file write succeeds. The generated result is
# a portrait premium tournament card rather than the previous landscape report.
replace_method('    private void saveResultImage(Competition c,ArrayList<ResultRow> rows){', '''    private void saveResultImage(Competition c,ArrayList<ResultRow> rows){
        if(rows.isEmpty())return;
        final Dialog loading=showSavingDialog();
        final long started=System.currentTimeMillis();
        new Thread(()->{
            boolean success=false;
            String error="Unable to save result";
            Bitmap bmp=null;
            try{
                int width=1200;
                int headerH=330, metaH=180, footerH=130;
                int cardsH=0;
                for(ResultRow r:rows)cardsH+=usesTieBreak(r)?390:330;
                int height=dpCanvas(34)+headerH+24+metaH+24+cardsH+footerH;
                bmp=Bitmap.createBitmap(width,height,Bitmap.Config.ARGB_8888);
                Canvas cv=new Canvas(bmp);
                Paint p=new Paint(Paint.ANTI_ALIAS_FLAG);
                cv.drawColor(BG);

                float left=28,right=width-28;
                float y=28;

                // Premium Bastonero header.
                p.setStyle(Paint.Style.FILL);p.setColor(NAVY);cv.drawRoundRect(left,y,right,y+headerH,34,34,p);
                p.setStyle(Paint.Style.STROKE);p.setStrokeWidth(4);p.setColor(GOLD_2);cv.drawRoundRect(left,y,right,y+headerH,34,34,p);p.setStyle(Paint.Style.FILL);
                Bitmap logo=BitmapFactory.decodeResource(getResources(),R.drawable.brand_logo);
                if(logo!=null){
                    Rect src=new Rect(0,0,logo.getWidth(),logo.getHeight());
                    RectF dst=new RectF(width/2f-78,y+26,width/2f+78,y+182);
                    cv.drawBitmap(logo,src,dst,p);
                }
                drawText(cv,p,"BASTONERO",width/2f,y+238,54,GOLD_LIGHT,true,Paint.Align.CENTER);
                drawText(cv,p,"C A L C U L A T O R",width/2f,y+282,30,WHITE,true,Paint.Align.CENTER);
                drawText(cv,p,"Official Tournament Result",width/2f,y+316,22,MUTED,false,Paint.Align.CENTER);
                y+=headerH+24;

                // Competition information panel.
                p.setColor(CARD);cv.drawRoundRect(left,y,right,y+metaH,26,26,p);
                p.setStyle(Paint.Style.STROKE);p.setStrokeWidth(2);p.setColor(LINE);cv.drawRoundRect(left,y,right,y+metaH,26,26,p);p.setStyle(Paint.Style.FILL);
                drawTextFit(cv,p,c.meet,54,y+55,38,WHITE,true,760);
                String dateVenue=(c.date.isEmpty()?"No date":c.date)+(c.venue.isEmpty()?"":"   •   "+c.venue);
                drawTextFit(cv,p,dateVenue,54,y+96,23,TEXT,false,1080);
                String attributes=c.level+"   •   "+(isTeam(c)?"Team":"Individual")+"   •   "+c.division+"   •   "+c.weapon;
                drawTextFit(cv,p,attributes,54,y+145,23,GOLD_2,true,1080);
                y+=metaH+24;

                // Ranked result cards.
                for(ResultRow r:rows){
                    boolean tie=usesTieBreak(r);
                    boolean repeat="REPEAT PERFORMANCE".equals(r.status);
                    int cardH=tie?370:310;
                    int accent=medalAccent(r);
                    float bottom=y+cardH;
                    p.setColor(CARD);cv.drawRoundRect(left,y,right,bottom,28,28,p);
                    p.setStyle(Paint.Style.STROKE);p.setStrokeWidth(4);p.setColor(accent);cv.drawRoundRect(left,y,right,bottom,28,28,p);p.setStyle(Paint.Style.FILL);

                    // Rank medal.
                    float cx=135,cy=y+103;
                    p.setColor(Color.argb(65,Color.red(accent),Color.green(accent),Color.blue(accent)));cv.drawCircle(cx,cy,82,p);
                    p.setColor(accent);cv.drawCircle(cx,cy,65,p);
                    p.setColor(NAVY);cv.drawCircle(cx,cy,51,p);
                    drawText(cv,p,String.valueOf(r.rank),cx,cy+17,48,accent,true,Paint.Align.CENTER);

                    // Identity + medal/place remark.
                    drawTextFit(cv,p,safeName(r.entry.name),235,y+66,36,WHITE,true,610);
                    if(!r.entry.school.isEmpty())drawTextFit(cv,p,r.entry.school,235,y+101,20,MUTED,false,610);
                    if(!repeat)drawTextRight(cv,p,shortRemark(r),right-34,y+62,22,accent,true);

                    // Judge score boxes.
                    float judgesY=y+126;
                    float jx=235;
                    float jw=108;
                    for(int i=0;i<5;i++){
                        p.setColor(Color.rgb(8,28,51));cv.drawRoundRect(jx,judgesY,jx+jw,judgesY+70,12,12,p);
                        p.setStyle(Paint.Style.STROKE);p.setStrokeWidth(1.5f);p.setColor(LINE);cv.drawRoundRect(jx,judgesY,jx+jw,judgesY+70,12,12,p);p.setStyle(Paint.Style.FILL);
                        drawText(cv,p,"J"+(i+1),jx+jw/2,judgesY+24,16,MUTED,true,Paint.Align.CENTER);
                        drawText(cv,p,fmt1(r.data.nums[i]),jx+jw/2,judgesY+55,25,WHITE,true,Paint.Align.CENTER);
                        jx+=jw+12;
                    }

                    // Technical metrics and dominant Final Score box.
                    float metricsY=y+218;
                    drawResultMetric(cv,p,"REMOVED H&L",fmt1(r.data.high)+" | "+fmt1(r.data.low),235,metricsY,190,accent);
                    drawResultMetric(cv,p,"VALID SCORE",fmt(r.data.score),437,metricsY,175,accent);
                    drawResultMetric(cv,p,"PENALTY",fmt1(r.data.penalty),624,metricsY,155,accent);
                    float finalX=805;
                    p.setColor(Color.rgb(5,23,43));cv.drawRoundRect(finalX,metricsY-9,right-30,metricsY+73,16,16,p);
                    p.setStyle(Paint.Style.STROKE);p.setStrokeWidth(2.5f);p.setColor(accent);cv.drawRoundRect(finalX,metricsY-9,right-30,metricsY+73,16,16,p);p.setStyle(Paint.Style.FILL);
                    drawText(cv,p,"FINAL SCORE",finalX+18,metricsY+18,17,accent,true);
                    drawTextRight(cv,p,fmt(r.data.net),right-50,metricsY+57,38,accent,true);

                    if(tie){
                        float tieY=y+302;
                        p.setColor(Color.rgb(42,35,17));cv.drawRoundRect(235,tieY,right-30,tieY+48,13,13,p);
                        p.setStyle(Paint.Style.STROKE);p.setStrokeWidth(2);p.setColor(GOLD_2);cv.drawRoundRect(235,tieY,right-30,tieY+48,13,13,p);p.setStyle(Paint.Style.FILL);
                        drawText(cv,p,"5-JUDGE TOTAL SCORE",257,tieY+31,17,GOLD_LIGHT,true);
                        drawTextRight(cv,p,fmt(r.data.fiveTotal),right-52,tieY+33,27,GOLD_2,true);
                        if(repeat){
                            p.setColor(RED);cv.drawRoundRect(54,tieY+58,right-30,tieY+98,12,12,p);
                            drawText(cv,p,"REPEAT PERFORMANCE REQUIRED",width/2f,tieY+85,18,WHITE,true,Paint.Align.CENTER);
                            bottom=tieY+113;
                        }
                    }
                    y=bottom+20;
                }

                // Developer credit with premium golden badge.
                float badgeW=600,badgeH=58,bx=(width-badgeW)/2f,by=height-92;
                p.setColor(Color.rgb(61,45,12));cv.drawRoundRect(bx,by,bx+badgeW,by+badgeH,29,29,p);
                p.setStyle(Paint.Style.STROKE);p.setStrokeWidth(2.5f);p.setColor(GOLD_2);cv.drawRoundRect(bx,by,bx+badgeW,by+badgeH,29,29,p);p.setStyle(Paint.Style.FILL);
                drawText(cv,p,"Develop by Sir Hairie Laysam",width/2f,by+38,21,GOLD_LIGHT,true,Paint.Align.CENTER);

                String file="Bastonero_Result_"+System.currentTimeMillis()+".png";
                if(Build.VERSION.SDK_INT>=29){
                    ContentValues values=new ContentValues();
                    values.put(MediaStore.Images.Media.DISPLAY_NAME,file);
                    values.put(MediaStore.Images.Media.MIME_TYPE,"image/png");
                    values.put(MediaStore.Images.Media.RELATIVE_PATH,"Pictures/Bastonero");
                    Uri uri=getContentResolver().insert(MediaStore.Images.Media.EXTERNAL_CONTENT_URI,values);
                    if(uri==null)throw new Exception("Could not create image");
                    try(OutputStream out=getContentResolver().openOutputStream(uri)){
                        if(out==null||!bmp.compress(Bitmap.CompressFormat.PNG,100,out))throw new Exception("Could not write image");
                    }
                }else{
                    java.io.File dir=new java.io.File(getExternalFilesDir(android.os.Environment.DIRECTORY_PICTURES),"Bastonero");
                    if(!dir.exists()&&!dir.mkdirs())throw new Exception("Could not create Pictures/Bastonero");
                    java.io.File f=new java.io.File(dir,file);
                    try(OutputStream out=new java.io.FileOutputStream(f)){
                        if(!bmp.compress(Bitmap.CompressFormat.PNG,100,out))throw new Exception("Could not write image");
                    }
                }
                success=true;
            }catch(Exception ex){
                error=ex.getMessage()==null?"Unable to save result":ex.getMessage();
            }finally{
                if(bmp!=null)bmp.recycle();
            }

            long wait=2000-(System.currentTimeMillis()-started);
            if(wait>0)try{Thread.sleep(wait);}catch(Exception ignored){}
            final boolean ok=success;
            final String err=error;
            runOnUiThread(()->{
                if(loading.isShowing())loading.dismiss();
                if(ok)showSavedDialog();
                else premiumConfirm("Save Failed","Unable to save the result image. "+err,R.drawable.ic_info,"Close","Try Again",RED,()->saveResultImage(c,rows));
            });
        }).start();
    }

    private void drawResultMetric(Canvas cv,Paint p,String label,String value,float x,float y,float width,int accent){
        drawText(cv,p,label,x,y+15,15,MUTED,true);
        drawText(cv,p,value,x,y+49,27,WHITE,true);
        p.setColor(Color.argb(85,Color.red(accent),Color.green(accent),Color.blue(accent)));cv.drawRect(x+width-3,y+3,x+width,y+55,p);
    }

    private void drawTextFit(Canvas cv,Paint p,String value,float x,float y,float startSize,int color,boolean bold,float maxWidth){
        float size=startSize;
        p.setTypeface(bold?Typeface.DEFAULT_BOLD:Typeface.DEFAULT);
        p.setTextAlign(Paint.Align.LEFT);
        p.setTextSize(size);
        while(size>15&&p.measureText(value)>maxWidth){size-=1.5f;p.setTextSize(size);}
        drawText(cv,p,value,x,y,size,color,bold);
    }

    private int dpCanvas(int n){return n;}''', 'TEST 18 portrait result export')

# Replace the old stock gray success dialog with a premium gold/navy success card and add a
# dedicated non-cancelable loading dialog used while the file is actually being written.
replace_method('    private void showSavedDialog(){', '''    private void showSavedDialog(){
        final Dialog d=new Dialog(this);d.requestWindowFeature(Window.FEATURE_NO_TITLE);
        LinearLayout panel=darkCard(GOLD);panel.setPadding(dp(17),dp(17),dp(17),dp(17));
        LinearLayout top=row();top.setGravity(Gravity.CENTER_VERTICAL);
        LinearLayout iconBadge=new LinearLayout(this);iconBadge.setGravity(Gravity.CENTER);
        iconBadge.setBackground(gloss(Color.rgb(31,65,33),Color.rgb(17,48,32),Color.rgb(5,25,29),dp(999),GOLD));
        iconBadge.addView(iconView(R.drawable.ic_check,GOLD_2,30),new LinearLayout.LayoutParams(dp(30),dp(30)));elevate(iconBadge,8);
        top.addView(iconBadge,new LinearLayout.LayoutParams(dp(58),dp(58)));
        LinearLayout words=new LinearLayout(this);words.setOrientation(LinearLayout.VERTICAL);words.setPadding(dp(13),0,0,0);
        words.addView(text("Result Successfully Saved",19,WHITE,true));
        TextView path=text("Saved to Pictures/Bastonero",12,GOLD_LIGHT,false);path.setPadding(0,dp(5),0,0);words.addView(path);
        top.addView(words,new LinearLayout.LayoutParams(0,-2,1f));panel.addView(top);
        d.setContentView(panel);d.show();
        Window w=d.getWindow();if(w!=null){w.setBackgroundDrawable(new android.graphics.drawable.ColorDrawable(Color.TRANSPARENT));w.addFlags(WindowManager.LayoutParams.FLAG_DIM_BEHIND);WindowManager.LayoutParams lp=w.getAttributes();lp.dimAmount=.72f;w.setAttributes(lp);w.setLayout((int)(getResources().getDisplayMetrics().widthPixels*.88f),WindowManager.LayoutParams.WRAP_CONTENT);}
        new Handler(Looper.getMainLooper()).postDelayed(()->{if(d.isShowing())d.dismiss();},2200);
    }

    private Dialog showSavingDialog(){
        final Dialog d=new Dialog(this);d.requestWindowFeature(Window.FEATURE_NO_TITLE);d.setCancelable(false);
        LinearLayout panel=darkCard(GOLD);panel.setPadding(dp(18),dp(18),dp(18),dp(18));
        LinearLayout row=row();row.setGravity(Gravity.CENTER_VERTICAL);
        ProgressBar spinner=new ProgressBar(this);spinner.setIndeterminate(true);spinner.getIndeterminateDrawable().setColorFilter(GOLD_2,PorterDuff.Mode.SRC_IN);
        row.addView(spinner,new LinearLayout.LayoutParams(dp(54),dp(54)));
        LinearLayout words=new LinearLayout(this);words.setOrientation(LinearLayout.VERTICAL);words.setPadding(dp(14),0,0,0);
        words.addView(text("Saving Result…",19,WHITE,true));
        TextView note=text("Creating your official tournament result image",11,MUTED,false);note.setPadding(0,dp(5),0,0);words.addView(note);
        row.addView(words,new LinearLayout.LayoutParams(0,-2,1f));panel.addView(row);
        d.setContentView(panel);d.show();
        Window w=d.getWindow();if(w!=null){w.setBackgroundDrawable(new android.graphics.drawable.ColorDrawable(Color.TRANSPARENT));w.addFlags(WindowManager.LayoutParams.FLAG_DIM_BEHIND);WindowManager.LayoutParams lp=w.getAttributes();lp.dimAmount=.78f;w.setAttributes(lp);w.setLayout((int)(getResources().getDisplayMetrics().widthPixels*.86f),WindowManager.LayoutParams.WRAP_CONTENT);}
        return d;
    }''', 'TEST 18 premium saved/loading dialogs')

SRC.write_text(s,encoding='utf-8')
print('TEST 18 premium save experience and portrait result export applied')
