"""Uygulama genelinde kullanılan Qt StyleSheet (QSS) tanımı."""

AppStyleSheet = """
QWidget {
    background-color: #120d0e;
    color: #ece4e4;
    font-family: Segoe UI, Arial;
    font-size: 13px;
}
QFrame#Card {
    background-color: #1c1315;
    border: 1px solid #3a1f24;
    border-radius: 12px;
}
QLabel#TitleLabel {
    font-size: 20px;
    font-weight: 600;
    color: #ffffff;
}
QLabel#SubtitleLabel {
    color: #a3898c;
}
QLineEdit, QTextEdit {
    background-color: #120d0e;
    border: 1px solid #3a1f24;
    border-radius: 8px;
    padding: 8px;
    color: #ece4e4;
}
QLineEdit:focus, QTextEdit:focus {
    border: 1px solid #b3394a;
}
QComboBox {
    background-color: #1c1315;
    border: 1px solid #3a1f24;
    border-radius: 8px;
    padding: 7px 10px;
    color: #ece4e4;
    min-width: 130px;
}
QComboBox QAbstractItemView {
    background-color: #1c1315;
    color: #ece4e4;
    selection-background-color: #4a1620;
    border: 1px solid #3a1f24;
}
QPushButton {
    background-color: #8a2331;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 9px 16px;
    font-weight: 500;
}
QPushButton:hover {
    background-color: #a12a3b;
}
QPushButton#Secondary {
    background-color: #2a1c1f;
    color: #d8c8ca;
}
QPushButton#Secondary:hover {
    background-color: #38252a;
}
QPushButton#Danger {
    background-color: #6e1620;
}
QPushButton#Danger:hover {
    background-color: #8a1c28;
}
QPushButton#TagChip {
    background-color: #241618;
    color: #d8c8ca;
    border: 1px solid #3a1f24;
    border-radius: 13px;
    padding: 4px 12px;
    font-size: 12px;
    font-weight: 400;
}
QPushButton#TagChip:hover {
    border: 1px solid #b3394a;
}
QPushButton#TagChip:checked {
    background-color: #8a2331;
    color: white;
    border: 1px solid #8a2331;
}
/* Tablo satırlarındaki kompakt aksiyon butonları — dar sütuna sığması ve
   yazının kesilmemesi için normal butonlardan daha az padding kullanır */
QPushButton#RowSecondary {
    background-color: #2a1c1f;
    color: #d8c8ca;
    border: none;
    border-radius: 6px;
    padding: 4px 6px;
    font-size: 11px;
    font-weight: 500;
}
QPushButton#RowSecondary:hover {
    background-color: #38252a;
}
QPushButton#RowDanger {
    background-color: #6e1620;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 4px 6px;
    font-size: 11px;
    font-weight: 500;
}
QPushButton#RowDanger:hover {
    background-color: #8a1c28;
}
QTableWidget {
    background-color: #1c1315;
    border: 1px solid #3a1f24;
    border-radius: 10px;
    gridline-color: #2a1c1f;
    selection-background-color: #4a1620;
}
QHeaderView::section {
    background-color: #201619;
    color: #a3898c;
    padding: 8px;
    border: none;
    font-weight: 600;
}
QTableWidget::item {
    padding: 6px;
}
QScrollBar:vertical, QScrollBar:horizontal {
    background: #1c1315;
    width: 10px;
    height: 10px;
}
QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
    background: #3a1f24;
    border-radius: 5px;
}
QMenu {
    background-color: #1c1315;
    border: 1px solid #3a1f24;
    color: #ece4e4;
}
QMenu::item:selected {
    background-color: #4a1620;
}
"""
