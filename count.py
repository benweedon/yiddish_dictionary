import json
import sys

with open(sys.argv[1], encoding='utf-8') as f:
    d = json.load(f)

count = sum(1 for entry in d)
print(count)
