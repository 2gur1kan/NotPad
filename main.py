"""Uygulama giriş noktası."""
import os
import sys

# Windows'ta "Qt platform plugin bulunamadı" hatasını önlemek için:
# 1) PyQt5'in plugin klasörünü elle belirtiyoruz
# 2) PyQt5'in "bin" klasörünü (Qt5Core.dll vb. çekirdek dosyaların olduğu yer)
#    hem PATH'e hem de DLL arama dizinlerine ekliyoruz — qwindows.dll bu
#    dosyalar bulunamadan yüklenemiyor ve Qt bunu "plugin bulunamadı" diye
#    yanıltıcı bir hata olarak gösteriyor.
try:
    import PyQt5
    Qt5Directory = os.path.join(os.path.dirname(PyQt5.__file__), "Qt5")
    BinDirectory = os.path.join(Qt5Directory, "bin")
    PluginsDirectory = os.path.join(Qt5Directory, "plugins")
    PlatformsDirectory = os.path.join(PluginsDirectory, "platforms")

    if os.path.isdir(PluginsDirectory):
        os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = PluginsDirectory

    if os.path.isdir(BinDirectory):
        os.environ["PATH"] = BinDirectory + os.pathsep + os.environ.get("PATH", "")
        if hasattr(os, "add_dll_directory"):
            os.add_dll_directory(BinDirectory)

    if os.path.isdir(PlatformsDirectory) and hasattr(os, "add_dll_directory"):
        os.add_dll_directory(PlatformsDirectory)
except Exception as Error:
    print(f"[Qt tanı] Plugin yolu ayarlanırken hata: {Error}")

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from database import InitializeDatabase
from styles import AppStyleSheet
from main_window import MainWindow


def Main():
    InitializeDatabase()
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    Application = QApplication(sys.argv)
    Application.setStyleSheet(AppStyleSheet)
    Window = MainWindow()
    Window.show()
    sys.exit(Application.exec_())


if __name__ == "__main__":
    Main()
