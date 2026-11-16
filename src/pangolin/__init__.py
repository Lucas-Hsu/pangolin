from PyQt6.QtWidgets import *
from pangolin.wordlist import *
from pangolin.mainpage import *
from pangolin.definitions import *
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.mainPage = MainPage()
        self.dictPage = DictPage()
        self.layout = QStackedLayout()
        self.clipboard = QApplication.clipboard()
        self.setup()

    def setup(self):
        self.setWindowTitle("Pangolin")
        self.setGeometry(0, 0, WINDOW_W, WINDOW_H)

        self.layout.addWidget(self.mainPage)
        self.layout.addWidget(self.dictPage)

        central = QWidget()
        central.setLayout(self.layout)
        self.setCentralWidget(central)

    def page(self, n):
        def switch():
            self.layout.setCurrentIndex(n)
        return switch

    def generate(self):
        words = [
            self.dictPage.wordList.layout.itemAt(i).widget().wordLabel.text() 
            for i in range(self.dictPage.wordList.layout.count())
        ]
        numbers = self.mainPage.numbersCheck.isChecked()
        capital = self.mainPage.capitalCheck.isChecked()
        special = self.mainPage.specialCheck.isChecked()
        length = self.mainPage.lengthSpin.value()

        # call the generate function here
        self.mainPage.passwordLabel.setText(f"{length} {numbers} {capital} {special} {words}")

    def copyPassword(self):
        self.clipboard.setText(self.mainPage.passwordLabel.text())

def main():
    app = QApplication(sys.argv)

    window = MainWindow()

    window.mainPage.wordsButton.clicked.connect(window.page(1))
    window.mainPage.generateButton.clicked.connect(window.generate)
    window.mainPage.copyButton.clicked.connect(window.copyPassword)

    window.dictPage.backButton.clicked.connect(window.page(0))
    window.dictPage.addButton.clicked.connect(window.dictPage.addWord)

    window.show()
    app.exec()

if __name__ == "__main__":
    main()
