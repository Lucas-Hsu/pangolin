"""The scrollable form, using the supplied question and answer shapes."""
from PyQt6.QtCore import QRegularExpression, Qt, pyqtSignal
from PyQt6.QtGui import QColor, QPainter, QRegularExpressionValidator
from PyQt6.QtWidgets import (
    QLabel, QScrollArea, QScrollBar, QStyle, QStyleOptionSlider, QWidget,
)

from .art import ArtButton, ArtLineEdit, BACKGROUND, PURPLE, pixmap, rect, set_font_size
from .feedback import install_feedback

QUESTIONS = (
    'What is your favorite color?',
    'What is your favorite animal?',
    "What is your favorite pet's name?",
    'What is your favorite number?',
    'What is your 2nd favorite number?',
    'What is your 3rd favorite number?',
    'What is your favorite food?',
    'What is your favorite dance?',
    'What is your favorite song?',
    'What is your favorite drink?',
    'What is your favorite activity?',
    'What is your favorite adjective in the dictionary?',
    'What is your favorite verb in the dictionary?',
    'What is your favorite noun in the dictionary?',
)
NUMBER_FIELD_INDICES = (3, 4, 5)


class Header(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.image = pixmap('questions_header.png')

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(BACKGROUND))
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        painter.drawPixmap(rect((40, 64, 1214, 191), self.width() / 1280), self.image)


class ArtScrollBar(QScrollBar):
    def __init__(self, parent):
        super().__init__(Qt.Orientation.Vertical, parent)
        self.image = pixmap('scroll_thumb.png')
        self.artWidth = 0
        self.setArtWidth(24)
        install_feedback(self, click_effect=False)

    def setArtWidth(self, width):
        if self.artWidth == width:
            return
        self.artWidth = width
        self.setStyleSheet(f'QScrollBar:vertical {{width:{width}px; border:0;}}'
                           'QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {height:0;}')

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(BACKGROUND))
        if self.maximum() <= self.minimum():
            return
        option = QStyleOptionSlider()
        self.initStyleOption(option)
        target = self.style().subControlRect(QStyle.ComplexControl.CC_ScrollBar, option,
                                             QStyle.SubControl.SC_ScrollBarSlider, self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        painter.drawPixmap(target, self.image)


class QuestionSheet(QWidget):
    answersSubmitted = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.bubbles = [pixmap(f'question_{i}.png') for i in range(3)]
        self.labels = []
        self.fields = []
        for question in QUESTIONS:
            label = QLabel(question, self)
            label.setTextFormat(Qt.TextFormat.PlainText)
            label.setWordWrap(True)
            label.setStyleSheet(f'color:{PURPLE}; background:transparent;')
            field = ArtLineEdit(self, f'answer_{len(self.fields) % 3}.png')
            field.setAccessibleName(question)
            field.setMaxLength(80)
            if len(self.fields) in NUMBER_FIELD_INDICES:
                field.setValidator(QRegularExpressionValidator(QRegularExpression('[0-9]*'), field))
                field.setInputMethodHints(Qt.InputMethodHint.ImhDigitsOnly)
            field.setStyleSheet(f'QLineEdit {{color:{PURPLE}; background:transparent; border:0;'
                               'selection-background-color:#400080; selection-color:#e8d0ee;}')
            label.setBuddy(field)
            self.labels.append(label)
            self.fields.append(field)
        self.setupButton = ArtButton('Set Up', 'setup_button.png', self, click_effect=False)
        self.setupButton.setEnabled(False)
        self.setupButton.clicked.connect(self.submit)
        for index, field in enumerate(self.fields):
            field.textChanged.connect(self.updateComplete)
            field.returnPressed.connect(lambda index=index: self.advance(index))

    @staticmethod
    def row_top(index):
        return (index // 3) * 708 + (0, 218, 439)[index % 3]

    @staticmethod
    def validAnswer(field):
        return bool(field.text().strip()) and field.hasAcceptableInput()

    def updateComplete(self):
        self.setupButton.setEnabled(all(self.validAnswer(field) for field in self.fields))

    def advance(self, index):
        if index + 1 < len(self.fields):
            self.fields[index + 1].setFocus()
        else:
            self.submit()

    def submit(self):
        for field in self.fields:
            if not self.validAnswer(field):
                field.setFocus()
                return
        self.answersSubmitted.emit([field.text().strip() for field in self.fields])

    def reset(self):
        for field in self.fields:
            field.clear()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(BACKGROUND))
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        scale = self.width() / 1256
        for index in range(len(QUESTIONS)):
            variant = index % 3
            top = self.row_top(index)
            image = self.bubbles[variant]
            painter.drawPixmap(rect(((77, 57, 21)[variant], top,
                                     image.width(), image.height()), scale), image)

    def resizeEvent(self, event):
        scale = self.width() / 1256
        last = len(self.fields) - 1
        setup_top = self.row_top(last) + self.bubbles[last % 3].height() + 100
        self.setFixedHeight(round((setup_top + 288) * scale))
        for index, (label, field) in enumerate(zip(self.labels, self.fields)):
            top = self.row_top(index)
            x = (77, 57, 21)[index % 3]
            label.setGeometry(rect((x + 38, top + 32, 675, 132), scale))
            field.setGeometry(rect(((833, 816, 799)[index % 3],
                                    top + (95, 112, 129)[index % 3],
                                    (418, 420, 420)[index % 3], 90), scale))
            field.setTextMargins(round(16 * scale), 0, round(16 * scale), 0)
            set_font_size(label, 30 * scale)
            set_font_size(field, 30 * scale)
        self.setupButton.setGeometry(rect((263, setup_top, 696, 188), scale))
        super().resizeEvent(event)


class QuestionsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.header = Header(self)
        self.scroll = QScrollArea(self)
        self.scroll.setStyleSheet(f'QScrollArea {{border:0; background:{BACKGROUND};}}')
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBar(ArtScrollBar(self.scroll))
        self.sheet = QuestionSheet()
        self.scroll.setWidget(self.sheet)

    def resizeEvent(self, event):
        header_height = round(299 * self.width() / 1280)
        self.scroll.verticalScrollBar().setArtWidth(max(12, round(24 * self.width() / 1280)))
        self.header.setGeometry(0, 0, self.width(), header_height)
        self.scroll.setGeometry(0, header_height, self.width(), max(1, self.height() - header_height))
        super().resizeEvent(event)

    def reset(self):
        self.sheet.reset()
        self.scroll.verticalScrollBar().setValue(0)
