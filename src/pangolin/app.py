"""Qt application and connections between the existing pages."""

import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QStackedWidget

from .generator import generate
from .mainpage import MainPage
from .wordlist import DictPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pangolin")
        self.resize(540, 280)
        self.mainPage = MainPage()
        self.dictPage = DictPage()
        self.pages = QStackedWidget()
        self.pages.addWidget(self.mainPage)
        self.pages.addWidget(self.dictPage)
        self.setCentralWidget(self.pages)

        self.mainPage.wordsButton.clicked.connect(self.page(1))
        self.mainPage.generateButton.clicked.connect(self.generate)
        self.mainPage.copyButton.clicked.connect(self.copyPassword)
        self.dictPage.backButton.clicked.connect(self.page(0))

    def page(self, index):
        def switch():
            self.pages.setCurrentIndex(index)
        return switch

    def generate(self):
        try:
            password = generate(
                self.dictPage.wordList.words(),
                minimumLength=self.mainPage.lengthSpin.value(),
                needUppercase=self.mainPage.capitalCheck.isChecked(),
                needDigits=self.mainPage.numbersCheck.isChecked(),
                needSymbols=self.mainPage.specialCheck.isChecked(),
            )
        except ValueError as exc:
            QMessageBox.warning(self, "Cannot generate password", str(exc))
            return
        self.mainPage.passwordLabel.setText(password)
        self.mainPage.copyButton.setEnabled(True)

    def copyPassword(self):
        QApplication.clipboard().setText(self.mainPage.passwordLabel.text())


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Pangolin")
    window = MainWindow()
    window.show()
    return app.exec()
