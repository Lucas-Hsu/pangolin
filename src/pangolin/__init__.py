from PyQt6.QtWidgets import *
from pangolin.wordlist import DictPage
from pangolin.mainpage import MainPage
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.mainPage = MainPage()
        self.dictPage = DictPage()
        self.layout = QStackedLayout()
        self.setup()

    def setup(self):
        self.setWindowTitle("Pangolin")

        self.layout.addWidget(self.mainPage)
        self.layout.addWidget(self.dictPage)

        central = QWidget()
        central.setLayout(self.layout)
        self.setCentralWidget(central)

    def page(self, n):
        def switch():
            self.layout.setCurrentIndex(n)
        return switch


def main():
    app = QApplication(sys.argv)

    window = MainWindow()

    window.mainPage.wordsButton.clicked.connect(window.page(1))

    # link generate button here (look at mainPage.changeLabel())
    # window.mainPage.generateButton.clicked.connect(SOME_FUNC)

    window.dictPage.backButton.clicked.connect(window.page(1))

    window.show()
    app.exec()

if __name__ == "__main__":
    main()
