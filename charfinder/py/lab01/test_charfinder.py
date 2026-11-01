#!/usr/bin/env python3
"""Testes do utilitário charfinder."""

import io
import unittest
from contextlib import redirect_stderr, redirect_stdout

import charfinder


class FormatRowTests(unittest.TestCase):
    def test_bmp_minimum_width(self):
        self.assertEqual(
            charfinder.format_row(0x41, "A", "LATIN CAPITAL LETTER A"),
            "U+0041\tA\tLATIN CAPITAL LETTER A",
        )

    def test_astral_codepoint_uses_five_hex_digits(self):
        self.assertEqual(
            charfinder.format_row(0x1F600, "😀", "GRINNING FACE"),
            "U+1F600\t😀\tGRINNING FACE",
        )


class FindCharactersTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = list(charfinder.find_characters(["latin", "capital", "letter", "a"]))
        cls.by_codepoint = {codepoint: (char, name) for codepoint, char, name in cls.rows}

    def test_finds_expected_character(self):
        self.assertEqual(
            self.by_codepoint[0x00C1],
            ("Á", "LATIN CAPITAL LETTER A WITH ACUTE"),
        )

    def test_requires_all_words(self):
        self.assertNotIn(0x0061, self.by_codepoint)  # LATIN SMALL LETTER A

    def test_results_are_sorted_by_codepoint(self):
        codepoints = [codepoint for codepoint, _, _ in self.rows]
        self.assertEqual(codepoints, sorted(codepoints))

    def test_is_case_insensitive(self):
        found = list(charfinder.find_characters(["SmIlInG", "FACE"]))
        self.assertIn((0x263A, "☺", "WHITE SMILING FACE"), found)

    def test_word_order_does_not_matter(self):
        a = list(charfinder.find_characters(["white", "smiling"]))
        b = list(charfinder.find_characters(["smiling", "white"]))
        self.assertEqual(a, b)

    def test_unknown_word_returns_nothing(self):
        self.assertEqual(list(charfinder.find_characters(["zzzznotaname"])), [])

    def test_matches_whole_words_only(self):
        found = list(charfinder.find_characters(["cat"]))
        codepoints = {codepoint for codepoint, _, _ in found}
        self.assertIn(0x1F431, codepoints)  # CAT FACE
        self.assertNotIn(0x1F1E6, codepoints)  # REGIONAL INDICATOR SYMBOL LETTER A


class MainTests(unittest.TestCase):
    def test_prints_tab_separated_rows(self):
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            exit_code = charfinder.main(["white", "smiling", "face"])

        self.assertEqual(exit_code, 0)
        self.assertIn("U+263A\t☺\tWHITE SMILING FACE\n", stdout.getvalue())

    def test_ignores_empty_words(self):
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            exit_code = charfinder.main(["", "white", "   ", "smiling"])

        self.assertEqual(exit_code, 0)
        self.assertIn("U+263A\t☺\tWHITE SMILING FACE\n", stdout.getvalue())

    def test_rejects_only_empty_words(self):
        with redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as ctx:
            charfinder.main(["", "   "])

        self.assertEqual(ctx.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
