"""Kayıt detay / düzenleme paneli.

Tablodaki "Aç" butonuna basıldığında açılır. Burada kaydın tüm bilgileri
(başlık, bilgi, TAM ek açıklama/notlar ve etiketler) görünür ve doğrudan
buradan düzenlenip kaydedilebilir.
"""
from PyQt5.QtWidgets import (
    QDialog, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit,
    QVBoxLayout, QHBoxLayout, QScrollArea, QFrame, QMessageBox
)

import database as Database
from flow_layout import FlowLayout


class RecordDetailDialog(QDialog):
    def __init__(self, RecordId, parent=None):
        super().__init__(parent)
        self.RecordId = RecordId
        self.TagChipButtons = {}
        self.setWindowTitle("Not Detayı")
        self.resize(420, 540)

        self.SetupUi()
        self.LoadRecord()

    # ---------- Arayüz kurulumu ----------

    def SetupUi(self):
        MainLayout = QVBoxLayout(self)
        MainLayout.setContentsMargins(20, 20, 20, 20)
        MainLayout.setSpacing(10)

        MainLayout.addWidget(self.CreateFieldLabel("Başlık"))
        self.TitleInput = QLineEdit()
        MainLayout.addWidget(self.TitleInput)

        MainLayout.addWidget(self.CreateFieldLabel("Bilgi (örn: şifre)"))
        InfoRow = QHBoxLayout()
        self.InfoInput = QLineEdit()
        self.InfoInput.setEchoMode(QLineEdit.Password)
        self.ShowInfoButton = QPushButton("👁")
        self.ShowInfoButton.setObjectName("Secondary")
        self.ShowInfoButton.setFixedWidth(36)
        self.ShowInfoButton.setCheckable(True)
        self.ShowInfoButton.toggled.connect(self.ToggleInfoVisibility)
        InfoRow.addWidget(self.InfoInput)
        InfoRow.addWidget(self.ShowInfoButton)
        MainLayout.addLayout(InfoRow)

        MainLayout.addWidget(self.CreateFieldLabel("Ek Açıklama (Notlar) — tamamı"))
        self.NotesInput = QTextEdit()
        self.NotesInput.setMinimumHeight(180)
        MainLayout.addWidget(self.NotesInput)

        MainLayout.addWidget(self.CreateFieldLabel("Etiketler (seçmek için tıkla)"))
        self.TagScrollArea = QScrollArea()
        self.TagScrollArea.setWidgetResizable(True)
        self.TagScrollArea.setFixedHeight(84)
        self.TagScrollArea.setFrameShape(QFrame.NoFrame)
        TagContainer = QWidget()
        self.TagFlowLayout = FlowLayout(TagContainer, margin=2, spacing=6)
        TagContainer.setLayout(self.TagFlowLayout)
        self.TagScrollArea.setWidget(TagContainer)
        MainLayout.addWidget(self.TagScrollArea)

        MainLayout.addSpacing(6)

        ButtonRow = QHBoxLayout()
        self.SaveButton = QPushButton("Kaydet")
        self.SaveButton.clicked.connect(self.SaveChanges)
        self.CloseButton = QPushButton("Kapat")
        self.CloseButton.setObjectName("Secondary")
        self.CloseButton.clicked.connect(self.reject)
        ButtonRow.addWidget(self.SaveButton)
        ButtonRow.addWidget(self.CloseButton)
        MainLayout.addLayout(ButtonRow)

    def CreateFieldLabel(self, Text):
        Label = QLabel(Text)
        Label.setStyleSheet("color:#9aa0a8; font-size:12px;")
        return Label

    # ---------- Davranışlar ----------

    def ToggleInfoVisibility(self, IsVisible):
        self.InfoInput.setEchoMode(QLineEdit.Normal if IsVisible else QLineEdit.Password)
        self.ShowInfoButton.setText("🙈" if IsVisible else "👁")

    def LoadRecord(self):
        Connection = Database.GetConnection()
        Record = Connection.execute("SELECT * FROM kayitlar WHERE id=?", (self.RecordId,)).fetchone()
        Connection.close()
        if Record is None:
            return

        self.TitleInput.setText(Record["baslik"])
        self.InfoInput.setText(Record["bilgi"])
        self.NotesInput.setPlainText(Record["notlar"] or "")

        SelectedIds = {Tag["id"] for Tag in Database.GetRecordTags(self.RecordId)}
        self.RefreshTags(SelectedIds)

    def RefreshTags(self, SelectedIds=None):
        if SelectedIds is None:
            SelectedIds = self.GetSelectedTagIds()

        while self.TagFlowLayout.count():
            Item = self.TagFlowLayout.takeAt(0)
            Widget = Item.widget()
            if Widget:
                Widget.deleteLater()
        self.TagChipButtons = {}

        for Tag in Database.GetAllTags():
            ChipButton = QPushButton(Tag["ad"])
            ChipButton.setObjectName("TagChip")
            ChipButton.setCheckable(True)
            ChipButton.setChecked(Tag["id"] in SelectedIds)
            self.TagFlowLayout.addWidget(ChipButton)
            self.TagChipButtons[Tag["id"]] = ChipButton

    def GetSelectedTagIds(self):
        return {TagId for TagId, Button in self.TagChipButtons.items() if Button.isChecked()}

    def SaveChanges(self):
        Title = self.TitleInput.text().strip()
        Info = self.InfoInput.text().strip()
        NotesText = self.NotesInput.toPlainText().strip()
        TagIds = self.GetSelectedTagIds()

        if not Title or not Info:
            QMessageBox.warning(self, "Eksik bilgi", "Başlık ve bilgi alanları boş bırakılamaz.")
            return

        Database.UpdateRecord(self.RecordId, Title, Info, NotesText, TagIds)
        self.accept()
