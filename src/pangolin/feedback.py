"""Small, reusable hover and press effects without changing control geometry."""
from PyQt6.QtCore import QEvent, QEasingCurve, QObject, QRectF, Qt, QVariantAnimation
from PyQt6.QtGui import QColor, QPainter, QPixmap
from PyQt6.QtWidgets import QAbstractButton, QGraphicsEffect


class FeedbackEffect(QGraphicsEffect):
    def __init__(self, parent):
        super().__init__(parent)
        self.highlight = 0.0
        self.scale = 1.0

    def boundingRectFor(self, bounds):
        return bounds.adjusted(-bounds.width() * .06, -bounds.height() * .06,
                               bounds.width() * .06, bounds.height() * .06)

    def draw(self, painter):
        source, offset = self.sourcePixmap(Qt.CoordinateSystem.LogicalCoordinates,
                                            QGraphicsEffect.PixmapPadMode.NoPad)
        if source.isNull():
            return
        if self.highlight > .001:
            source = QPixmap(source)
            overlay = QPainter(source)
            overlay.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceAtop)
            overlay.fillRect(source.rect(), QColor(255, 255, 255, round(255 * self.highlight)))
            overlay.end()
        ratio = source.devicePixelRatioF()
        target = QRectF(offset.x(), offset.y(), source.width() / ratio, source.height() / ratio)
        center = target.center()
        painter.save()
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        painter.translate(center)
        painter.scale(self.scale, self.scale)
        painter.translate(-center)
        painter.drawPixmap(offset, source)
        painter.restore()


class Feedback(QObject):
    def __init__(self, widget, click_effect=True):
        super().__init__(widget)
        self.widget = widget
        self.click_effect = click_effect
        self.effect = FeedbackEffect(widget)
        widget.setGraphicsEffect(self.effect)
        widget.installEventFilter(self)
        self.hover = QVariantAnimation(self)
        self.hover.setDuration(130)
        self.hover.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.hover.valueChanged.connect(self.setHighlight)
        self.press = QVariantAnimation(self)
        self.press.setDuration(240)
        self.press.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.press.valueChanged.connect(self.setScale)
        self.press.finished.connect(lambda: self.setScale(1.0))
        if isinstance(widget, QAbstractButton) and click_effect:
            widget.pressed.connect(self.pop)

    def setHighlight(self, value):
        self.effect.highlight = float(value)
        self.effect.update()

    def setScale(self, value):
        self.effect.scale = float(value)
        self.effect.update()

    def pop(self):
        self.press.stop()
        self.press.setStartValue(1.0)
        self.press.setKeyValueAt(.32, 1.1)
        self.press.setEndValue(1.0)
        self.press.start()

    def eventFilter(self, watched, event):
        kind = event.type()
        if kind in (QEvent.Type.Enter, QEvent.Type.Leave):
            self.hover.stop()
            self.hover.setStartValue(self.effect.highlight)
            self.hover.setEndValue(.12 if kind == QEvent.Type.Enter and self.widget.isEnabled() else 0.0)
            self.hover.start()
        elif kind == QEvent.Type.MouseButtonPress and self.click_effect:
            if not isinstance(self.widget, QAbstractButton) and self.widget.isEnabled():
                self.pop()
        return False


def install_feedback(widget, click_effect=True):
    widget.feedback = Feedback(widget, click_effect)
    return widget.feedback
