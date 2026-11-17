"""Three artwork screens: welcome, questions, and the password generator."""
import sys
from pathlib import Path

from PyQt6.QtCore import QEvent, QObject, QStandardPaths
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QStackedWidget

from .generator import digit_bank_from_answers, generate
from .mainpage import MainPage
from .questions import QuestionsPage
from .storage import WordBankStore
from .welcome import WelcomePage


class ToolTipFilter(QObject):
    def eventFilter(self, watched, event):
        return event.type() == QEvent.Type.ToolTip


class MainWindow(QMainWindow):
    def __init__(self, store=None):
        super().__init__()
        self.setWindowTitle('Pangolin')
        self.resize(960, 768)
        self.setMinimumSize(640, 512)
        self.toolTipFilter = ToolTipFilter(self)
        QApplication.instance().installEventFilter(self.toolTipFilter)
        self.store = store if store is not None else WordBankStore(
            Path(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppDataLocation))
            / 'words.enc'
        )
        try:
            self.words = self.store.load()
        except (OSError, ValueError) as exc:
            QMessageBox.warning(self, 'Cannot load saved data', str(exc))
            self.words = []
        self.lastCopiedPassword = ''
        self.welcomePage = WelcomePage()
        self.questionsPage = QuestionsPage()
        self.mainPage = MainPage()
        self.pages = QStackedWidget()
        for page in (self.welcomePage, self.questionsPage, self.mainPage):
            self.pages.addWidget(page)
        self.setCentralWidget(self.pages)
        self.welcomePage.setupButton.clicked.connect(self.showQuestions)
        self.questionsPage.sheet.answersSubmitted.connect(self.saveAnswers)
        self.mainPage.generateButton.generationRequested.connect(self.generatePassword)
        self.mainPage.copyButton.clicked.connect(self.copyPassword)
        self.mainPage.clearButton.clicked.connect(self.clearData)
        if self.words:
            self.showMain()
        else:
            self.pages.setCurrentWidget(self.welcomePage)

    def showQuestions(self):
        self.pages.setCurrentWidget(self.questionsPage)
        self.questionsPage.sheet.fields[0].setFocus()

    def saveAnswers(self, answers):
        try:
            self.store.save(answers)
        except (OSError, ValueError) as exc:
            QMessageBox.warning(self, 'Cannot save data', str(exc))
            return
        self.words = list(answers)
        self.questionsPage.reset()
        self.showMain()

    def showMain(self):
        self.pages.setCurrentWidget(self.mainPage)

    def generatePassword(self):
        numbers = digit_bank_from_answers(self.words)
        try:
            password = generate(
                self.words, numbers,
                minimumLength=self.mainPage.lengthSpin.value(),
                needUppercase=self.mainPage.capitalCheck.isChecked(),
                needDigits=self.mainPage.numbersCheck.isChecked(),
                needSymbols=self.mainPage.specialCheck.isChecked(),
            )
        except ValueError as exc:
            QMessageBox.warning(self, 'Cannot generate password', str(exc))
            return
        self.mainPage.setPassword(password)

    def copyPassword(self):
        password = self.mainPage.copyButton.password
        if not password:
            return
        clipboard = QApplication.clipboard()
        clipboard.setText(password)
        if clipboard.text() == password:
            self.lastCopiedPassword = password
            self.mainPage.copyButton.flashCopied()

    def clearData(self):
        try:
            self.store.clear()
        except OSError as exc:
            QMessageBox.warning(self, 'Cannot clear data', str(exc))
            return
        if self.lastCopiedPassword and QApplication.clipboard().text() == self.lastCopiedPassword:
            QApplication.clipboard().clear()
        self.lastCopiedPassword = ''
        self.words = []
        self.questionsPage.reset()
        self.mainPage.reset()
        self.pages.setCurrentWidget(self.welcomePage)


def main():
    app = QApplication(sys.argv)
    app.setApplicationName('Pangolin')
    window = MainWindow()
    window.show()
    return app.exec()
