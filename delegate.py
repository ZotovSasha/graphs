from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Delegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        painter.save()
        super().paint(painter, option, index)
        painter.setPen(QPen(QColor("#90AFFF"), 2))
        painter.drawLine(option.rect.bottomLeft(), option.rect.bottomRight())
        painter.drawLine(option.rect.topRight(), option.rect.bottomRight())
        painter.restore()