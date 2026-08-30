from pathlib import Path

SRC = Path('native/app/src/main/java/com/bastonero/calculator/nativeapp/MainActivity.java')
s = SRC.read_text(encoding='utf-8')

# TEST 23 identity. Preserve all scoring, ranking, export, result-locking and About content.
s = s.replace('TEST 22', 'TEST 23').replace('bastonero_native_t22', 'bastonero_native_t23')
s = s.replace('// TEST 23 Developer Information + Circular Portrait + Revised Story',
              '// TEST 23 Perfect Circular Portrait + Coaching Support Layout', 1)

# Rebuild the developer portrait as a true oval-clipped frame with an overlay gold ring.
# Use a top-anchored square crop of the original portrait so the vacant space above the hair
# is preserved and the top of the developer's head/hair is never cropped by CENTER_CROP.
old_photo = '''        FrameLayout photoFrame=new FrameLayout(this);
        photoFrame.setBackground(round(Color.rgb(10,32,55),dp(999),GOLD_2));photoFrame.setClipToOutline(true);elevate(photoFrame,10);
        ImageView portrait=new ImageView(this);portrait.setScaleType(ImageView.ScaleType.CENTER_CROP);portrait.setAdjustViewBounds(false);
        Bitmap developerBitmap=BitmapFactory.decodeResource(getResources(),R.drawable.developer_photo);
        if(developerBitmap!=null)portrait.setImageBitmap(developerBitmap);else portrait.setImageResource(R.drawable.brand_logo);
        FrameLayout.LayoutParams portraitP=new FrameLayout.LayoutParams(-1,-1,Gravity.CENTER);portraitP.setMargins(dp(5),dp(5),dp(5),dp(5));photoFrame.addView(portrait,portraitP);
        LinearLayout.LayoutParams photoP=new LinearLayout.LayoutParams(dp(154),dp(154));photoP.setMargins(0,dp(14),0,dp(11));dev.addView(photoFrame,photoP);'''
new_photo = '''        FrameLayout photoFrame=new FrameLayout(this);
        android.graphics.drawable.GradientDrawable photoOval=new android.graphics.drawable.GradientDrawable();
        photoOval.setShape(android.graphics.drawable.GradientDrawable.OVAL);photoOval.setColor(Color.rgb(8,27,48));
        photoFrame.setBackground(photoOval);photoFrame.setClipToOutline(true);elevate(photoFrame,10);
        ImageView portrait=new ImageView(this);portrait.setScaleType(ImageView.ScaleType.FIT_XY);portrait.setAdjustViewBounds(false);
        Bitmap developerBitmap=BitmapFactory.decodeResource(getResources(),R.drawable.developer_photo);
        if(developerBitmap!=null){
            int side=Math.min(developerBitmap.getWidth(),developerBitmap.getHeight());
            int cropX=Math.max(0,(developerBitmap.getWidth()-side)/2);
            Bitmap safePortrait=Bitmap.createBitmap(developerBitmap,cropX,0,side,side);
            portrait.setImageBitmap(safePortrait);
        }else portrait.setImageResource(R.drawable.brand_logo);
        FrameLayout.LayoutParams portraitP=new FrameLayout.LayoutParams(-1,-1,Gravity.CENTER);photoFrame.addView(portrait,portraitP);
        android.graphics.drawable.GradientDrawable portraitRing=new android.graphics.drawable.GradientDrawable();
        portraitRing.setShape(android.graphics.drawable.GradientDrawable.OVAL);portraitRing.setColor(Color.TRANSPARENT);portraitRing.setStroke(dp(3),GOLD_2);
        photoFrame.setForeground(portraitRing);
        LinearLayout.LayoutParams photoP=new LinearLayout.LayoutParams(dp(158),dp(158));photoP.setMargins(0,dp(14),0,dp(11));dev.addView(photoFrame,photoP);'''
if old_photo not in s:
    raise SystemExit('TEST 23 portrait marker missing')
s = s.replace(old_photo,new_photo,1)

