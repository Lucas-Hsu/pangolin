import base64
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from pangolin.encryption import make_cipher
from pangolin.storage import WordBankStore


class StorageTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.store = WordBankStore(Path(temporary.name) / 'Pangolin' / 'words.enc')

    def test_first_launch_and_encrypted_round_trip(self):
        self.assertEqual(self.store.load(), [])
        answers = ['Ocean blue', '紫色', 'kitten']
        self.store.save(answers)
        self.assertEqual(WordBankStore(self.store.path).load(), answers)
        token = self.store.path.read_bytes()
        self.assertNotIn(b'Ocean blue', token)
        self.assertEqual(json.loads(make_cipher().decrypt(token)), answers)
        self.assertEqual(self.store.path.stat().st_mode & 0o777, 0o600)

    def test_legacy_json_migrates_and_plaintext_is_removed(self):
        self.store.legacy_path.parent.mkdir(parents=True)
        self.store.legacy_path.write_text('["blue", "kitten"]')
        self.assertEqual(self.store.load(), ['blue', 'kitten'])
        self.assertTrue(self.store.path.exists())
        self.assertFalse(self.store.legacy_path.exists())
        self.assertEqual(self.store.load(), ['blue', 'kitten'])

    def test_failed_write_does_not_replace_previous_bank(self):
        self.store.save(['violet'])
        old_token = self.store.path.read_bytes()
        with patch('pangolin.storage.os.replace', side_effect=OSError('disk full')):
            with self.assertRaises(OSError):
                self.store.save(['new answer'])
        self.assertEqual(self.store.path.read_bytes(), old_token)
        self.assertEqual(list(self.store.path.parent.iterdir()), [self.store.path])

    def test_corruption_and_invalid_data_are_reported(self):
        self.store.path.parent.mkdir(parents=True)
        for token in (b'invalid', make_cipher().encrypt(b'[1]'),
                      make_cipher().encrypt(b'{"words": []}')):
            self.store.path.write_bytes(token)
            with self.subTest(token=token), self.assertRaises(ValueError):
                self.store.load()

    def test_clear_removes_encrypted_and_legacy_data(self):
        self.store.save(['blue'])
        self.store.legacy_path.write_text('["old"]')
        self.store.clear()
        self.assertFalse(self.store.path.exists())
        self.assertFalse(self.store.legacy_path.exists())
        self.assertEqual(self.store.load(), [])

    def test_blank_words_are_empty(self):
        self.store.save(['', '   '])
        self.assertEqual(self.store.load(), [])


if __name__ == '__main__':
    unittest.main()
