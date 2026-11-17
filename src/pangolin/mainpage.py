import math

from PyQt6.QtCore import QEasingCurve, QRect, Qt, QVariantAnimation, pyqtSignal
from PyQt6.QtGui import QColor, QFontMetrics, QIntValidator, QPainter

from .art import ArtButton, ArtCanvas, ArtLineEdit, PURPLE, pixmap, rect


class PasswordBubble(ArtButton):
    def __init__(self, parent):
        super().__init__('Copy password', 'bubble_initial.png', parent)
        self.initialImage = self.image
        self.readyImage = pixmap('bubble_ready.png')
        self.greenImage = pixmap('bubble_empty.png')
        color = QPainter(self.greenImage)
        color.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
        color.fillRect(self.greenImage.rect(), QColor('#42ed84'))
        color.end()
        self.password = ''
        self.flash = 0.0
        self.flashAnimation = QVariantAnimation(self)
        self.flashAnimation.setDuration(700)
        self.flashAnimation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.flashAnimation.valueChanged.connect(self.setFlash)

    def setFlash(self, value):
        self.flash = float(value)
        self.update()

    def flashCopied(self):
        self.flashAnimation.stop()
        self.flashAnimation.setStartValue(.88)
        self.flashAnimation.setEndValue(0.0)
        self.flashAnimation.start()

    def setPassword(self, password):
        self.flashAnimation.stop()
        self.flash = 0.0
        self.password = password
        self.image = self.readyImage if password else self.initialImage
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        if self.flash > .001:
            painter.setOpacity(self.flash)
            painter.drawPixmap(self.rect(), self.greenImage)
            painter.setOpacity(1.0)
        if not self.password:
            return
        scale = self.width() / 888
        target = rect((100, 185, 680, 155), scale)
        flags = (Qt.AlignmentFlag.AlignCenter | Qt.TextFlag.TextWordWrap
                 | Qt.TextFlag.TextWrapAnywhere)
        font = self.font()
        size = max(10, round(48 * scale))
        while size > max(9, round(14 * scale)):
            font.setPixelSize(size)
            bounds = QFontMetrics(font).boundingRect(target, int(flags), self.password)
            if bounds.height() <= target.height():
                break
            size -= 1
        painter.setFont(font)
        painter.setPen(QColor(PURPLE))
        painter.drawText(target, int(flags), self.password)


class PangolinButton(ArtButton):
    generationRequested = pyqtSignal()

    def __init__(self, parent):
        super().__init__('Generate password', parent=parent)
        self.body = pixmap('pangolin.png')
        # Sampled from the supplied coral swatch, converted to sRGB.
        self.generateColor = QColor('#ff7474')
        self.angle = 0.0
        self.isSpinning = False
        self.spinAnimation = QVariantAnimation(self)
        self.spinAnimation.setDuration(1100)
        self.spinAnimation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.spinAnimation.valueChanged.connect(self.setAngle)
        self.spinAnimation.finished.connect(self.finishSpin)
        self.pressed.connect(self.startSpin)

    def setAngle(self, value):
        self.angle = float(value)
        self.update()

    def startSpin(self):
        current_angle = self.angle
        was_spinning = self.isSpinning
        self.spinAnimation.stop()
        self.isSpinning = True
        self.spinAnimation.setStartValue(current_angle)
        # Continue from this exact angle, then settle upright so the label is readable.
        self.spinAnimation.setEndValue(math.ceil(current_angle / 360.0) * 360.0 + 720.0)
        self.spinAnimation.start()
        if not was_spinning:
            # Give the first paint visible movement without waiting for Qt's first timer tick.
            self.spinAnimation.setCurrentTime(1)
        self.generationRequested.emit()

    def finishSpin(self):
        self.isSpinning = False

    def reset(self):
        self.spinAnimation.stop()
        self.isSpinning = False
        self.setAngle(0)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(self.width() / 504, self.height() / 504)
        painter.rotate(self.angle % 360)
        painter.drawPixmap(QRect(-252, -252, 504, 504), self.body)
        # Place each glyph along the upper arc, tangent to the pangolin's ring.
        font = self.font()
        font.setPixelSize(44)
        font.setBold(True)
        painter.setFont(font)
        painter.setPen(self.generateColor)
        metrics = QFontMetrics(font)
        advances = [metrics.horizontalAdvance(letter) + 3 for letter in 'GENERATE']
        radius = 171
        position = -sum(advances) / 2
        for letter, advance in zip('GENERATE', advances):
            angle = -90 + math.degrees((position + advance / 2) / radius)
            painter.save()
            painter.translate(radius * math.cos(math.radians(angle)),
                              radius * math.sin(math.radians(angle)))
            painter.rotate(angle + 90)
            painter.drawText(round(-metrics.horizontalAdvance(letter) / 2), 0, letter)
            painter.restore()
            position += advance
        if self.hasFocus() and self.keyboardFocus:
            painter.setPen(QColor('white'))
            painter.drawEllipse(QRect(-235, -235, 470, 470))


