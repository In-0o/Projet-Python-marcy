from cx_Freeze import setup, Executable

setup(
    name = "Appli Qrcode",
    version = "1.2",
    description = "Application pour lire et scanner des Qrcode, cette application est seulement en POC donc à ne pas utiliser en prod.",
    executables = [Executable("c:/Users/E0428120/Documents/Python/Appli Qrcode.py")],
)