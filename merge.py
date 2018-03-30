import json
import sys

from utils import combine_entries

if __name__ == '__main__':
    d1 = json.load(open(sys.argv[1], encoding='utf-8'))
    d2 = json.load(open(sys.argv[2], encoding='utf-8'))

    new_dict = d1
    for yiddish in d2:
        if yiddish not in new_dict:
            new_dict[yiddish] = d2[yiddish]
        else:
            new_dict[yiddish] = combine_entries(d2[yiddish], new_dict[yiddish])

    json.dump(new_dict, open(sys.argv[3], 'w', encoding='utf-8'), ensure_ascii=False, indent=4, sort_keys=True)
