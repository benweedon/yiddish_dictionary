from collections import OrderedDict

def combine_entries(entry1, entry2):
    new_entry = {}
    new_entry['eng'] = list(OrderedDict.fromkeys(entry1['eng'] + entry2['eng']))
    new_entry['_pro'] = list(OrderedDict.fromkeys(entry1['_pro'] + entry2['_pro']))
    new_entry['_pos'] = list(OrderedDict.fromkeys(entry1['_pos'] + entry2['_pos']))
    new_entry['_src'] = list(OrderedDict.fromkeys(entry1['_src'] + entry2['_src']))
    return new_entry

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
