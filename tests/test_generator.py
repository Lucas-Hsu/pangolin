import itertools
import unittest

from pangolin.generator import DEFAULT_DIGITS, SYMBOLS, digit_bank_from_answers, generate


class GeneratorTests(unittest.TestCase):
    def test_digit_bank_reads_new_and_legacy_answer_orders(self):
        answers = ['violet', 'pangolin', 'Mochi', '67', '007', '2026',
                   'noodles', 'waltz', 'song', 'tea', 'painting', 'curious', 'explore', 'moon']
        self.assertEqual(digit_bank_from_answers(answers), ('67', '007', '2026'))
        legacy = answers[:4] + answers[6:]
        self.assertEqual(digit_bank_from_answers(legacy), ('67',))
        self.assertEqual(digit_bank_from_answers(['violet']), DEFAULT_DIGITS)

    def test_requested_length_and_character_classes(self):
        for upper, digits, symbols in itertools.product((False, True), repeat=3):
            for length in (1, 8, 16, 64, 256):
                with self.subTest(upper=upper, digits=digits, symbols=symbols, length=length):
                    password = generate(["apple", "banana"], [7, 11], length,
                                        upper, digits, symbols)
                    self.assertGreaterEqual(len(password), length)
                    self.assertEqual(any(c.isupper() for c in password), upper)
                    self.assertEqual(any(c.isdigit() for c in password), digits)
                    self.assertEqual(any(c in SYMBOLS for c in password), symbols)

    def test_whole_words_are_not_truncated(self):
        self.assertEqual(generate(["banana"], minimumLength=8,
                                  needUppercase=False, needDigits=False,
                                  needSymbols=False), "bananabanana")

    def test_empty_and_blank_lists_fail_instead_of_looping(self):
        for bank in ([], ["", "   "]):
            with self.subTest(bank=bank), self.assertRaises(ValueError):
                generate(bank)

    def test_invalid_minimum_lengths(self):
        for length in (0, -1, 257, 2.5, "16", True):
            with self.subTest(length=length), self.assertRaises(ValueError):
                generate(["apple"], minimumLength=length)

    def test_blank_entries_are_ignored(self):
        self.assertEqual(generate([" ", " a ", ""], minimumLength=3,
                                  needUppercase=False, needDigits=False,
                                  needSymbols=False), "aaa")

    def test_uppercase_can_be_met_with_a_number_only_word_bank(self):
        self.assertTrue(any(c.isupper() for c in generate(["123"])))

    def test_invalid_number_banks(self):
        for bank in ([], [-1], ["abc"], [""]):
            with self.subTest(bank=bank), self.assertRaises(ValueError):
                generate(["apple"], bank, needDigits=True)


if __name__ == "__main__":
    unittest.main()
