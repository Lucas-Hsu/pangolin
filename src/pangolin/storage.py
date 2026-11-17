"""Atomic encrypted saving, with migration from the earlier JSON word bank."""
import json
import os
from pathlib import Path
import tempfile

from cryptography.fernet import InvalidToken
from .encryption import make_cipher


class WordBankStore:
    def __init__(self, path, legacy_path=None):
        self.path = Path(path)
        self.legacy_path = Path(legacy_path) if legacy_path is not None else self.path.with_suffix('.json')
        self.cipher = make_cipher()

    @staticmethod
    def _words(data):
        if not isinstance(data, list) or any(not isinstance(word, str) for word in data):
            raise ValueError('The saved word bank must contain a list of words.')
        return [word.strip() for word in data if word.strip()]

    def load(self):
        try:
            token = self.path.read_bytes()
        except FileNotFoundError:
            try:
                words = self._words(json.loads(self.legacy_path.read_text(encoding='utf-8')))
            except FileNotFoundError:
                return []
            self.save(words)
            return words
        try:
            return self._words(json.loads(self.cipher.decrypt(token).decode('utf-8')))
        except (InvalidToken, UnicodeError, json.JSONDecodeError) as exc:
            raise ValueError('The saved data cannot be decrypted or is damaged.') from exc

    def save(self, words):
        words = self._words(words)
        token = self.cipher.encrypt(json.dumps(words, ensure_ascii=False).encode('utf-8'))
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(mode='wb', dir=self.path.parent, delete=False) as file:
                temporary = Path(file.name)
                file.write(token)
            os.replace(temporary, self.path)
            if self.legacy_path != self.path:
                self.legacy_path.unlink(missing_ok=True)
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)

    def clear(self):
        self.path.unlink(missing_ok=True)
        if self.legacy_path != self.path:
            self.legacy_path.unlink(missing_ok=True)
