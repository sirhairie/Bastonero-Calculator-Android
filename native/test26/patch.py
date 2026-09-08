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


# TEST 26 identity. Preserve TEST 25 HD export, TEST 23 About, and result-lock workflow.
s = s.replace('TEST 25', 'TEST 26').replace('bastonero_native_t25', 'bastonero_native_t26')
s = s.replace('// TEST 26 Ranking-Matched Medal + 2X HD Result Export',
              '// TEST 26 Tie-Break Ranking Precision Fix', 1)

# Fix official ranking order for mathematically equal displayed Final Scores.
# Example: 9.5+9.5+9.6 can be represented as 28.6 while
# 9.7+9.7+9.7-0.5 can be represented as 28.599999999999998.
# Comparing raw doubles incorrectly puts the former ahead before tie-breaking.
# Normalize Final Score and 5-Judge Total to hundredths before all ranking decisions.
replace_method('    private ArrayList<ResultRow> analyze(Competition c){', '''    private ArrayList<ResultRow> analyze(Competition c){
        ArrayList<ResultRow> rows=new ArrayList<>();
        for(Entry e:c.entries){
            ScoreData d=lockedScoreData(e);
            if(d.complete){ResultRow r=new ResultRow();r.entry=e;r.data=d;rows.add(r);}
        }

        // Official ordering: Final Score first, then 5-Judge Total for a Final Score tie.
        // Integer hundredths eliminate binary floating-point artifacts from changing placement.
        rows.sort((a,b)->{
            long aNet=Math.round(a.data.net*100.0);
            long bNet=Math.round(b.data.net*100.0);
            int byFinal=Long.compare(bNet,aNet);
            if(byFinal!=0)return byFinal;
            long aFive=Math.round(a.data.fiveTotal*100.0);
            long bFive=Math.round(b.data.fiveTotal*100.0);
            return Long.compare(bFive,aFive);
        });

        String lastExact=null;int lastRank=0;
        for(int i=0;i<rows.size();i++){
            ResultRow x=rows.get(i);
            long xNet=Math.round(x.data.net*100.0);
            long xFive=Math.round(x.data.fiveTotal*100.0);
            String key=xNet+"|"+xFive;
            x.rank=key.equals(lastExact)?lastRank:i+1;lastExact=key;lastRank=x.rank;

            int sameFinal=0,sameExact=0;
            long highestFive=Long.MIN_VALUE;
            for(ResultRow y:rows){
                long yNet=Math.round(y.data.net*100.0);
                long yFive=Math.round(y.data.fiveTotal*100.0);
                if(yNet==xNet){
                    sameFinal++;
                    highestFive=Math.max(highestFive,yFive);
                    if(yFive==xFive)sameExact++;
                }
            }

            if(sameExact>1){
                x.status="REPEAT PERFORMANCE";x.accent=RED;
                x.detail="Final score and 5-judge total are still tied. Repeat performance is required.";
            }else if(sameFinal>1&&xFive==highestFive){
                x.status="TIE-BREAK WINNER";x.accent=BLUE_2;
                x.detail="Final score tied. Won the tie-break with the higher 5-judge total of "+fmt(x.data.fiveTotal)+".";
            }else if(sameFinal>1){
                x.status="TIE-BREAK APPLIED";x.accent=BRONZE;
                x.detail="Final score tied. Ranked by the 5-judge total of "+fmt(x.data.fiveTotal)+".";
            }else{
                x.status="RANKED";x.accent=GREEN;
                x.detail="Valid Score "+fmt(x.data.score)+" minus penalty "+fmt1(x.data.penalty)+" gives Final Score "+fmt(x.data.net)+".";
            }
        }
        return rows;
    }''', 'TEST 26 normalized tie-break ranking')

SRC.write_text(s,encoding='utf-8')
print('TEST 26 tie-break ranking precision fix applied')
