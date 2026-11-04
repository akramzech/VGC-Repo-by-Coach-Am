#!/bin/zsh
# finish.sh NAME DROP_AT : audio mix, check, render
cd "$(dirname $0)/$1" || exit 1
/usr/bin/python3 ../S2/short_audio.py $2 | tail -2
cd hf && npx --yes hyperframes@0.8.216 check --json 2>&1 | /usr/bin/python3 -c "
import sys,json
t=sys.stdin.read(); d=json.loads(t[t.find('{'):])
for k in ['lint','runtime','layout']: print(k,d[k]['errorCount'],d[k]['warningCount'])
for k in ['lint','runtime','layout']:
    for f in d[k]['findings']:
        if f['severity']=='error': print(k,f['code'],f.get('selector'),f.get('time'),f.get('message','')[:140])
"
