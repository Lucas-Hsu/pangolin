from PyQt6.QtWidgets import *
from pangolin.definitions import *
import sys

class Row(QWidget):
    def __init__(self, text):
        super().__init__()

        self.wordLabel = QLabel(text)
        self.editButton = QPushButton("edit")
        self.deleteButton = QPushButton("delete")

        self.setup()

    def setup(self):
        layout = QHBoxLayout()
        self.setLayout(layout)

        layout.addWidget(self.deleteButton, 0)
        layout.addWidget(self.editButton, 1)
        layout.addWidget(self.wordLabel, 5)

class WordList(QScrollArea):
    def __init__(self, words):
        super().__init__()
        self.layout = QFormLayout()
        self.setup(words)

    def setup(self, words):
        for w in words:
            self.layout.addRow(Row(w))
        groupBox = QGroupBox()
        groupBox.setLayout(self.layout)
        self.setWidget(groupBox)
        self.setWidgetResizable(True)
        self.setFixedHeight(WINDOW_H)


class DictPage(QWidget):
    def __init__(self):
        super().__init__()
        self.backButton = QPushButton("<")
        self.wordInput = QLineEdit()
        self.addButton = QPushButton("Add Word")

        words = []
        try:
            with open(WORDFILE, 'r') as file:
                words = [line for line in file]
        except:
            sys.exit(f"could not read {WORDFILE}!")
        self.wordList = WordList(words)
        self.setup()

    def setup(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        top = QHBoxLayout()
        top.addWidget(self.backButton, 1)
        top.addWidget(self.wordInput, 5)
        top.addWidget(self.addButton, 1)
        topw = QWidget()
        topw.setLayout(top)

        layout.addWidget(topw)
        layout.addWidget(self.wordList)

    def addWord(self):
        word = self.wordInput.text()
        self.wordList.layout.addRow(Row(word))
        try:
            with open(WORDFILE, 'a') as file:
                file.write(word)
        except:
            sys.exit(f"could not read {WORDFILE}!")

