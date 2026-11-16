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

        layout.addWidget(self.deleteButton, 1)
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

    def rebuildList(self, words):
        self.layout = QFormLayout()
        self.setup(words)


class DictPage(QWidget):
    def __init__(self):
        super().__init__()
        self.backButton = QPushButton("<")
        self.wordInput = QLineEdit()
        self.addButton = QPushButton("Add Word")

        self.words = []
        try:
            with open(WORDFILE, 'r') as file:
                self.words = [line for line in file]
        except:
            print(f"could not find {WORDFILE}, creating.", file = sys.stderr)
        self.wordList = WordList(self.words)
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

    def writeWords(self):
        try:
            with open(WORDFILE, 'w') as file:
                for word in self.words:
                    file.write(word + "\n")
        except:
            sys.exit(f"could not read {WORDFILE}!")

    def connectRows(self):
        for i in range(self.wordList.layout.count()):
            self.wordList.layout.itemAt(i).widget().editButton.clicked.connect(self.editWord(i))
            self.wordList.layout.itemAt(i).widget().deleteButton.clicked.connect(self.deleteWord(i))

    def rebuildList(self):
        self.wordList.rebuildList(self.words)
        self.connectRows()

    def addWord(self):
        word = self.wordInput.text()
        if not word.strip(): 
            return
        self.words.append(word)
        self.writeWords()
        self.rebuildList()

    def deleteWord(self, idx):
        def dw():
            self.wordList.layout.removeRow(idx)
            self.words.pop(idx)
            self.writeWords()
            self.rebuildList()
        return dw

    def editWord(self, idx):
        def cw():
            word = self.wordInput.text()
            if not word.strip(): 
                return
            self.wordList.layout.itemAt(idx).widget().wordLabel.setText(word)
            self.words[idx] = word
            self.writeWords()
            self.rebuildList()
        return cw

