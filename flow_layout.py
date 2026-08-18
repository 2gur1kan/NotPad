"""Etiket "chip" butonlarını satır satır, kutunun genişliğine göre otomatik
kaydırarak dizen basit bir Flow (akış) layout sınıfı."""
from PyQt5.QtCore import Qt, QRect, QPoint, QSize
from PyQt5.QtWidgets import QLayout


class FlowLayout(QLayout):
    def __init__(self, parent=None, margin=0, spacing=6):
        super().__init__(parent)
        self.Items = []
        self.setContentsMargins(margin, margin, margin, margin)
        self.setSpacing(spacing)

    # Not: addItem, count, itemAt, takeAt, expandingDirections,
    # hasHeightForWidth, heightForWidth, setGeometry, sizeHint, minimumSize
    # metotları Qt'nin QLayout arayüzünün bir parçasıdır ve framework
    # tarafından tam olarak bu isimlerle çağrılır — bu yüzden orijinal
    # (camelCase) isimleriyle bırakıldı, aksi halde Qt bunları tanımaz.

    def addItem(self, item):
        self.Items.append(item)

    def count(self):
        return len(self.Items)

    def itemAt(self, index):
        if 0 <= index < len(self.Items):
            return self.Items[index]
        return None

    def takeAt(self, index):
        if 0 <= index < len(self.Items):
            return self.Items.pop(index)
        return None

    def expandingDirections(self):
        return Qt.Orientations(Qt.Horizontal)

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        return self.DoLayout(QRect(0, 0, width, 0), TestOnly=True)

    def setGeometry(self, rect):
        super().setGeometry(rect)
        self.DoLayout(rect, TestOnly=False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        Size = QSize()
        for Item in self.Items:
            Size = Size.expandedTo(Item.minimumSize())
        Margins = self.contentsMargins()
        Size += QSize(Margins.left() + Margins.right(), Margins.top() + Margins.bottom())
        return Size

    def DoLayout(self, rect, TestOnly):
        X, Y = rect.x(), rect.y()
        RowHeight = 0
        Spacing = self.spacing()

        for Item in self.Items:
            Widget = Item.widget()
            NextX = X + Widget.sizeHint().width() + Spacing
            if NextX - Spacing > rect.right() and RowHeight > 0:
                X = rect.x()
                Y = Y + RowHeight + Spacing
                NextX = X + Widget.sizeHint().width() + Spacing
                RowHeight = 0
            if not TestOnly:
                Item.setGeometry(QRect(QPoint(X, Y), Widget.sizeHint()))
            X = NextX
            RowHeight = max(RowHeight, Widget.sizeHint().height())

        return Y + RowHeight - rect.y()
