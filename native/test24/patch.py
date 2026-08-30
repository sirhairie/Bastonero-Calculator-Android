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


# TEST 24 identity. Preserve TEST 23 About page and all scoring/result-lock behavior.
s = s.replace('TEST 23', 'TEST 24').replace('bastonero_native_t23', 'bastonero_native_t24')
s = s.replace('// TEST 24 Perfect Circular Portrait + Coaching Support Layout',
              '// TEST 24 Portrait Saved Result Redesign', 1)

# Completely rebuild the saved-result image as a portrait-first tournament result.
replace_method('    private void saveResultImage(Competition c,ArrayList<ResultRow> rows){', '''    private void saveResultImage(Competition c,ArrayList<ResultRow> rows){
        if(rows.isEmpty())return;
        final Dialog loading=showSavingDialog();
        final long started=System.currentTimeMillis();
        new Thread(()->{
            boolean success=false;
            String error="Unable to save result";
            Bitmap bmp=null;
            try{
                final int width=1080;
                final int margin=34;
                final int headerH=300;
                final int metaH=176;
                int cardsH=0;
                for(ResultRow r:rows){
                    boolean tie=usesTieBreak(r);
                    cardsH+=tie?722:567;
                }
                final int footerH=126;
                final int height=margin+headerH+20+metaH+20+cardsH+footerH;
                bmp=Bitmap.createBitmap(width,height,Bitmap.Config.ARGB_8888);
                Canvas cv=new Canvas(bmp);
                Paint p=new Paint(Paint.ANTI_ALIAS_FLAG);
                cv.drawColor(BG);

                float left=margin,right=width-margin,y=margin;

                // Premium portrait header. Bastonero Calculator is intentionally one line.
                p.setColor(NAVY);cv.drawRoundRect(left,y,right,y+headerH,32,32,p);
                p.setStyle(Paint.Style.STROKE);p.setStrokeWidth(4);p.setColor(GOLD_2);
                cv.drawRoundRect(left,y,right,y+headerH,32,32,p);p.setStyle(Paint.Style.FILL);
                Bitmap logo=BitmapFactory.decodeResource(getResources(),R.drawable.brand_logo);
                if(logo!=null){
                    Rect src=new Rect(0,0,logo.getWidth(),logo.getHeight());
                    RectF dst=new RectF(width/2f-62,y+18,width/2f+62,y+142);
                    cv.drawBitmap(logo,src,dst,p);
                }
                drawTextCenteredFit(cv,p,"Bastonero Calculator",width/2f,y+201,50,GOLD_LIGHT,true,940);
                drawTextCenteredFit(cv,p,"Official Tournament Result",width/2f,y+252,34,WHITE,true,940);
                y+=headerH+20;

                // Competition information centered under the header.
                p.setColor(CARD);cv.drawRoundRect(left,y,right,y+metaH,24,24,p);
                p.setStyle(Paint.Style.STROKE);p.setStrokeWidth(2);p.setColor(LINE);
                cv.drawRoundRect(left,y,right,y+metaH,24,24,p);p.setStyle(Paint.Style.FILL);
                drawTextCenteredFit(cv,p,c.meet,width/2f,y+48,34,WHITE,true,930);
                String dateVenue=(c.date.isEmpty()?"No date":c.date)+(c.venue.isEmpty()?"":"   •   "+c.venue);
                drawTextCenteredFit(cv,p,dateVenue,width/2f,y+91,21,TEXT,false,930);
                String attributes=c.level+"   •   "+(isTeam(c)?"Team":"Individual")+"   •   "+c.division+"   •   "+c.weapon;
                drawTextCenteredFit(cv,p,attributes,width/2f,y+139,21,GOLD_2,true,930);
                y+=metaH+20;

                for(ResultRow r:rows){
                    boolean tie=usesTieBreak(r);
                    boolean repeat="REPEAT PERFORMANCE".equals(r.status);
                    int accent=repeat?GOLD_2:medalAccent(r);
                    int cardH=tie?700:545;
                    float cardBottom=y+cardH;

                    p.setColor(CARD);cv.drawRoundRect(left,y,right,cardBottom,28,28,p);
                    p.setStyle(Paint.Style.STROKE);p.setStrokeWidth(4);p.setColor(accent);
                    cv.drawRoundRect(left,y,right,cardBottom,28,28,p);p.setStyle(Paint.Style.FILL);

                    // Identity / medal area. Divider is below the medal so nothing overlaps it.
                    if(repeat)drawExportTieBadge(cv,p,left+38,y+26,138,138);
                    else drawExportMedal(cv,p,r.rank,accent,left+38,y+26,138,138);

                    drawTextFit(cv,p,safeName(r.entry.name),left+208,y+66,32,WHITE,true,500);
                    if(!r.entry.school.isEmpty())drawTextFit(cv,p,r.entry.school,left+208,y+104,20,MUTED,false,500);

                    if(!repeat){
                        String medalLabel=shortRemark(r);
                        float badgeW=Math.max(160,premiumTextWidth(p,medalLabel,17,true)+44);
                        float bx=right-badgeW-26,by=y+43;
                        p.setColor(Color.argb(230,Math.max(18,Color.red(accent)/3),Math.max(18,Color.green(accent)/3),Math.max(18,Color.blue(accent)/3)));
                        cv.drawRoundRect(bx,by,right-26,by+50,25,25,p);
                        p.setStyle(Paint.Style.STROKE);p.setStrokeWidth(1.8f);p.setColor(accent);
                        cv.drawRoundRect(bx,by,right-26,by+50,25,25,p);p.setStyle(Paint.Style.FILL);
                        drawText(cv,p,medalLabel,(bx+right-26)/2f,by+33,17,WHITE,true,Paint.Align.CENTER);
                    }

                    float dividerY=y+184;
                    p.setColor(LINE_SOFT);cv.drawRect(left+26,dividerY,right-26,dividerY+2,p);

                    // Four major scoring values in a roomy 2 x 2 grid.
                    float innerLeft=left+28,innerRight=right-28;
                    float gap=14;
                    float metricW=(innerRight-innerLeft-gap)/2f;
                    float metricY1=y+207;
                    float metricY2=y+312;
                    drawExportMetricBox(cv,p,"REMOVED H&L",fmt1(r.data.high)+" | "+fmt1(r.data.low),innerLeft,metricY1,metricW,90,WHITE,false);
                    drawExportMetricBox(cv,p,"VALID SCORE",fmt(r.data.score),innerLeft+metricW+gap,metricY1,metricW,90,accent,true);
                    drawExportMetricBox(cv,p,"PENALTY",fmt1(r.data.penalty),innerLeft,metricY2,metricW,90,WHITE,false);
                    drawExportMetricBox(cv,p,"FINAL SCORE",fmt(r.data.net),innerLeft+metricW+gap,metricY2,metricW,90,accent,true);

                    // Five judges stay in one clean row.
                    float judgeY=y+424;
                    float judgeGap=10;
                    float jw=(innerRight-innerLeft-judgeGap*4)/5f;
                    for(int i=0;i<5;i++)drawExportJudgeBox(cv,p,"J"+(i+1),fmt1(r.data.nums[i]),innerLeft+i*(jw+judgeGap),judgeY,jw,78);

                    if(tie){
                        float totalY=y+522;
                        drawExportTieTotal(cv,p,fmt(r.data.fiveTotal),innerLeft,totalY,innerRight-innerLeft,84);
                        float statusY=y+620;
                        if(repeat){
                            p.setColor(RED);cv.drawRoundRect(innerLeft,statusY,innerRight,statusY+52,14,14,p);
                            drawText(cv,p,"REPEAT PERFORMANCE REQUIRED",width/2f,statusY+34,18,WHITE,true,Paint.Align.CENTER);
                        }else{
                            p.setColor(Color.rgb(58,48,22));cv.drawRoundRect(innerLeft,statusY,innerRight,statusY+48,13,13,p);
                            p.setStyle(Paint.Style.STROKE);p.setStrokeWidth(1.8f);p.setColor(GOLD_2);
                            cv.drawRoundRect(innerLeft,statusY,innerRight,statusY+48,13,13,p);p.setStyle(Paint.Style.FILL);
                            String label="TIE-BREAK WINNER".equals(r.status)?"TIE-BREAK WINNER":"TIE-BREAK APPLIED";
                            drawText(cv,p,label,width/2f,statusY+32,17,GOLD_LIGHT,true,Paint.Align.CENTER);
                        }
                    }

                    y=cardBottom+22;
                }

                // Compact gold developer footer after the final result card.
                float badgeW=610,badgeH=58,bx=(width-badgeW)/2f,by=y+10;
                p.setColor(Color.rgb(65,46,10));cv.drawRoundRect(bx,by,bx+badgeW,by+badgeH,29,29,p);
                p.setStyle(Paint.Style.STROKE);p.setStrokeWidth(2.5f);p.setColor(GOLD_2);
                cv.drawRoundRect(bx,by,bx+badgeW,by+badgeH,29,29,p);p.setStyle(Paint.Style.FILL);
                drawText(cv,p,"Develop by Sir Hairie Laysam",width/2f,by+38,20,GOLD_LIGHT,true,Paint.Align.CENTER);

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
    }''', 'TEST 24 portrait saved-result export')

