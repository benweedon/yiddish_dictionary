import json
import sys

from utils import combine_entries

if __name__ == '__main__':
    with open(sys.argv[1], encoding='utf-8') as f1, open(sys.argv[2], encoding='utf-8') as f2:
        d1 = json.load(f1)
        d2 = json.load(f2)

    new_dict = d1
    for yiddish in d2:
        if yiddish not in new_dict:
            new_dict[yiddish] = d2[yiddish]
        else:
            new_dict[yiddish] = combine_entries(d2[yiddish], new_dict[yiddish])

    with open(sys.argv[3], 'w', encoding='utf-8') as f:
        json.dump(new_dict, f, ensure_ascii=False, indent=4, sort_keys=True)
