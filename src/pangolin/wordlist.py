from PyQt6.QtWidgets import *

class Row(QWidget):
    def __init__(self, text):
        super().__init__()
        layout = QHBoxLayout()
        self.setLayout(layout)

        label = QLabel(text)
        edit = QPushButton("edit")
        delete = QPushButton("delete")

        layout.addWidget(delete, 0)
        layout.addWidget(edit, 1)
        layout.addWidget(label, 5)

class Dictpage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.back = QPushButton("back")

        layout.addWidget(self.back)
        layout.addWidget(QLineEdit())
        self.setLayout(layout)

        formlayout = QFormLayout()
        formlayout.addRow(Row("fooooooooooooooooooooooooooooooooooo"))
        formlayout.addRow(Row("bar"))

        formwidget = QWidget()
        formwidget.setLayout(formlayout)

        scrollable = QScrollArea()
        scrollable.setWidget(formwidget)

        layout.addWidget(scrollable)
