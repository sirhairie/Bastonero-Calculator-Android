from pathlib import Path

SRC = Path('native/app/src/main/java/com/bastonero/calculator/nativeapp/MainActivity.java')
s = SRC.read_text(encoding='utf-8')

# TEST 22 identity. Preserve TEST 21 About structure, TEST 20 portrait repair,
# and all existing scoring, ranking, confirmation, and export behavior.
s = s.replace('TEST 21', 'TEST 22').replace('bastonero_native_t21', 'bastonero_native_t22')
s = s.replace('// TEST 22 Developer Profile + Project Story Panel',
              '// TEST 22 Developer Information + Circular Portrait + Revised Story', 1)

# Replace the developer profile row with a centered circular portrait and identity stack.
start = s.find('        LinearLayout dev=darkCard(GOLD);')
end_marker = '        page.addView(dev,fullMargins(0,0,0,dp(12)));'
end = s.find(end_marker, start)
if start < 0 or end < 0:
    raise SystemExit('TEST 22 developer information block missing')
end += len(end_marker)
new_dev = '''        LinearLayout dev=darkCard(GOLD);dev.setGravity(Gravity.CENTER_HORIZONTAL);
        TextView devHead=text("DEVELOPER INFORMATION",13,GOLD_LIGHT,true);devHead.setGravity(Gravity.CENTER);dev.addView(devHead);

        FrameLayout photoFrame=new FrameLayout(this);
        photoFrame.setBackground(round(Color.rgb(10,32,55),dp(999),GOLD_2));photoFrame.setClipToOutline(true);elevate(photoFrame,10);
        ImageView portrait=new ImageView(this);portrait.setScaleType(ImageView.ScaleType.CENTER_CROP);portrait.setAdjustViewBounds(false);
        Bitmap developerBitmap=BitmapFactory.decodeResource(getResources(),R.drawable.developer_photo);
        if(developerBitmap!=null)portrait.setImageBitmap(developerBitmap);else portrait.setImageResource(R.drawable.brand_logo);
        FrameLayout.LayoutParams portraitP=new FrameLayout.LayoutParams(-1,-1,Gravity.CENTER);portraitP.setMargins(dp(5),dp(5),dp(5),dp(5));photoFrame.addView(portrait,portraitP);
        LinearLayout.LayoutParams photoP=new LinearLayout.LayoutParams(dp(154),dp(154));photoP.setMargins(0,dp(14),0,dp(11));dev.addView(photoFrame,photoP);

        TextView devName=text("Hairie A. Laysam",20,WHITE,true);devName.setGravity(Gravity.CENTER);dev.addView(devName);
        TextView role=text("Teacher I",12,GOLD_2,true);role.setGravity(Gravity.CENTER);role.setPadding(0,dp(4),0,0);dev.addView(role);
        TextView school=text("Sta. Maria National High School",11,MUTED,false);school.setGravity(Gravity.CENTER);school.setPadding(dp(8),dp(3),dp(8),dp(2));dev.addView(school);
        page.addView(dev,fullMargins(0,0,0,dp(12)));'''
s = s[:start] + new_dev + s[end:]

# Replace the Project Story narrative with the user's actual origin story.
story_start = s.find('        TextView story=text("Bastonero Calculator grew from actual experiences')
story_end = s.find('        story.setLineSpacing(0,1.12f);storyPanel.addView(story);', story_start)
if story_start < 0 or story_end < 0:
    raise SystemExit('TEST 22 Project Story narrative missing')
story_end += len('        story.setLineSpacing(0,1.12f);storyPanel.addView(story);')
new_story = '''        TextView story=text("Bastonero Calculator began when Hairie A. Laysam was directly assigned by the school principal to serve as coach of the Arnis Girls. At that time, he had no prior knowledge of Arnis, its competition rules and regulations, or its scoring system. In practical terms, he was a complete beginner.\\n\\nAs time went by, he began learning the sport step by step—its rules, gameplay, judging, score computation, competition flow, and the many details needed to guide athletes correctly.\\n\\nDuring that learning process, Icon Jules F. Descallar suggested creating an application that could compute Arnis Anyo scores quickly and accurately. Mara W. Samson, one of the Arnis Girls, supported the idea and encouraged the development of the tool.\\n\\nFrom there, Bastonero Calculator began to take shape. Hairie developed the application while Icon Jules F. Descallar served as its tester and scoring validator, repeatedly checking the app's behavior and computation accuracy and providing feedback for corrections and improvements.\\n\\nThrough repeated testing, refinement, and real competition-based feedback, the app continued to evolve until it became a complete scoring and ranking tool designed for practical Arnis Anyo competition use.",11,TEXT,false);
        story.setLineSpacing(0,1.12f);storyPanel.addView(story);'''
s = s[:story_start] + new_story + s[story_end:]

# Expand the Chaperon panel with Leonila M. Umpad as Fellow Coach - Arnis Boys.
old_chap = '''        LinearLayout chap=aboutSection("CHAPERON",R.drawable.ic_person);
        TextView chapName=text("Analyn F. Patacsil",16,WHITE,true);chapName.setPadding(0,dp(7),0,0);chap.addView(chapName);
        TextView chapBody=text("With appreciation for her support and assistance to the Arnis Girls during their activities and competitions.",10,MUTED,false);
        chapBody.setPadding(0,dp(5),0,0);chap.addView(chapBody);page.addView(chap,fullMargins(0,0,0,dp(12)));'''
new_chap = '''        LinearLayout chap=aboutSection("CHAPERON",R.drawable.ic_group);
        TextView chapName=text("Analyn F. Patacsil",16,WHITE,true);chapName.setPadding(0,dp(7),0,0);chap.addView(chapName);
        TextView chapRole=text("Chaperon",10,GOLD_2,true);chapRole.setPadding(0,dp(2),0,0);chap.addView(chapRole);
        View chapDivider=divider();LinearLayout.LayoutParams chapDivP=new LinearLayout.LayoutParams(-1,dp(1));chapDivP.setMargins(0,dp(10),0,dp(8));chap.addView(chapDivider,chapDivP);
        TextView coachName=text("Leonila M. Umpad",16,WHITE,true);chap.addView(coachName);
        TextView coachRole=text("Fellow Coach - Arnis Boys",10,GOLD_2,true);coachRole.setPadding(0,dp(2),0,0);chap.addView(coachRole);
        TextView chapBody=text("With appreciation for their support and assistance to the Arnis Girls during their activities and competitions.",10,MUTED,false);
        chapBody.setPadding(0,dp(9),0,0);chap.addView(chapBody);page.addView(chap,fullMargins(0,0,0,dp(12)));'''
if old_chap not in s:
    raise SystemExit('TEST 22 Chaperon panel marker missing')
s = s.replace(old_chap, new_chap, 1)

# Use a people icon for App Tester & Scoring Validation.
old_tester = '        LinearLayout tester=aboutSection("APP TESTER & SCORING VALIDATION",R.drawable.ic_check);'
new_tester = '        LinearLayout tester=aboutSection("APP TESTER & SCORING VALIDATION",R.drawable.ic_group);'
if old_tester not in s:
    raise SystemExit('TEST 22 tester icon marker missing')
s = s.replace(old_tester, new_tester, 1)

SRC.write_text(s,encoding='utf-8')
print('TEST 22 Developer Information, circular portrait, acknowledgments, and revised story applied')
