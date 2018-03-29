from collections import OrderedDict
import json
import re
import sys

def replace_combining_chars(s):
    s = s.replace('א\u05B7', 'אַ')
    s = s.replace('א\u05B8', 'אָ')
    s = s.replace('ב\u05BC', 'בּ')
    s = s.replace('ב\u05BF', 'בֿ')
    s = s.replace('ו\u05BC', 'וּ')
    s = s.replace('ו\u05B9', 'וֹ')
    s = s.replace('ו\u05BA', 'וֹ')
    s = s.replace('י\u05B4', 'יִ')
    s = s.replace('יי\u05B7', 'ײַ')
    s = s.replace('ײ\u05B7', 'ײַ')
    s = s.replace('כ\u05BC', 'כּ')
    s = s.replace('פ\u05BC', 'פּ')
    s = s.replace('פ\u05BF', 'פֿ')
    s = s.replace('ש\u05C2', 'שׂ')
    s = s.replace('ת\u05BC', 'תּ')
    return s

def combine_entries(entry1, entry2):
    newEntry = {}
    newEntry['eng'] = list(OrderedDict.fromkeys(entry1['eng'] + entry2['eng']))
    newEntry['pronunciation'] = list(OrderedDict.fromkeys(entry1['pronunciation'] + entry2['pronunciation']))
    newEntry['pos'] = list(OrderedDict.fromkeys(entry1['pos'] + entry2['pos']))
    return newEntry

if __name__ == '__main__':
    # load the json into an object
    j = json.load(open(sys.argv[1], encoding='utf-8'))

    # normalize yiddish strings
    for yiddish in j.copy():
        new_yiddish = replace_combining_chars(yiddish)
        if new_yiddish not in j:
            j[new_yiddish] = j[yiddish]
            j.pop(yiddish, None)
        elif new_yiddish != yiddish:
            j[new_yiddish] = combine_entries(j[yiddish], j[new_yiddish])
            j.pop(yiddish, None)

    # remove the empty key
    j.pop('', None)

    # output the json back to a file
    json.dump(j, open(sys.argv[2], 'w', encoding='utf-8'), ensure_ascii=False, indent=4, sort_keys=True)
