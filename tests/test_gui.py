import importlib.util
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
QT_AVAILABLE = importlib.util.find_spec('PyQt6') is not None
if QT_AVAILABLE:
    from PyQt6.QtCore import QEvent
    from PyQt6.QtTest import QSignalSpy, QTest
    from PyQt6.QtWidgets import QApplication
    from pangolin.app import MainWindow
    from pangolin.questions import NUMBER_FIELD_INDICES, QUESTIONS
    from pangolin.storage import WordBankStore

ANSWERS = ['violet', 'pangolin', 'Mochi', '67', '007', '2026', 'noodles', 'waltz',
           'Moon River', 'tea', 'painting', 'curious', 'explore', 'moon']


@unittest.skipUnless(QT_AVAILABLE, 'Install the project dependencies to test Qt')
class GuiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])
        cls.app.setApplicationName('Pangolin')

    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.store = WordBankStore(Path(temporary.name) / 'words.enc')
        self.window = MainWindow(self.store)
        self.window.show()
        self.app.processEvents()

    def tearDown(self):
        self.window.close()
        self.window.deleteLater()
        self.app.processEvents()

    def complete_questions(self):
        self.window.welcomePage.setupButton.click()
        sheet = self.window.questionsPage.sheet
        for field, answer in zip(sheet.fields, ANSWERS):
            field.setText(answer)
        sheet.setupButton.click()
        self.app.processEvents()

    def test_welcome_questions_and_save(self):
        self.assertIs(self.window.pages.currentWidget(), self.window.welcomePage)
        self.window.welcomePage.setupButton.click()
        self.app.processEvents()
        self.assertIs(self.window.pages.currentWidget(), self.window.questionsPage)
        sheet = self.window.questionsPage.sheet
        self.assertEqual(len(sheet.fields), 14)
        self.assertEqual([(image.width(), image.height()) for image in sheet.bubbles],
                         [(769, 199), (781, 206), (792, 223)])
        self.assertEqual([label.text() for label in sheet.labels], list(QUESTIONS))
        self.assertFalse(sheet.setupButton.isEnabled())
        for field, answer in zip(sheet.fields[:-1], ANSWERS[:-1]):
            field.setText(answer)
        sheet.fields[-1].setText('   ')
        self.assertFalse(sheet.setupButton.isEnabled())
        sheet.fields[-1].setText('moon')
        self.assertTrue(sheet.setupButton.isEnabled())
        self.window.questionsPage.scroll.ensureWidgetVisible(sheet.setupButton)
        self.assertGreater(self.window.questionsPage.scroll.verticalScrollBar().value(), 0)
        sheet.setupButton.click()
        self.assertEqual(self.store.load(), ANSWERS)
        self.assertIs(self.window.pages.currentWidget(), self.window.mainPage)
        self.assertEqual(self.window.pages.count(), 3)

    def test_initial_instructions_and_separate_generate_and_copy(self):
        self.complete_questions()
        page = self.window.mainPage
        self.assertEqual(page.copyButton.password, '')
        self.assertIs(page.copyButton.image, page.copyButton.initialImage)
        self.app.clipboard().setText('leave this alone')
        page.copyButton.click()
        self.assertEqual(self.app.clipboard().text(), 'leave this alone')
        self.assertEqual(page.copyButton.flash, 0)
        page.lengthSpin.setValue(64)
        page.specialCheck.setChecked(True)
        spy = QSignalSpy(page.generateButton.generationRequested)
        page.generateButton.click()
        self.assertTrue(page.generateButton.isSpinning)
        QTest.qWait(180)
        self.assertGreater(page.generateButton.angle, 0)
        self.assertLess(page.generateButton.angle, 720)
        self.assertTrue(page.copyButton.password)
        previous_angle = page.generateButton.angle
        page.generateButton.click()
        self.assertEqual(page.generateButton.angle, previous_angle)
        self.assertEqual(len(spy), 2)
        QTest.qWait(1300)
        self.assertEqual(len(spy), 2)
        self.assertFalse(page.generateButton.isSpinning)
        self.assertAlmostEqual(page.generateButton.angle % 360, 0)
        self.assertGreaterEqual(page.generateButton.angle, previous_angle + 720)
        password = page.copyButton.password
        self.assertGreaterEqual(len(password), 64)
        self.assertTrue(any(c.isupper() for c in password))
        self.assertTrue(any(number in password for number in ('67', '007', '2026')))
        self.assertEqual(self.app.clipboard().text(), 'leave this alone')
        page.copyButton.click()
        self.assertEqual(self.app.clipboard().text(), password)
        self.assertGreater(page.copyButton.flash, 0)
        self.assertEqual(page.copyButton.password, password)
        QTest.qWait(780)
        self.assertAlmostEqual(page.copyButton.flash, 0)
        page.generateButton.click()
        QTest.qWait(1200)
        self.assertEqual(len(spy), 3)
        self.assertEqual(self.app.clipboard().text(), password)

    def test_three_digit_only_fields_and_number_bank(self):
        self.window.welcomePage.setupButton.click()
        sheet = self.window.questionsPage.sheet
        for index in NUMBER_FIELD_INDICES:
            field = sheet.fields[index]
            field.insert('abc')
            self.assertEqual(field.text(), '')
            field.insert('007')
            self.assertEqual(field.text(), '007')
            field.insert('x')
            self.assertEqual(field.text(), '007')
            field.selectAll()
            self.app.clipboard().setText('12.3')
            field.paste()
            self.assertEqual(field.text(), '007')
        for field, answer in zip(sheet.fields, ANSWERS):
            field.setText(answer)
        for index in NUMBER_FIELD_INDICES:
            for invalid in ('-1', '+1', '1.2', '1 2', ' 12', '１２', ''):
                sheet.fields[index].setText(invalid)
                self.assertFalse(sheet.setupButton.isEnabled())
                sheet.submit()
                self.assertFalse(self.store.path.exists())
            sheet.fields[index].setText(ANSWERS[index])
        self.assertTrue(sheet.setupButton.isEnabled())
        sheet.setupButton.click()
        self.assertEqual(self.store.load(), ANSWERS)
        with patch('pangolin.app.generate', return_value='testPassword007') as generate:
            self.window.mainPage.generateButton.click()
        self.assertEqual(generate.call_args.args[1], ('67', '007', '2026'))

    def test_fast_start_and_repeated_presses_keep_spinning(self):
        self.complete_questions()
        button = self.window.mainPage.generateButton
        from PyQt6.QtGui import QColor
        self.assertEqual(button.generateColor, QColor('#ff7474'))
        spy = QSignalSpy(button.generationRequested)
        button.click()
        self.assertEqual(len(spy), 1)
        self.assertGreater(button.angle, 0)
        button.spinAnimation.setCurrentTime(60)
        self.assertGreater(button.angle, 20)
        previous = button.angle
        for count in range(2, 7):
            QTest.qWait(200)
            self.assertTrue(button.isSpinning)
            self.assertGreater(button.angle, previous)
            previous = button.angle
            button.click()
            self.assertAlmostEqual(button.angle, previous)
            self.assertEqual(len(spy), count)
        self.assertTrue(button.isSpinning)
        QTest.qWait(1220)
        self.assertFalse(button.isSpinning)
        self.assertAlmostEqual(button.angle % 360, 0)
        self.assertGreaterEqual(button.angle, previous + 720)

    def test_reset_clears_saved_data_fields_and_own_clipboard(self):
        self.complete_questions()
        page = self.window.mainPage
        page.generateButton.click()
        QTest.qWait(1200)
        page.copyButton.click()
        page.generateButton.click()
        self.assertTrue(page.generateButton.isSpinning)
        page.clearButton.click()
        self.assertIs(self.window.pages.currentWidget(), self.window.welcomePage)
        self.assertEqual(self.store.load(), [])
        self.assertEqual(self.app.clipboard().text(), '')
        self.assertTrue(all(not field.text() for field in self.window.questionsPage.sheet.fields))
        self.assertEqual(page.copyButton.password, '')
        self.assertIs(page.copyButton.image, page.copyButton.initialImage)
        QTest.qWait(1200)
        self.assertFalse(page.generateButton.isSpinning)
        self.assertEqual(page.copyButton.password, '')

    def test_hover_and_click_feedback(self):
        self.complete_questions()
        page = self.window.mainPage
        controls = (page.generateButton, page.copyButton, page.capitalCheck,
                    page.numbersCheck, page.specialCheck, page.lengthSpin,
                    page.upButton, page.downButton, page.clearButton,
                    self.window.welcomePage.setupButton,
                    self.window.questionsPage.sheet.setupButton,
                    *self.window.questionsPage.sheet.fields,
                    self.window.questionsPage.scroll.verticalScrollBar())
        self.assertTrue(all(hasattr(control, 'feedback') for control in controls))
        checkbox = page.capitalCheck
        self.app.sendEvent(checkbox, QEvent(QEvent.Type.Enter))
        QTest.qWait(170)
        self.assertAlmostEqual(checkbox.feedback.effect.highlight, .12)
        self.app.sendEvent(checkbox, QEvent(QEvent.Type.Leave))
        QTest.qWait(170)
        self.assertAlmostEqual(checkbox.feedback.effect.highlight, 0)
        checkbox.click()
        QTest.qWait(45)
        self.assertGreater(checkbox.feedback.effect.scale, 1)
        QTest.qWait(260)
        self.assertAlmostEqual(checkbox.feedback.effect.scale, 1)
        self.assertFalse(page.clearButton.feedback.click_effect)
        self.assertFalse(self.window.welcomePage.setupButton.feedback.click_effect)

    def test_length_number_is_rendered_and_can_be_edited_or_stepped(self):
        self.complete_questions()
        page = self.window.mainPage
        editor = page.lengthSpin
        for size in ((640, 512), (1280, 1024)):
            self.window.resize(*size)
            self.app.processEvents()
            for value in (8, 16, 128, 256):
                editor.setValue(value)
                self.app.processEvents()
                image = editor.grab().toImage()
                yellow_pixels = sum(
                    1 for y in range(image.height()) for x in range(image.width())
                    if (image.pixelColor(x, y).red() > 180
                        and image.pixelColor(x, y).green() > 180
                        and image.pixelColor(x, y).blue() < 160)
                )
                self.assertGreater(yellow_pixels, 10, (size, value))
                self.assertEqual(editor.text(), str(value))
        editor.selectAll()
        editor.insert('32')
        self.assertEqual(editor.value(), 32)
        page.upButton.click()
        self.assertEqual(editor.text(), '33')
        page.downButton.click()
        self.assertEqual(editor.text(), '32')
        editor.setFocus()
        editor.clear()
        page.upButton.setFocus()
        self.app.processEvents()
        self.assertEqual(editor.text(), '32')

    def test_restart_skips_questions_and_reset_preserves_unrelated_clipboard(self):
        self.complete_questions()
        self.window.close()
        self.window = MainWindow(self.store)
        self.assertIs(self.window.pages.currentWidget(), self.window.mainPage)
        self.assertEqual(self.window.mainPage.copyButton.password, '')
        self.app.clipboard().setText('something else')
        self.window.mainPage.clearButton.click()
        self.assertEqual(self.app.clipboard().text(), 'something else')
        self.window.close()
        self.window = MainWindow(self.store)
        self.assertIs(self.window.pages.currentWidget(), self.window.welcomePage)

    def test_save_failure_stays_on_questions(self):
        self.window.welcomePage.setupButton.click()
        with patch.object(self.store, 'save', side_effect=OSError('disk full')):
            with patch('pangolin.app.QMessageBox.warning') as warning:
                self.window.saveAnswers(ANSWERS)
        self.assertTrue(warning.called)
        self.assertIs(self.window.pages.currentWidget(), self.window.questionsPage)

    def test_art_scales_without_stretching_and_tooltips_are_blocked(self):
        for size in ((640, 512), (1280, 1024), (1400, 800), (720, 1000)):
            self.window.resize(*size)
            self.app.processEvents()
            page = self.window.welcomePage
            geometry = page.setupButton.geometry()
            self.assertAlmostEqual(geometry.width() / geometry.height(), 696 / 188, delta=0.04)
            self.assertTrue(page.rect().contains(geometry))
        self.assertTrue(self.window.toolTipFilter.eventFilter(self.window, QEvent(QEvent.Type.ToolTip)))


if __name__ == '__main__':
    unittest.main()
