from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QCheckBox, QGroupBox, QHBoxLayout, QLabel, QPushButton,
    QSpinBox, QVBoxLayout, QWidget,
)


class MainPage(QWidget):
    def __init__(self):
        super().__init__()
        self.capitalCheck = QCheckBox("Capital Letters")
        self.specialCheck = QCheckBox("Special Characters")
        self.numbersCheck = QCheckBox("Numbers")
        for checkbox in (self.capitalCheck, self.specialCheck, self.numbersCheck):
            checkbox.setChecked(True)
        self.lengthSpin = QSpinBox()
        self.lengthSpin.setRange(1, 256)
        self.lengthSpin.setValue(16)
        self.generateButton = QPushButton("Generate")
        self.wordsButton = QPushButton("Word List")
        self.passwordLabel = QLabel("")
        self.passwordLabel.setTextFormat(Qt.TextFormat.PlainText)
        self.passwordLabel.setWordWrap(True)
        self.passwordLabel.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.copyButton = QPushButton("Copy Password")
        self.copyButton.setEnabled(False)
        self.setup()

    def setup(self):
        layout = QHBoxLayout(self)
        options = QGroupBox("Password options")
        controls = QVBoxLayout(options)
        controls.addWidget(QLabel("Minimum length"))
        controls.addWidget(self.lengthSpin)
        controls.addWidget(self.numbersCheck)
        controls.addWidget(self.capitalCheck)
        controls.addWidget(self.specialCheck)
        controls.addWidget(self.generateButton)
        controls.addWidget(self.wordsButton)
        layout.addWidget(options)

        output = QGroupBox("Password")
        result = QVBoxLayout(output)
        result.addWidget(self.passwordLabel, 1)
        result.addWidget(self.copyButton)
        layout.addWidget(output, 1)
