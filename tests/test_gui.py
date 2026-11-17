"""Headless checks for the real Qt widgets; requires the project dependencies."""

import importlib.util
import os
import unittest
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
QT_AVAILABLE = importlib.util.find_spec("PyQt6") is not None

if QT_AVAILABLE:
    from PyQt6.QtWidgets import QApplication
    from pangolin.app import MainWindow


@unittest.skipUnless(QT_AVAILABLE, "Install project dependencies to test the GUI")
class GuiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.window = MainWindow()

    def tearDown(self):
        self.window.close()
        self.window.deleteLater()
        self.app.processEvents()

    def test_navigation_generation_and_copy(self):
        page = self.window.mainPage
        self.assertFalse(page.copyButton.isEnabled())
        page.wordsButton.click()
        self.assertEqual(self.window.pages.currentIndex(), 1)
        self.window.dictPage.backButton.click()
        self.assertEqual(self.window.pages.currentIndex(), 0)
        page.generateButton.click()
        password = page.passwordLabel.text()
        self.assertGreaterEqual(len(password), page.lengthSpin.value())
        self.assertTrue(any(c.isupper() for c in password))
        self.assertTrue(any(c.isdigit() for c in password))
        self.assertTrue(page.copyButton.isEnabled())
        page.copyButton.click()
        self.assertEqual(self.app.clipboard().text(), password)

    def test_add_edit_delete_and_empty_input(self):
        page = self.window.dictPage
        original = page.wordList.words()
        page.wordInput.setText("   ")
        page.addButton.click()
        self.assertEqual(page.wordList.words(), original)
        page.wordInput.setText("  pangolin  ")
        page.addButton.click()
        self.assertEqual(page.wordList.words()[-1], "pangolin")
        self.assertEqual(page.wordInput.text(), "")
        row = page.wordList.rowsLayout.itemAt(len(original)).widget()
        with patch("pangolin.wordlist.QInputDialog.getText", return_value=("armadillo", True)):
            row.editButton.click()
        self.assertEqual(page.wordList.words()[-1], "armadillo")
        row.deleteButton.click()
        self.assertEqual(page.wordList.words(), original)

    def test_empty_word_bank_has_a_clear_error(self):
        word_list = self.window.dictPage.wordList
        while word_list.rowsLayout.count():
            word_list.removeWord(word_list.rowsLayout.itemAt(0).widget())
        with patch("pangolin.app.QMessageBox.warning") as warning:
            self.window.mainPage.generateButton.click()
        self.assertEqual(warning.call_count, 1)
        self.assertIn("at least one word", warning.call_args.args[2])
        self.assertFalse(self.window.mainPage.copyButton.isEnabled())


if __name__ == "__main__":
    unittest.main()
