#!/usr/bin/env python3
"""Localiza caracteres Unicode cujos nomes contêm todas as palavras dadas.

Uso:
    python3 charfinder.py palavra [palavra ...]

Cada palavra precisa coincidir com uma palavra inteira do nome — buscar
"cat" não traz, por exemplo, "REGIONAL INDICATOR SYMBOL LETTER A".

Exemplo:
    python3 charfinder.py latin capital letter a

A saída tem três campos separados por tabulação:
    1. código do caractere no formato U+XXXX;
    2. o próprio caractere;
    3. o nome oficial do caractere.

A busca ignora diferenças entre maiúsculas e minúsculas e não depende da
ordem das palavras. Caracteres sem nome oficial (não atribuídos, controles,
surrogates e área de uso privado) não aparecem no resultado.
"""

from __future__ import annotations

import argparse
import os
import sys
import unicodedata
from collections.abc import Iterable, Iterator


def find_characters(words: Iterable[str]) -> Iterator[tuple[int, str, str]]:
    """Gera (codepoint, caractere, nome) para cada caractere que casa.

    Um caractere casa quando *todas* as palavras aparecem como palavras
    inteiras em seu nome oficial (sem diferenciar maiúsculas de minúsculas).
    Os nomes são divididos em palavras por espaços e hífens.
    Os resultados são gerados em ordem de codepoint.
    """
    needles = {word.casefold() for word in words}
    for codepoint in range(sys.maxunicode + 1):
        character = chr(codepoint)
        name = unicodedata.name(character, None)
        if name is None:
            continue
        name_words = {word.casefold() for word in name.replace("-", " ").split()}
        if needles <= name_words:
            yield codepoint, character, name


def format_row(codepoint: int, character: str, name: str) -> str:
    """Formata uma linha com os três campos separados por tabulação."""
    return f"U+{codepoint:04X}\t{character}\t{name}"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="charfinder",
        description=(
            "Lista caracteres Unicode cujos nomes contêm todas as palavras "
            "fornecidas. A saída é tabulada em: código U+XXXX, caractere, nome."
        ),
    )
    parser.add_argument(
        "words",
        nargs="+",
        metavar="PALAVRA",
        help=(
            "palavra inteira que deve aparecer no nome do caractere "
            "(pode repetir)"
        ),
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    words = [word.strip() for word in args.words if word.strip()]
    if not words:
        parser.error("informe ao menos uma palavra")

    try:
        for codepoint, character, name in find_characters(words):
            print(format_row(codepoint, character, name))
    except BrokenPipeError:
        # Evita o erro de flush ao encerrar o pipe (ex.: `... | head`).
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stdout.fileno())
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
