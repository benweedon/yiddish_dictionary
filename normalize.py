from collections import OrderedDict
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

def sort_yiddish(yiddish):
    yiddish_to_key = {
        'א': 'A',
        'אַ': 'B',
        'אָ': 'C',
        'ב': 'D',
        'בּ': 'E',
        'בֿ': 'F',
        'ג': 'G',
        'ד': 'H',
        'ה': 'I',
        'ו': 'J',
        'וּ': 'K',
        'וֹ': 'L',
        'װ': 'M',
        'ױ': 'N',
        'ז': 'O',
        'ח': 'P',
        'ט': 'Q',
        'י': 'R',
        'יִ': 'S',
        'ײ': 'T',
        'ײַ': 'U',
        'כּ': 'V',
        'כ': 'W',
        'ך': 'X',
        'ל': 'Y',
        'מ': 'Z',
        'ם': 'a',
        'נ': 'b',
        'ן': 'c',
        'ס': 'd',
        'ע': 'e',
        'פ': 'f',
        'פּ': 'g',
        'פֿ': 'h',
        'ף': 'i',
        'צ': 'j',
        'ץ': 'k',
        'ק': 'l',
        'ר': 'm',
        'ש': 'n',
        'שׂ': 'o',
        'תּ': 'p',
        'ת': 'q',
    }
    key = ''
    for char in yiddish:
        if char in yiddish_to_key:
            key += yiddish_to_key[char]
        else:
            key += char
    return key

def normalize(input, output):
    # load the json into an object
    d = json.load(input)

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

    # sort the dictionary
    d = OrderedDict(sorted(d.items(), key=lambda i: sort_yiddish(i[0])))

    # output the json
    json.dump(d, output, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    with open(sys.argv[1], encoding='utf-8') as input, open(sys.argv[2], 'w', encoding='utf-8') as output:
        normalize(input, output)
