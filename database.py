"""Veritabanı erişim katmanı (SQLite).

Not: Tablo/sütun adları (kayitlar, etiketler, baslik, bilgi, notlar, ad, ...)
bilinçli olarak Türkçe bırakıldı, çünkü bunlar zaten var olan "notlar.db"
dosyasının mevcut şemasını oluşturuyor. Bunları İngilizceye çevirmek bir
veri taşıma (migration) işlemi gerektirir ve mevcut kayıtlarınızı bozma
riski taşır. Sadece Python tarafındaki değişken/fonksiyon isimleri
İngilizceye çevrildi (PascalCase).
"""
import sqlite3
from pathlib import Path

import sys
from pathlib import Path

if getattr(sys, "frozen", False):
    # EXE olarak çalışıyorsa EXE'nin bulunduğu klasör
    BaseDirectory = Path(sys.executable).resolve().parent
else:
    # Python dosyası olarak çalışıyorsa .py dosyasının bulunduğu klasör
    BaseDirectory = Path(__file__).resolve().parent

DatabasePath = BaseDirectory / "notlar.db"


def GetConnection():
    Connection = sqlite3.connect(DatabasePath)
    Connection.row_factory = sqlite3.Row
    Connection.execute("PRAGMA foreign_keys = ON")
    return Connection


def InitializeDatabase():
    Connection = GetConnection()

    ExistingTables = {
        Row["name"] for Row in Connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
    }

    if "kayitlar" not in ExistingTables:
        Connection.execute(
            """
            CREATE TABLE kayitlar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                baslik TEXT NOT NULL,
                bilgi TEXT NOT NULL,
                notlar TEXT
            )
            """
        )
        # eski sürümden (isim, sifre, ek_bilgi şemalı "notlar" tablosu) veri taşı
        if "notlar" in ExistingTables:
            OldRecords = Connection.execute("SELECT * FROM notlar").fetchall()
            for OldRecord in OldRecords:
                Connection.execute(
                    "INSERT INTO kayitlar (baslik, bilgi, notlar) VALUES (?, ?, ?)",
                    (OldRecord["isim"], OldRecord["sifre"], OldRecord["ek_bilgi"]),
                )
            Connection.execute("DROP TABLE notlar")

    Connection.execute(
        """
        CREATE TABLE IF NOT EXISTS etiketler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ad TEXT NOT NULL UNIQUE
        )
        """
    )
    Connection.execute(
        """
        CREATE TABLE IF NOT EXISTS kayit_etiket (
            kayit_id INTEGER NOT NULL,
            etiket_id INTEGER NOT NULL,
            PRIMARY KEY (kayit_id, etiket_id),
            FOREIGN KEY (kayit_id) REFERENCES kayitlar(id) ON DELETE CASCADE,
            FOREIGN KEY (etiket_id) REFERENCES etiketler(id) ON DELETE CASCADE
        )
        """
    )
    Connection.commit()
    Connection.close()


def GetAllRecords(SearchText="", TagId=None):
    Connection = GetConnection()
    Query = """
        SELECT k.*, GROUP_CONCAT(DISTINCT e.ad) AS etiket_adlari
        FROM kayitlar k
        LEFT JOIN kayit_etiket ke ON ke.kayit_id = k.id
        LEFT JOIN etiketler e ON e.id = ke.etiket_id
    """
    WhereClauses = []
    Parameters = []
    if TagId:
        WhereClauses.append("k.id IN (SELECT kayit_id FROM kayit_etiket WHERE etiket_id = ?)")
        Parameters.append(TagId)
    if SearchText:
        WhereClauses.append("k.baslik LIKE ?")
        Parameters.append(f"%{SearchText}%")
    if WhereClauses:
        Query += " WHERE " + " AND ".join(WhereClauses)
    Query += " GROUP BY k.id ORDER BY k.id DESC"
    Rows = Connection.execute(Query, Parameters).fetchall()
    Connection.close()
    return Rows


def GetRecordTags(RecordId):
    Connection = GetConnection()
    Rows = Connection.execute(
        """
        SELECT e.id, e.ad FROM etiketler e
        JOIN kayit_etiket ke ON ke.etiket_id = e.id
        WHERE ke.kayit_id = ?
        ORDER BY e.ad
        """,
        (RecordId,),
    ).fetchall()
    Connection.close()
    return Rows


def GetAllTags():
    Connection = GetConnection()
    Rows = Connection.execute("SELECT * FROM etiketler ORDER BY ad").fetchall()
    Connection.close()
    return Rows


def AddTag(Name):
    Connection = GetConnection()
    try:
        Connection.execute("INSERT INTO etiketler (ad) VALUES (?)", (Name,))
        Connection.commit()
    except sqlite3.IntegrityError:
        pass  # bu isimde etiket zaten var
    finally:
        Connection.close()


def DeleteTag(TagId):
    Connection = GetConnection()
    Connection.execute("DELETE FROM etiketler WHERE id=?", (TagId,))
    Connection.commit()
    Connection.close()


def AddRecord(Title, Info, NotesText, TagIds=None):
    Connection = GetConnection()
    Cursor = Connection.execute(
        "INSERT INTO kayitlar (baslik, bilgi, notlar) VALUES (?, ?, ?)",
        (Title, Info, NotesText),
    )
    RecordId = Cursor.lastrowid
    if TagIds:
        Connection.executemany(
            "INSERT OR IGNORE INTO kayit_etiket (kayit_id, etiket_id) VALUES (?, ?)",
            [(RecordId, TagId) for TagId in TagIds],
        )
    Connection.commit()
    Connection.close()


def UpdateRecord(RecordId, Title, Info, NotesText, TagIds=None):
    Connection = GetConnection()
    Connection.execute(
        "UPDATE kayitlar SET baslik=?, bilgi=?, notlar=? WHERE id=?",
        (Title, Info, NotesText, RecordId),
    )
    Connection.execute("DELETE FROM kayit_etiket WHERE kayit_id=?", (RecordId,))
    if TagIds:
        Connection.executemany(
            "INSERT OR IGNORE INTO kayit_etiket (kayit_id, etiket_id) VALUES (?, ?)",
            [(RecordId, TagId) for TagId in TagIds],
        )
    Connection.commit()
    Connection.close()


def DeleteRecord(RecordId):
    Connection = GetConnection()
    Connection.execute("DELETE FROM kayitlar WHERE id=?", (RecordId,))
    Connection.commit()
    Connection.close()
