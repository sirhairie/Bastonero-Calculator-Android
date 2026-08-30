from pathlib import Path

SRC = Path('native/app/src/main/java/com/bastonero/calculator/nativeapp/MainActivity.java')
s = SRC.read_text(encoding='utf-8')

# TEST 20 identity. Preserve all TEST 19 behavior; only fix the About portrait and header cleanup.
s = s.replace('TEST 19', 'TEST 20').replace('bastonero_native_t19', 'bastonero_native_t20')
s = s.replace('// TEST 20 Ranking-Matched Export + Project Story About',
              '// TEST 20 About Portrait Fix + Header Cleanup', 1)

# Remove the redundant ABOUT label below the Bastonero logo.
old_about = '''        TextView about=text("ABOUT",12,GOLD_LIGHT,true);about.setGravity(Gravity.CENTER);about.setPadding(0,dp(4),0,0);hero.addView(about);\n'''
if old_about not in s:
    raise SystemExit('TEST 20 ABOUT label marker missing')
s = s.replace(old_about, '', 1)

# Rebuild the developer-photo holder with a FrameLayout and explicitly decoded bitmap.
# This avoids the blank LinearLayout placeholder seen in TEST 19 and guarantees the image view
# receives a real decoded portrait resource before it is attached.
old_photo = '''        LinearLayout photoFrame=new LinearLayout(this);photoFrame.setPadding(dp(3),dp(3),dp(3),dp(3));
        photoFrame.setBackground(gloss(Color.rgb(64,48,13),Color.rgb(23,38,53),Color.rgb(5,20,38),dp(18),GOLD_2));elevate(photoFrame,8);
        ImageView portrait=new ImageView(this);portrait.setScaleType(ImageView.ScaleType.CENTER_CROP);
        portrait.setImageResource(R.drawable.developer_photo);
        photoFrame.addView(portrait,new LinearLayout.LayoutParams(-1,-1));
        profile.addView(photoFrame,new LinearLayout.LayoutParams(dp(118),dp(154)));'''
new_photo = '''        FrameLayout photoFrame=new FrameLayout(this);photoFrame.setPadding(dp(3),dp(3),dp(3),dp(3));
        photoFrame.setBackground(gloss(Color.rgb(64,48,13),Color.rgb(23,38,53),Color.rgb(5,20,38),dp(18),GOLD_2));elevate(photoFrame,8);
        ImageView portrait=new ImageView(this);portrait.setScaleType(ImageView.ScaleType.CENTER_CROP);portrait.setAdjustViewBounds(false);
        Bitmap developerBitmap=BitmapFactory.decodeResource(getResources(),R.drawable.developer_photo);
        if(developerBitmap!=null)portrait.setImageBitmap(developerBitmap);else portrait.setImageResource(R.drawable.brand_logo);
        FrameLayout.LayoutParams portraitP=new FrameLayout.LayoutParams(-1,-1,Gravity.CENTER);photoFrame.addView(portrait,portraitP);
        profile.addView(photoFrame,new LinearLayout.LayoutParams(dp(118),dp(154)));'''
if old_photo not in s:
    raise SystemExit('TEST 20 developer photo marker missing')
s = s.replace(old_photo, new_photo, 1)

SRC.write_text(s,encoding='utf-8')
print('TEST 20 About portrait fix and header cleanup applied')
