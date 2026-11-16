from PyQt6.QtWidgets import *

class MainPage(QWidget):
    def __init__(self):
        super().__init__()
        self.capitalCheck = QCheckBox("Capital Letters")
        self.specialCheck = QCheckBox("Special Characters")
        self.numbersCheck = QCheckBox("Numbers")
        self.lengthSpin = QSpinBox()
        self.generateButton = QPushButton("Generate")
        self.wordsButton = QPushButton("Word List")
        self.passwordLabel = QLabel("asdfjkasdf")
        self.copyButton = QPushButton("Copy Password")


        self.capital = False;
        self.numbers = False;
        self.special = False;
        self.length = 0;

        self.setup()

    def setup(self):
        layout = QHBoxLayout()
        self.setLayout(layout)

        col0 = QVBoxLayout()
        gb0 = QGroupBox()
        gb0.setLayout(col0)
        layout.addWidget(gb0)

        col1 = QVBoxLayout()
        gb1 = QGroupBox()
        gb1.setLayout(col1)
        layout.addWidget(gb1)


        col0.addWidget(self.lengthSpin)
        col0.addWidget(self.numbersCheck)
        col0.addWidget(self.capitalCheck)
        col0.addWidget(self.specialCheck)
        col0.addWidget(self.generateButton)
        col0.addWidget(self.wordsButton)

        col1.addWidget(self.passwordLabel)
        col1.addWidget(self.copyButton)

        self.capitalCheck.stateChanged.connect(self.capitalChanged)
        self.numbersCheck.stateChanged.connect(self.numbersChanged)
        self.specialCheck.stateChanged.connect(self.specialChanged)
        self.lengthSpin.valueChanged.connect(self.lengthChanged)


    def capitalChanged(self):
        self.capital = self.capitalCheck.isChecked()

    def numbersChanged(self):
        self.numbers = self.numbersCheck.isChecked()

    def specialChanged(self):
        self.special = self.specialCheck.isChecked()

    def lengthChanged(self, value):
        self.length = value