class ArtCheckBox(ArtButton):
    def __init__(self, name, image, icon_y, parent):
        super().__init__(name, image, parent)
        self.setCheckable(True)
        self.icon_y = icon_y
        self.checkedImage = pixmap('checked.png')
        self.uncheckedImage = pixmap('unchecked.png')

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        scale = self.width() / self.image.width()
        image = self.checkedImage if self.isChecked() else self.uncheckedImage
        painter.drawPixmap(rect((3, self.icon_y, image.width(), image.height()), scale), image)


class LengthInput(ArtLineEdit):
    """A full-size number editor, independent of native spin-box insets."""
    def __init__(self, parent):
        super().__init__(parent, 'length_box.png')
        self._value = 8
        self.setValidator(QIntValidator(1, 256, self))
        self.setAccessibleName('Minimum password length')
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFrame(False)
        self.setTextMargins(0, 0, 0, 0)
        self.setAttribute(Qt.WidgetAttribute.WA_MacShowFocusRect, False)
        self.setStyleSheet(
            'QLineEdit {background:transparent; border:0; padding:0; margin:0;'
            'color:#fffc79; selection-background-color:#521b93; selection-color:#fffc79;}'
        )
        self.textChanged.connect(self.rememberValid)
        self.setValue(8)

    def rememberValid(self):
        if self.hasAcceptableInput():
            self._value = int(self.text())

    def value(self):
        return int(self.text()) if self.hasAcceptableInput() else self._value

    def setValue(self, value):
        self._value = max(1, min(256, int(value)))
        self.setText(str(self._value))

    def stepUp(self):
        self.setValue(self.value() + 1)

    def stepDown(self):
        self.setValue(self.value() - 1)

    def focusOutEvent(self, event):
        self.setValue(self.value())
        super().focusOutEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Up:
            self.stepUp()
        elif event.key() == Qt.Key.Key_Down:
            self.stepDown()
        elif event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.setValue(self.value())
            super().keyPressEvent(event)
        else:
            super().keyPressEvent(event)

    def fitFont(self, scale):
        font = self.font()
        size = max(10, round(72 * scale))
        # Leave room for all three digits and the editor's text margins.
        while size > 10:
            font.setPixelSize(size)
            metrics = QFontMetrics(font)
            if (metrics.horizontalAdvance('256') <= self.width() - 12
                    and metrics.height() <= self.height() - 8):
                break
            size -= 1
        font.setPixelSize(size)
        self.setFont(font)


class MainPage(ArtCanvas):
    def __init__(self):
        super().__init__('main.png')
        self.generateButton = PangolinButton(self)
        self.copyButton = PasswordBubble(self)
        self.capitalCheck = ArtCheckBox('Uppercase', 'option_uppercase.png', 21, self)
        self.numbersCheck = ArtCheckBox('Digits', 'option_digits.png', 8, self)
        self.specialCheck = ArtCheckBox('Symbols', 'option_symbols.png', 7, self)
        self.lengthSpin = LengthInput(self)
        self.upButton = ArtButton('Increase minimum length', 'arrow_up.png', self)
        self.downButton = ArtButton('Decrease minimum length', 'arrow_down.png', self)
        self.upButton.clicked.connect(self.lengthSpin.stepUp)
        self.downButton.clicked.connect(self.lengthSpin.stepDown)
        self.clearButton = ArtButton('Clear Data', 'clear_data.png', self, click_effect=False)
        self.reset()

    def reset(self):
        self.capitalCheck.setChecked(True)
        self.numbersCheck.setChecked(True)
        self.specialCheck.setChecked(False)
        self.lengthSpin.setValue(8)
        self.generateButton.reset()
        self.setPassword('')

    def setPassword(self, password):
        self.copyButton.setPassword(password)

    def layoutArt(self):
        self.place(self.copyButton, (170, 9, 888, 431))
        self.place(self.generateButton, (770, 414, 504, 504))
        self.place(self.capitalCheck, (59, 456, 470, 94))
        self.place(self.numbersCheck, (59, 550, 350, 82))
        self.place(self.specialCheck, (59, 633, 370, 93))
        self.place(self.lengthSpin, (49, 745, 152, 110))
        self.place(self.upButton, (201, 735, 68, 62))
        self.place(self.downButton, (201, 796, 68, 61))
        self.place(self.clearButton, (69, 939, 437, 85))
        self.lengthSpin.fitFont(self.scale)
