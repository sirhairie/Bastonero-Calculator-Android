from pathlib import Path

SRC = Path('native/app/src/main/java/com/bastonero/calculator/nativeapp/MainActivity.java')
s = SRC.read_text(encoding='utf-8')

# TEST 21 identity. Preserve TEST 20 portrait repair and all scoring/export behavior.
s = s.replace('TEST 20', 'TEST 21').replace('bastonero_native_t20', 'bastonero_native_t21')
s = s.replace('// TEST 21 About Portrait Fix + Header Cleanup',
              '// TEST 21 Developer Profile + Project Story Panel', 1)

# Clean the portrait frame so the actual photo sits neatly inside a premium rounded card.
old_photo = '''        FrameLayout photoFrame=new FrameLayout(this);photoFrame.setPadding(dp(3),dp(3),dp(3),dp(3));
        photoFrame.setBackground(gloss(Color.rgb(64,48,13),Color.rgb(23,38,53),Color.rgb(5,20,38),dp(18),GOLD_2));elevate(photoFrame,8);
        ImageView portrait=new ImageView(this);portrait.setScaleType(ImageView.ScaleType.CENTER_CROP);portrait.setAdjustViewBounds(false);
        Bitmap developerBitmap=BitmapFactory.decodeResource(getResources(),R.drawable.developer_photo);
        if(developerBitmap!=null)portrait.setImageBitmap(developerBitmap);else portrait.setImageResource(R.drawable.brand_logo);
        FrameLayout.LayoutParams portraitP=new FrameLayout.LayoutParams(-1,-1,Gravity.CENTER);photoFrame.addView(portrait,portraitP);
        profile.addView(photoFrame,new LinearLayout.LayoutParams(dp(118),dp(154)));'''
new_photo = '''        FrameLayout photoFrame=new FrameLayout(this);
        photoFrame.setBackground(round(Color.rgb(10,32,55),dp(18),GOLD_2));photoFrame.setClipToOutline(true);elevate(photoFrame,8);
        ImageView portrait=new ImageView(this);portrait.setScaleType(ImageView.ScaleType.CENTER_CROP);portrait.setAdjustViewBounds(false);
        Bitmap developerBitmap=BitmapFactory.decodeResource(getResources(),R.drawable.developer_photo);
        if(developerBitmap!=null)portrait.setImageBitmap(developerBitmap);else portrait.setImageResource(R.drawable.brand_logo);
        FrameLayout.LayoutParams portraitP=new FrameLayout.LayoutParams(-1,-1,Gravity.CENTER);portraitP.setMargins(dp(4),dp(4),dp(4),dp(4));photoFrame.addView(portrait,portraitP);
        profile.addView(photoFrame,new LinearLayout.LayoutParams(dp(124),dp(164)));'''
if old_photo not in s:
    raise SystemExit('TEST 21 portrait frame marker missing')
s = s.replace(old_photo, new_photo, 1)

# Developer profile should contain only identity information. Move the purpose into Project Story.
old_identity_purpose = '''        TextView purpose=text("Created to make Arnis Anyo scoring faster, clearer, and more reliable during competitions.",11,TEXT,false);
        purpose.setPadding(0,dp(10),0,0);identity.addView(purpose);
        profile.addView(identity,new LinearLayout.LayoutParams(0,-2,1f));dev.addView(profile);

'''
new_identity_purpose = '''        profile.addView(identity,new LinearLayout.LayoutParams(0,-2,1f));dev.addView(profile);
        page.addView(dev,fullMargins(0,0,0,dp(12)));

'''
if old_identity_purpose not in s:
    raise SystemExit('TEST 21 identity-purpose marker missing')
s = s.replace(old_identity_purpose, new_identity_purpose, 1)

# Replace the old loose story paragraph with a dedicated premium PROJECT STORY panel.
story_start = s.find('        TextView story=text("Bastonero Calculator grew from actual experiences')
story_end_marker = '        page.addView(dev,fullMargins(0,0,0,dp(12)));'
story_end = s.find(story_end_marker, story_start)
if story_start < 0 or story_end < 0:
    raise SystemExit('TEST 21 old project story block missing')
story_end += len(story_end_marker)
new_story = '''        LinearLayout storyPanel=aboutSection("PROJECT STORY",R.drawable.ic_info);

        LinearLayout purposePanel=new LinearLayout(this);purposePanel.setOrientation(LinearLayout.VERTICAL);
        purposePanel.setPadding(dp(12),dp(11),dp(12),dp(11));
        purposePanel.setBackground(round(Color.rgb(28,44,42),dp(13),GOLD_2));
        TextView purposeLabel=text("PURPOSE",10,GOLD_2,true);purposePanel.addView(purposeLabel);
        TextView purposeText=text("Created to make Arnis Anyo scoring faster, clearer, and more reliable during competitions.",12,WHITE,true);
        purposeText.setPadding(0,dp(5),0,0);purposePanel.addView(purposeText);
        storyPanel.addView(purposePanel,fullMargins(0,dp(2),0,dp(10)));

        TextView story=text("Bastonero Calculator grew from actual experiences in coaching and handling Arnis Anyo competitions. During competitions, manually checking the scores from five judges, identifying the highest and lowest scores, computing the valid score, applying penalties, determining rankings, and resolving ties can become difficult—especially when accurate results are needed quickly.\\n\\nThe project began as a simple scoring concept designed to make this process easier and more dependable. Through repeated development, real-world testing, corrections, interface redesigns, and feedback, it gradually evolved into a dedicated native Android application.\\n\\nFeatures such as Result Locking, Five-Judge Total Tie-Breaking, Repeat Performance Detection, Ranking and Medal Results, Competitor and Team Management, and Saved Tournament Results were developed and refined based on practical competition needs.\\n\\nBastonero Calculator combines Arnis coaching experience, practical problem-solving, technology, and continuous improvement with one goal: to provide a dependable and easy-to-use scoring companion for Arnis Anyo competitions.",11,TEXT,false);
        story.setLineSpacing(0,1.12f);storyPanel.addView(story);
        page.addView(storyPanel,fullMargins(0,0,0,dp(12)));'''
s = s[:story_start] + new_story + s[story_end:]

SRC.write_text(s,encoding='utf-8')
print('TEST 21 developer profile and Project Story panel applied')
