from PyQt6.QtWidgets import *

class Mainpage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QGridLayout()
        self.setLayout(layout)

        capital = QCheckBox("Capital Letters")
        special = QCheckBox("Special Characters")
        numbers = QCheckBox("Numbers")
        length = QSpinBox()
        generate = QPushButton("Generate")

        self.dictionary = QPushButton("Word List")

        password = QLabel("asdfjkasdf")

        layout.addWidget(length, 0, 0)
        layout.addWidget(numbers, 1, 0)
        layout.addWidget(capital, 2, 0)
        layout.addWidget(special, 3, 0)
        layout.addWidget(generate, 5, 0)
        layout.addWidget(self.dictionary, 6, 0)

        layout.addWidget(password, 0, 3)
