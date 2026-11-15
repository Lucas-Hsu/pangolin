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


        self.capital = False;
        self.numbers = False;
        self.special = False;
        self.length = 0;

        self.setup()

    def setup(self):
        layout = QGridLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel("Minimum Length:"), 0, 0)
        layout.addWidget(self.lengthSpin, 1, 0)
        layout.addWidget(self.numbersCheck, 2, 0)
        layout.addWidget(self.capitalCheck, 3, 0)
        layout.addWidget(self.specialCheck, 4, 0)
        layout.addWidget(self.generateButton, 6, 0)
        layout.addWidget(self.wordsButton, 7, 0)
        layout.addWidget(self.passwordLabel, 0, 3)

        self.capitalCheck.stateChanged.connect(self.capitalChanged)
        self.numbersCheck.stateChanged.connect(self.numbersChanged)
        self.specialCheck.stateChanged.connect(self.specialChanged)
        self.lengthSpin.valueChanged.connect(self.lengthChanged)
        self.generateButton.clicked.connect(self.changeLabel)

    def changeLabel(self):
        self.passwordLabel.setText(f"{self.capital} {self.numbers} {self.special} {self.length}")

    def capitalChanged(self):
        self.capital = self.capitalCheck.isChecked()

    def numbersChanged(self):
        self.numbers = self.numbersCheck.isChecked()

    def specialChanged(self):
        self.special = self.specialCheck.isChecked()

    def lengthChanged(self, value):
        self.length = value
