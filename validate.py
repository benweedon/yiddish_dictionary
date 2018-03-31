import io
from normalize import normalize
import sys

def fail_validation(msg):
    print(msg, file=sys.stderr)
    print()
    print('This file is not valid :(')
    sys.exit(1)

if __name__ == '__main__':
    output = io.StringIO()
    with open(sys.argv[1], encoding='utf-8') as f:
        normalize(f, output)
        f.seek(0)
        if output.getvalue() != f.read():
            fail_validation('The file isn\'t normalized. Run normalize.py and try again!')

    print('This file is valid! :)')
