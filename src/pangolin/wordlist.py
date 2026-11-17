from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QHBoxLayout, QInputDialog, QLabel, QLineEdit, QMessageBox,
    QPushButton, QScrollArea, QVBoxLayout, QWidget,
)

from .generator import DEFAULT_WORDS


class Row(QWidget):
    removeRequested = pyqtSignal()

    def __init__(self, text):
        super().__init__()
        self.wordLabel = QLabel(text)
        self.wordLabel.setTextFormat(Qt.TextFormat.PlainText)
        self.editButton = QPushButton("Edit")
        self.deleteButton = QPushButton("Delete")
        layout = QHBoxLayout(self)
        layout.addWidget(self.deleteButton)
        layout.addWidget(self.editButton)
        layout.addWidget(self.wordLabel, 1)
        self.editButton.clicked.connect(self.editWord)
        self.deleteButton.clicked.connect(lambda checked=False: self.removeRequested.emit())

    def editWord(self):
        text, accepted = QInputDialog.getText(
            self, "Edit word", "Word:", text=self.wordLabel.text()
        )
        if accepted:
            text = text.strip()
            if not text:
                QMessageBox.warning(self, "Empty word", "Enter a word first.")
                return
            self.wordLabel.setText(text)


class WordList(QScrollArea):
    def __init__(self, words):
        super().__init__()
        container = QWidget()
        self.rowsLayout = QVBoxLayout(container)
        self.rowsLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setWidget(container)
        self.setWidgetResizable(True)
        self.setMinimumHeight(200)
        for word in words:
            self.addWord(word)

    def addWord(self, text):
        row = Row(text)
        row.removeRequested.connect(lambda: self.removeWord(row))
        self.rowsLayout.addWidget(row)

    def removeWord(self, row):
        self.rowsLayout.removeWidget(row)
        row.deleteLater()

    def words(self):
        return [self.rowsLayout.itemAt(i).widget().wordLabel.text()
                for i in range(self.rowsLayout.count())]


class DictPage(QWidget):
    def __init__(self):
        super().__init__()
        self.backButton = QPushButton("Back")
        self.wordInput = QLineEdit()
        self.wordInput.setPlaceholderText("Add a word")
        self.addButton = QPushButton("Add Word")
        self.wordList = WordList(DEFAULT_WORDS)
        layout = QVBoxLayout(self)
        top = QHBoxLayout()
        top.addWidget(self.backButton)
        top.addWidget(self.wordInput, 1)
        top.addWidget(self.addButton)
        layout.addLayout(top)
        layout.addWidget(self.wordList)
        layout.addWidget(QLabel("The word list is kept for this session."))
        self.addButton.clicked.connect(self.addWord)
        self.wordInput.returnPressed.connect(self.addWord)

    def addWord(self):
        text = self.wordInput.text().strip()
        if not text:
            self.wordInput.setFocus()
            return
        self.wordList.addWord(text)
        self.wordInput.clear()
        self.wordInput.setFocus()
