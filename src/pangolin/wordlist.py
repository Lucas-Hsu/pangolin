from PyQt6.QtWidgets import *

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
        self.setFixedHeight(200)


class DictPage(QWidget):
    def __init__(self):
        super().__init__()
        self.backButton = QPushButton("<")
        self.wordInput = QLineEdit()
        self.addButton = QPushButton("Add Word")
        self.wordList = WordList(["test" for i in range(5)])
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
        self.wordList.layout.addRow(Row(self.wordInput.text()))