# Replace the fragile drawable-based export medal with stable Canvas geometry and add a neutral tie badge.
replace_method('    private void drawExportMedal(Canvas cv,Paint p,int rank,int accent,float x,float y,float w,float h){', '''    private void drawExportMedal(Canvas cv,Paint p,int rank,int accent,float x,float y,float w,float h){
        float cx=x+w/2f;
        float r=Math.min(w,h)*0.29f;

        Path leftRibbon=new Path();
        leftRibbon.moveTo(cx-r*.72f,y+6);leftRibbon.lineTo(cx-r*.08f,y+6);
        leftRibbon.lineTo(cx-r*.18f,y+h*.53f);leftRibbon.lineTo(cx-r*.95f,y+h*.53f);
        leftRibbon.close();p.setColor(accent);cv.drawPath(leftRibbon,p);

        Path rightRibbon=new Path();
        rightRibbon.moveTo(cx+r*.08f,y+6);rightRibbon.lineTo(cx+r*.72f,y+6);
        rightRibbon.lineTo(cx+r*.95f,y+h*.53f);rightRibbon.lineTo(cx+r*.18f,y+h*.53f);
        rightRibbon.close();p.setColor(accent);cv.drawPath(rightRibbon,p);

        float cy=y+h*.64f;
        p.setColor(Color.argb(70,0,0,0));cv.drawCircle(cx+3,cy+5,r+8,p);
        p.setColor(accent);cv.drawCircle(cx,cy,r+7,p);
        p.setColor(Color.rgb(247,226,165));cv.drawCircle(cx,cy,r-2,p);
        p.setStyle(Paint.Style.STROKE);p.setStrokeWidth(3);p.setColor(GOLD_LIGHT);cv.drawCircle(cx,cy,r-2,p);p.setStyle(Paint.Style.FILL);
        drawText(cv,p,String.valueOf(rank),cx,cy+11,30,Color.rgb(14,24,34),true,Paint.Align.CENTER);
    }

    private void drawExportTieBadge(Canvas cv,Paint p,float x,float y,float w,float h){
        float cx=x+w/2f,cy=y+h*.53f;
        float r=Math.min(w,h)*.34f;
        p.setColor(Color.argb(75,0,0,0));cv.drawCircle(cx+3,cy+5,r+7,p);
        p.setColor(Color.rgb(25,38,52));cv.drawCircle(cx,cy,r+7,p);
        p.setStyle(Paint.Style.STROKE);p.setStrokeWidth(5);p.setColor(GOLD_2);cv.drawCircle(cx,cy,r+7,p);p.setStyle(Paint.Style.FILL);
        p.setColor(Color.rgb(58,48,22));cv.drawCircle(cx,cy,r-4,p);
        drawText(cv,p,"TIE",cx,cy+10,26,GOLD_LIGHT,true,Paint.Align.CENTER);
    }''', 'TEST 24 clean export medal and tie badge')

SRC.write_text(s,encoding='utf-8')
print('TEST 24 portrait saved-result redesign applied')
