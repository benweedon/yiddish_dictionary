import json
import re
import sys

from utils import combine_entries

def replace_combining_chars(s):
    s = s.replace('א\u05B7', 'אַ')
    s = s.replace('א\u05B8', 'אָ')
    s = s.replace('ב\u05BC', 'בּ')
    s = s.replace('ב\u05BF', 'בֿ')
    s = s.replace('ו\u05BC', 'וּ')
    s = s.replace('ו\u05B9', 'וֹ')
    s = s.replace('ו\u05BA', 'וֹ')
    s = s.replace('וו', 'װ');
    s = s.replace('וי', 'ױ');
    s = s.replace('י\u05B4', 'יִ')
    s = s.replace('יי', 'ײ');
    s = s.replace('יי\u05B7', 'ײַ')
    s = s.replace('ײ\u05B7', 'ײַ')
    s = s.replace('כ\u05BC', 'כּ')
    s = s.replace('פ\u05BC', 'פּ')
    s = s.replace('פ\u05BF', 'פֿ')
    s = s.replace('ש\u05C2', 'שׂ')
    s = s.replace('ת\u05BC', 'תּ')
    return s

if __name__ == '__main__':
    # load the json into an object
    d = json.load(open(sys.argv[1], encoding='utf-8'))

    # normalize yiddish strings
    for yiddish in d.copy():
        new_yiddish = replace_combining_chars(yiddish)
        if new_yiddish not in d:
            d[new_yiddish] = d[yiddish]
            d.pop(yiddish, None)
        elif new_yiddish != yiddish:
            d[new_yiddish] = combine_entries(d[yiddish], d[new_yiddish])
            d.pop(yiddish, None)

    # remove the empty key
    d.pop('', None)

    # output the json back to a file
    json.dump(d, open(sys.argv[2], 'w', encoding='utf-8'), ensure_ascii=False, indent=4, sort_keys=True)
