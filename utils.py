from collections import OrderedDict

def combine_entries(entry1, entry2):
    newEntry = {}
    newEntry['eng'] = list(OrderedDict.fromkeys(entry1['eng'] + entry2['eng']))
    newEntry['_pro'] = list(OrderedDict.fromkeys(entry1['_pro'] + entry2['_pro']))
    newEntry['_pos'] = list(OrderedDict.fromkeys(entry1['_pos'] + entry2['_pos']))
    return newEntry
