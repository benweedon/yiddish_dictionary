from collections import OrderedDict
import io
import json
from normalize import normalize
import os
import re
import sys

import utils

# if running on Windows, enable ANSI control sequences
if os.name == 'nt':
    import ctypes
    handle = ctypes.windll.kernel32.GetStdHandle(-11)
    ctypes.windll.kernel32.SetConsoleMode(handle, 7)

with open('sources.json', encoding='utf-8') as f:
    sources = json.load(f)

num_lines = None

errors = 0
warnings = 0

def fail(msg):
    print(msg, file=sys.stderr)
    sys.exit(1)

def error(msg, line):
    width = len(str(num_lines))
    print('{:>{width}}: \033[91m{}\033[0m'.format(line, msg, width=width), file=sys.stderr)
    global errors
    errors += 1

def warn(msg, line):
    width = len(str(num_lines))
    print('{:>{width}}: \033[93m{}\033[0m'.format(line, msg, width=width), file=sys.stderr)
    global warnings
    warnings += 1

def get_line_increment(entry):
    lines = 2
    for key in ['_pos', '_pro', '_src', 'eng', 'fra']:
        if key in entry:
            lines += 1
            if len(entry[key]) > 0:
                lines += 1 + len(entry[key])
    return lines

def validate_sources(entry, line):
    global sources
    line += 3
    if len(entry['_pos']) > 0:
        line += 1 + len(entry['_pos'])
    if len(entry['_pro']) > 0:
        line += 1 + len(entry['_pro'])
    if ('_src' not in entry) or (len(entry['_src'])==0):
        error('Entry does not have a source', line)
    else:
        for src in entry['_src']:
            line += 1
            if src not in sources:
                error('Source is not listed in sources.json', line)

def validate_no_punctuation(yiddish, line):
    punctuation = r'[`~!@#$%^&*()\-_+={}[\]\\|;:''"<>,./?־\u2000-\u206F\u2E00-\u2E7F]';
    if re.match(punctuation, yiddish) is not None:
        warn('Yiddish string contains punctuation', line)

if __name__ == '__main__':
    output = io.StringIO()
    with open(sys.argv[1], encoding='utf-8') as f:
        # get the number of lines in the file
        num_lines = sum(1 for line in f)

        # check that the file is normalized
        f.seek(0)
        normalize(f, output)
        f.seek(0)
        fileContents = f.read()
        # strip trailing newlines
        if fileContents[-1] == '\n':
            fileContents = fileContents[:-1]
        if output.getvalue() != fileContents:
            fail('The file isn\'t normalized. Run normalize.py and try again!')

        # perform all other validation
        f.seek(0)
        d = OrderedDict(sorted(json.load(f).items(), key=lambda i: utils.sort_yiddish(i[0])))
        line = 2
        for yiddish in d:
            validate_no_punctuation(yiddish, line)
            validate_sources(d[yiddish], line)
            line += get_line_increment(d[yiddish])

    if errors > 0 or warnings > 0:
        print()

    print('errors: {}, warnings: {}'.format(errors, warnings));

    if errors > 0:
        fail('Dictionary is not valid.')
