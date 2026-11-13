from PyQt6.QtWidgets import *
from pangolin.wordlist import Dictpage
from pangolin.mainpage import Mainpage
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pangolin")

        self.layout = QStackedLayout()

        main = Mainpage()
        main.dictionary.clicked.connect(self.page(1))
        dict = Dictpage()
        dict.back.clicked.connect(self.page(0))

        self.layout.addWidget(main)
        self.layout.addWidget(dict)

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
    window.show()
    app.exec()

if __name__ == "__main__":
    main()
