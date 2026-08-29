from pathlib import Path

SRC = Path('native/app/src/main/java/com/bastonero/calculator/nativeapp/MainActivity.java')
s = SRC.read_text(encoding='utf-8')

bad = 'current.matches("\\d{4}-\\d{2}-\\d{2}")'
good = 'current.matches("\\\\d{4}-\\\\d{2}-\\\\d{2}")'
if bad not in s:
    raise SystemExit('TEST 9 date regex escape target not found')
s = s.replace(bad, good, 1)
SRC.write_text(s, encoding='utf-8')
print('TEST 9 Java regex escaping fixed')
