"""Position real controls over the supplied 1280 × 1024 artwork."""
from pathlib import Path

from PyQt6.QtCore import QRect, QRectF, Qt
from PyQt6.QtGui import QColor, QColorSpace, QImage, QPainter, QPen, QPixmap
from PyQt6.QtWidgets import QAbstractButton, QLineEdit, QWidget

from .feedback import install_feedback

ASSETS = Path(__file__).with_name('assets')
# The supplied PNGs use Generic RGB. These are the corresponding sRGB colors.
BACKGROUND = '#eddaf2'
PURPLE = '#521b93'


def pixmap(name):
    image = QImage(str(ASSETS / name))
    if image.isNull():
        raise RuntimeError(f'Missing artwork: {name}')
    if image.colorSpace().isValid():
        image.convertToColorSpace(QColorSpace(QColorSpace.NamedColorSpace.SRgb))
    return QPixmap.fromImage(image)


def rect(values, scale=1, left=0, top=0):
    x, y, width, height = values
    return QRect(round(left + x * scale), round(top + y * scale),
                 max(1, round(width * scale)), max(1, round(height * scale)))


def set_font_size(widget, size):
    font = widget.font()
    font.setPixelSize(max(10, round(size)))
    widget.setFont(font)


class ArtButton(QAbstractButton):
    def __init__(self, name, image=None, parent=None, click_effect=True):
        super().__init__(parent)
        self.setAccessibleName(name)
        self.setText(name)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.image = pixmap(image) if image else None
        self.keyboardFocus = False
        install_feedback(self, click_effect)

    def focusInEvent(self, event):
        self.keyboardFocus = event.reason() in (
            Qt.FocusReason.TabFocusReason, Qt.FocusReason.BacktabFocusReason,
            Qt.FocusReason.ShortcutFocusReason,
        )
        super().focusInEvent(event)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        if self.image is not None:
            painter.drawPixmap(self.rect(), self.image)
        if self.hasFocus() and self.keyboardFocus:
            pen = QPen(QColor(PURPLE))
            pen.setStyle(Qt.PenStyle.DotLine)
            painter.setPen(pen)
            painter.drawRect(self.rect().adjusted(2, 2, -3, -3))


class ArtLineEdit(QLineEdit):
    def __init__(self, parent=None, image=None):
        super().__init__(parent)
        self.image = pixmap(image) if image else None
        install_feedback(self)

    def paintEvent(self, event):
        if self.image is not None:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
            painter.drawPixmap(self.rect(), self.image)
            painter.end()
        super().paintEvent(event)


class ArtCanvas(QWidget):
    def __init__(self, image=None, parent=None):
        super().__init__(parent)
        self.image = pixmap(image) if image else None
        self.scale = 1
        self.left = 0
        self.top = 0

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(BACKGROUND))
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        if self.image is not None:
            painter.drawPixmap(rect((0, 0, 1280, 1024), self.scale, self.left, self.top), self.image)

    def place(self, widget, bounds):
        widget.setGeometry(rect(bounds, self.scale, self.left, self.top))

    def resizeEvent(self, event):
        self.scale = min(self.width() / 1280, self.height() / 1024)
        self.left = (self.width() - 1280 * self.scale) / 2
        self.top = (self.height() - 1024 * self.scale) / 2
        self.layoutArt()
        super().resizeEvent(event)

    def layoutArt(self):
        pass