# Replace the awkward stacked Chaperon panel with two balanced profile blocks and one shared note.
old_chap = '''        LinearLayout chap=aboutSection("CHAPERON",R.drawable.ic_group);
        TextView chapName=text("Analyn F. Patacsil",16,WHITE,true);chapName.setPadding(0,dp(7),0,0);chap.addView(chapName);
        TextView chapRole=text("Chaperon",10,GOLD_2,true);chapRole.setPadding(0,dp(2),0,0);chap.addView(chapRole);
        View chapDivider=divider();LinearLayout.LayoutParams chapDivP=new LinearLayout.LayoutParams(-1,dp(1));chapDivP.setMargins(0,dp(10),0,dp(8));chap.addView(chapDivider,chapDivP);
        TextView coachName=text("Leonila M. Umpad",16,WHITE,true);chap.addView(coachName);
        TextView coachRole=text("Fellow Coach - Arnis Boys",10,GOLD_2,true);coachRole.setPadding(0,dp(2),0,0);chap.addView(coachRole);
        TextView chapBody=text("With appreciation for their support and assistance to the Arnis Girls during their activities and competitions.",10,MUTED,false);
        chapBody.setPadding(0,dp(9),0,0);chap.addView(chapBody);page.addView(chap,fullMargins(0,0,0,dp(12)));'''
new_chap = '''        LinearLayout chap=aboutSection("CHAPERON & COACHING SUPPORT",R.drawable.ic_group);

        LinearLayout chaperonCard=new LinearLayout(this);chaperonCard.setOrientation(LinearLayout.VERTICAL);
        chaperonCard.setPadding(dp(12),dp(10),dp(12),dp(10));
        chaperonCard.setBackground(round(Color.rgb(8,31,57),dp(14),LINE));
        TextView chapName=text("Analyn F. Patacsil",15,WHITE,true);chaperonCard.addView(chapName);
        TextView chapRole=text("Chaperon",10,GOLD_2,true);chapRole.setPadding(0,dp(3),0,0);chaperonCard.addView(chapRole);
        LinearLayout.LayoutParams chaperonP=new LinearLayout.LayoutParams(-1,-2);chaperonP.setMargins(0,dp(3),0,dp(8));chap.addView(chaperonCard,chaperonP);

        LinearLayout coachCard=new LinearLayout(this);coachCard.setOrientation(LinearLayout.VERTICAL);
        coachCard.setPadding(dp(12),dp(10),dp(12),dp(10));
        coachCard.setBackground(round(Color.rgb(8,31,57),dp(14),LINE));
        TextView coachName=text("Leonila M. Umpad",15,WHITE,true);coachCard.addView(coachName);
        TextView coachRole=text("Fellow Coach - Arnis Boys",10,GOLD_2,true);coachRole.setPadding(0,dp(3),0,0);coachCard.addView(coachRole);
        LinearLayout.LayoutParams coachP=new LinearLayout.LayoutParams(-1,-2);coachP.setMargins(0,0,0,dp(9));chap.addView(coachCard,coachP);

        LinearLayout supportNote=new LinearLayout(this);supportNote.setOrientation(LinearLayout.VERTICAL);
        supportNote.setPadding(dp(12),dp(10),dp(12),dp(10));supportNote.setBackground(round(Color.rgb(20,42,57),dp(12),GOLD));
        TextView noteLabel=text("WITH APPRECIATION",9,GOLD_2,true);supportNote.addView(noteLabel);
        TextView chapBody=text("For their support and assistance to the Arnis Girls during activities and competitions.",10,MUTED,false);
        chapBody.setPadding(0,dp(4),0,0);supportNote.addView(chapBody);chap.addView(supportNote);
        page.addView(chap,fullMargins(0,0,0,dp(12)));'''
if old_chap not in s:
    raise SystemExit('TEST 23 coaching-support marker missing')
s = s.replace(old_chap,new_chap,1)

SRC.write_text(s,encoding='utf-8')
print('TEST 23 perfect circular portrait and coaching support layout applied')
