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
        formwidget = QWidget()
        formwidget.setLayout(self.layout)
        self.setWidget(formwidget)

class DictPage(QWidget):
    def __init__(self):
        super().__init__()
        self.backButton = QPushButton("back")
        self.wordInput = QLineEdit()
        self.wordList = WordList(["foo", "bar"])
        self.setup()

    def setup(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        top = QHBoxLayout()
        top.addWidget(self.backButton, 1)
        top.addWidget(self.wordInput, 5)
        topw = QWidget()
        topw.setLayout(top)

        layout.addWidget(topw)
        layout.addWidget(self.wordList)

