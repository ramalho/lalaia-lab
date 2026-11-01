#!/usr/bin/env python3
"""Exibe caracteres Unicode cujos nomes contêm todas as palavras dadas.

Uso: cf.py PALAVRA [PALAVRA ...]

Exemplo:
    $ ./cf.py cat smiling
    U+1F638	😸	GRINNING CAT FACE WITH SMILING EYES
    U+1F63A	😺	SMILING CAT FACE WITH OPEN MOUTH
    U+1F63B	😻	SMILING CAT FACE WITH HEART-SHAPED EYES
"""

import re
import sys
import unicodedata

WORD_SEP = re.compile(r'[\s-]+')


def find(*query_words, start=0, end=sys.maxunicode + 1):
    query = {w.upper() for w in query_words}
    for code in range(start, end):
        char = chr(code)
        name = unicodedata.name(char, None)
        if name and query.issubset(WORD_SEP.split(name)):
            yield code, char, name


def main(words):
    if not words:
        print(__doc__.strip(), file=sys.stderr)
        sys.exit(2)
    for code, char, name in find(*words):
        print(f'U+{code:04X}\t{char}\t{name}')


if __name__ == '__main__':
    main(sys.argv[1:])
