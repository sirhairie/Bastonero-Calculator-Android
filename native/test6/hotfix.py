from pathlib import Path

SRC = Path('native/app/src/main/java/com/bastonero/calculator/nativeapp/MainActivity.java')
s = SRC.read_text(encoding='utf-8')

# patch.py intentionally creates a visual two-line title, but Java source needs an escaped newline.
bad_title = 'TextView title = text("Bastonero' + '\n' + 'Calculator",15,WHITE,true);'
good_title = r'TextView title = text("Bastonero\nCalculator",15,WHITE,true);'
if bad_title not in s:
    raise SystemExit('TEST 6 broken title string not found')
s = s.replace(bad_title, good_title, 1)

# Rebuild the custom About body as one valid Java string containing escaped newlines.
start = s.find('TextView body=text("TEST 6 Precision UI.')
if start < 0:
    raise SystemExit('TEST 6 About body start not found')
end_marker = '",12,TEXT,false);'
end = s.find(end_marker, start)
if end < 0:
    raise SystemExit('TEST 6 About body end not found')
end += len(end_marker)
new_body = (
    r'TextView body=text("TEST 6 Precision UI. Fully native Android interface and scoring engine—no WebView, HTML, CSS, or JavaScript.\n\n'
    r'VISUAL SYSTEM\n'
    r'• Responsive compact header\n'
    r'• Mockup-matched navy, royal blue, and metallic gold\n'
    r'• Custom Arnis and tournament vector icons\n'
    r'• Raised gradient cards and beveled controls\n'
    r'• Enhanced embossed medal ranking\n\n'
    r'SCORING\n'
    r'• Five judges, valid scores 7.0–10.0\n'
    r'• Remove highest and lowest\n'
    r'• Add the middle three scores\n'
    r'• Subtract official penalty\n'
    r'• Tied Final Score: use 5-judge total\n'
    r'• Still tied: Repeat Performance\n\n'
    r'DEVELOPER\n'
    r'Hairie A. Laysam\n'
    r'Sta. Maria National High School\n\n'
    r'Native v2.0 • TEST 6",12,TEXT,false);'
)
s = s[:start] + new_body + s[end:]

SRC.write_text(s, encoding='utf-8')
print('TEST 6 Java string escaping fixed')
