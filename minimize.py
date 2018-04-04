import json
import sys

with open(sys.argv[1], encoding='utf-8') as f:
    d = json.load(f)

with open(sys.argv[2], 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, separators=(',',':'))
