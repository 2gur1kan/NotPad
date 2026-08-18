"""Ana pencere: Not Defteri arayüzü."""
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QMainWindow, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox, QAbstractItemView, QFrame, QTextEdit,
    QComboBox, QScrollArea, QMenu
)
from PyQt5.QtGui import QCursor

import database as Database
from flow_layout import FlowLayout
from record_detail_dialog import RecordDetailDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Not Defteri")
        self.resize(1000, 620)
        self.TagChipButtons = {}  # {TagId: QPushButton}

        self.SetupUi()
        self.RefreshTags()
        self.RefreshList()

    # ---------- Arayüz kurulumu ----------

    def SetupUi(self):
        CentralWidget = QWidget()
        self.setCentralWidget(CentralWidget)
        MainLayout = QVBoxLayout(CentralWidget)
        MainLayout.setContentsMargins(24, 24, 24, 24)
        MainLayout.setSpacing(16)

        TitleLabel = QLabel("Not Defteri")
        TitleLabel.setObjectName("TitleLabel")
        SubtitleLabel = QLabel("Hesap bilgilerini yerel olarak saklayan ufak bir uygulama")
        SubtitleLabel.setObjectName("SubtitleLabel")
        MainLayout.addWidget(TitleLabel)
        MainLayout.addWidget(SubtitleLabel)

        BodyLayout = QHBoxLayout()
        BodyLayout.setSpacing(16)
        MainLayout.addLayout(BodyLayout)

        # ---- Sol: yeni kayıt ekleme kartı ----
        FormCard = QFrame()
        FormCard.setObjectName("Card")
        FormCard.setFixedWidth(320)
        FormLayout = QVBoxLayout(FormCard)
        FormLayout.setContentsMargins(18, 18, 18, 18)
        FormLayout.setSpacing(10)

        FormTitleLabel = QLabel("Yeni Not Ekle")
        FormTitleLabel.setStyleSheet("font-weight:600; font-size:14px; color:#fff;")
        FormLayout.addWidget(FormTitleLabel)

        FormLayout.addWidget(self.CreateFieldLabel("1. Başlık"))
        self.TitleInput = QLineEdit()
        self.TitleInput.setPlaceholderText("örn: Gmail, İş Bankası...")
        FormLayout.addWidget(self.TitleInput)

        FormLayout.addWidget(self.CreateFieldLabel("2. Bilgi (örn: şifre)"))
        InfoRow = QHBoxLayout()
        self.InfoInput = QLineEdit()
        self.InfoInput.setPlaceholderText("şifre / bilgi")
        self.InfoInput.setEchoMode(QLineEdit.Password)
        self.ShowInfoButton = QPushButton("👁")
        self.ShowInfoButton.setObjectName("Secondary")
        self.ShowInfoButton.setFixedWidth(36)
        self.ShowInfoButton.setCheckable(True)
        self.ShowInfoButton.toggled.connect(self.ToggleInfoVisibility)
        InfoRow.addWidget(self.InfoInput)
        InfoRow.addWidget(self.ShowInfoButton)
        FormLayout.addLayout(InfoRow)

        FormLayout.addWidget(self.CreateFieldLabel("3. Notlar (ek açıklama)"))
        self.NotesInput = QTextEdit()
        self.NotesInput.setPlaceholderText("isteğe bağlı, serbest metin")
        self.NotesInput.setFixedHeight(70)
        FormLayout.addWidget(self.NotesInput)

        FormLayout.addWidget(self.CreateFieldLabel("Etiketler (seçmek için tıkla)"))
        self.TagScrollArea = QScrollArea()
        self.TagScrollArea.setWidgetResizable(True)
        self.TagScrollArea.setFixedHeight(84)
        self.TagScrollArea.setFrameShape(QFrame.NoFrame)
        TagContainer = QWidget()
        self.TagFlowLayout = FlowLayout(TagContainer, margin=2, spacing=6)
        TagContainer.setLayout(self.TagFlowLayout)
        self.TagScrollArea.setWidget(TagContainer)
        FormLayout.addWidget(self.TagScrollArea)

        NewTagRow = QHBoxLayout()
        self.NewTagInput = QLineEdit()
        self.NewTagInput.setPlaceholderText("yeni etiket adı")
        self.NewTagInput.returnPressed.connect(self.AddNewTag)
        NewTagButton = QPushButton("+")
        NewTagButton.setObjectName("Secondary")
        NewTagButton.setFixedWidth(36)
        NewTagButton.clicked.connect(self.AddNewTag)
        NewTagRow.addWidget(self.NewTagInput)
        NewTagRow.addWidget(NewTagButton)
        FormLayout.addLayout(NewTagRow)

        FormLayout.addSpacing(6)

        self.SaveButton = QPushButton("Kaydet")
        self.SaveButton.clicked.connect(self.SaveRecord)
        FormLayout.addWidget(self.SaveButton)

        FormLayout.addStretch()
        BodyLayout.addWidget(FormCard)

        # ---- Sağ: liste kartı (sade: sadece Başlık + Bilgi) ----
        ListCard = QFrame()
        ListCard.setObjectName("Card")
        ListLayout = QVBoxLayout(ListCard)
        ListLayout.setContentsMargins(18, 18, 18, 18)
        ListLayout.setSpacing(10)

        FilterRow = QHBoxLayout()
        self.SearchInput = QLineEdit()
        self.SearchInput.setPlaceholderText("Başlığa göre ara...")
        self.SearchInput.textChanged.connect(lambda: self.RefreshList())
        self.TagFilterCombo = QComboBox()
        self.TagFilterCombo.currentIndexChanged.connect(lambda: self.RefreshList())
        FilterRow.addWidget(self.SearchInput, 1)
        FilterRow.addWidget(self.TagFilterCombo)
        ListLayout.addLayout(FilterRow)

        # Sadece 3 sütun: Başlık, Bilgi, Aksiyonlar.
        # Notlar (ek açıklama) ve Etiketler artık listede DEĞİL, sadece
        # "Aç" butonuyla açılan RecordDetailDialog panelinde tam haliyle görünüyor.
        self.Table = QTableWidget(0, 3)
        self.Table.setHorizontalHeaderLabels(["Başlık", "Bilgi", ""])
        self.Table.verticalHeader().setVisible(False)
        self.Table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.Table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.Table.setSelectionMode(QAbstractItemView.SingleSelection)
        Header = self.Table.horizontalHeader()
        Header.setSectionResizeMode(0, QHeaderView.Stretch)
        Header.setSectionResizeMode(1, QHeaderView.Fixed)
        Header.setSectionResizeMode(2, QHeaderView.Fixed)
        self.Table.setColumnWidth(1, 110)
        self.Table.setColumnWidth(2, 140)  # Aç + Sil butonları için sabit genişlik
        ListLayout.addWidget(self.Table)

        BodyLayout.addWidget(ListCard, stretch=1)

    def CreateFieldLabel(self, Text):
        Label = QLabel(Text)
        Label.setStyleSheet("color:#9aa0a8; font-size:12px;")
        return Label

    # ---------- Etiket davranışları ----------

    def RefreshTags(self, SelectedIds=None):
        if SelectedIds is None:
            SelectedIds = self.GetSelectedTagIds()

        while self.TagFlowLayout.count():
            Item = self.TagFlowLayout.takeAt(0)
            Widget = Item.widget()
            if Widget:
                Widget.deleteLater()
        self.TagChipButtons = {}

        Tags = Database.GetAllTags()
        for Tag in Tags:
            ChipButton = QPushButton(Tag["ad"])
            ChipButton.setObjectName("TagChip")
            ChipButton.setCheckable(True)
            ChipButton.setChecked(Tag["id"] in SelectedIds)
            ChipButton.setContextMenuPolicy(Qt.CustomContextMenu)
            ChipButton.customContextMenuRequested.connect(
                lambda Position, TagId=Tag["id"], TagName=Tag["ad"]: self.ShowTagContextMenu(TagId, TagName)
            )
            self.TagFlowLayout.addWidget(ChipButton)
            self.TagChipButtons[Tag["id"]] = ChipButton

        PreviousSelection = self.TagFilterCombo.currentData()
        self.TagFilterCombo.blockSignals(True)
        self.TagFilterCombo.clear()
        self.TagFilterCombo.addItem("Tüm Etiketler", None)
        for Tag in Tags:
            self.TagFilterCombo.addItem(Tag["ad"], Tag["id"])
        Index = self.TagFilterCombo.findData(PreviousSelection)
        self.TagFilterCombo.setCurrentIndex(Index if Index >= 0 else 0)
        self.TagFilterCombo.blockSignals(False)

    def GetSelectedTagIds(self):
        return {TagId for TagId, Button in self.TagChipButtons.items() if Button.isChecked()}

    def AddNewTag(self):
        Name = self.NewTagInput.text().strip()
        if not Name:
            return
        Database.AddTag(Name)
        self.NewTagInput.clear()
        self.RefreshTags()

    def ShowTagContextMenu(self, TagId, TagName):
        Menu = QMenu(self)
        DeleteAction = Menu.addAction(f"'{TagName}' etiketini sil")
        SelectedAction = Menu.exec_(QCursor.pos())
        if SelectedAction == DeleteAction:
            Reply = QMessageBox.question(
                self, "Etiket silinsin mi?",
                f"'{TagName}' etiketi tamamen silinsin mi?\n"
                f"(Bu etikete sahip notlardan da kaldırılacak.)",
                QMessageBox.Yes | QMessageBox.No,
            )
            if Reply == QMessageBox.Yes:
                Database.DeleteTag(TagId)
                self.RefreshTags()
                self.RefreshList()

    # ---------- Diğer davranışlar ----------

    def ToggleInfoVisibility(self, IsVisible):
        self.InfoInput.setEchoMode(QLineEdit.Normal if IsVisible else QLineEdit.Password)
        self.ShowInfoButton.setText("🙈" if IsVisible else "👁")

    def RefreshList(self):
        SearchText = self.SearchInput.text().strip()
        TagId = self.TagFilterCombo.currentData() if hasattr(self, "TagFilterCombo") else None
        Records = Database.GetAllRecords(SearchText, TagId)
        self.Table.setRowCount(0)

        for Record in Records:
            RowIndex = self.Table.rowCount()
            self.Table.insertRow(RowIndex)

            self.Table.setItem(RowIndex, 0, QTableWidgetItem(Record["baslik"]))
            self.Table.setItem(RowIndex, 1, QTableWidgetItem("•" * 8))

            ActionsWidget = self.CreateRowActionsWidget(Record["id"])
            self.Table.setCellWidget(RowIndex, 2, ActionsWidget)
            self.Table.setRowHeight(RowIndex, 44)

    def CreateRowActionsWidget(self, RecordId):
        ContainerWidget = QWidget()
        ContainerWidget.setStyleSheet("background: transparent;")
        Layout = QHBoxLayout(ContainerWidget)
        Layout.setContentsMargins(4, 2, 4, 2)
        Layout.setSpacing(6)

        OpenButton = QPushButton("Aç")
        OpenButton.setObjectName("RowSecondary")
        OpenButton.setMinimumWidth(50)
        OpenButton.clicked.connect(lambda: self.OpenRecordDetail(RecordId))

        DeleteButton = QPushButton("Sil")
        DeleteButton.setObjectName("RowDanger")
        DeleteButton.setMinimumWidth(50)
        DeleteButton.clicked.connect(lambda: self.DeleteRecordRow(RecordId))

        Layout.addWidget(OpenButton)
        Layout.addWidget(DeleteButton)
        return ContainerWidget

    def OpenRecordDetail(self, RecordId):
        """"Aç" butonuna basılınca çağrılır: kaydın tüm bilgilerini (tam
        notlar dahil) gösteren ve doğrudan düzenlemeye izin veren paneli açar."""
        Dialog = RecordDetailDialog(RecordId, self)
        Dialog.exec_()
        self.RefreshList()

    def SaveRecord(self):
        Title = self.TitleInput.text().strip()
        Info = self.InfoInput.text().strip()
        NotesText = self.NotesInput.toPlainText().strip()
        TagIds = self.GetSelectedTagIds()

        if not Title or not Info:
            QMessageBox.warning(self, "Eksik bilgi", "Başlık ve bilgi alanları boş bırakılamaz.")
            return

        Database.AddRecord(Title, Info, NotesText, TagIds)
        self.ClearForm()
        self.RefreshList()

    def ClearForm(self):
        self.TitleInput.clear()
        self.InfoInput.clear()
        self.NotesInput.clear()
        self.ShowInfoButton.setChecked(False)
        self.RefreshTags(SelectedIds=set())

    def DeleteRecordRow(self, RecordId):
        Reply = QMessageBox.question(
            self, "Silinsin mi?",
            "Bu notu silmek istediğine emin misin?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if Reply == QMessageBox.Yes:
            Database.DeleteRecord(RecordId)
            self.RefreshList()
