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

errors = 0
warnings = 0

def fail(msg):
    print(msg, file=sys.stderr)
    print()
    print('This file is not valid :(')
    sys.exit(1)

def error(msg, line):
    print('{}: \033[91m{}\033[0m'.format(line, msg), file=sys.stderr)
    global errors
    errors += 1

def warn(msg, line):
    print('{}: \033[93m{}\033[0m'.format(line, msg), file=sys.stderr)
    global warnings
    warnings += 1

def get_line_increment(entry):
    lines = 5
    for key in ['_pro', '_pos', 'eng']:
        if len(entry[key]) > 0:
            lines += 1 + len(entry[key])
    return lines

def validate_no_punctuation(yiddish, line):
    punctuation = r'[`~!@#$%^&*()\-_+={}[\]\\|;:''"<>,./?־\u2000-\u206F\u2E00-\u2E7F]';
    if re.match(punctuation, yiddish) is not None:
        warn('Yiddish string contains punctuation', line)

if __name__ == '__main__':
    output = io.StringIO()
    with open(sys.argv[1], encoding='utf-8') as f:
        # check that the file is normalized
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
            line += get_line_increment(d[yiddish])

    if errors > 0 or warnings > 0:
        print()

    print('errors: {}, warnings: {}'.format(errors, warnings));

    if errors > 0:
        fail('Dictionary is not valid.')
