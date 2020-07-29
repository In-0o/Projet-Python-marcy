##########################################################################
#                       Initialisation
##########################################################################

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qrcode
import os
from pyzbar import pyzbar
from imutils.video import VideoStream
import imutils
import cv2
import argparse
import webbrowser
import time
import win32gui
import win32con

##########################################################################
#                       Cacher console
##########################################################################

The_program_to_hide = win32gui.GetForegroundWindow()
win32gui.ShowWindow(The_program_to_hide, win32con.SW_HIDE)

##########################################################################
#                       Paramètres Qrcode
##########################################################################

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=3,
    border=4

)
color = ""

##########################################################################
#                       Scan du Qrcode
##########################################################################

class Thread(QThread):
    changePixmap = pyqtSignal(QImage)

    def run(self):
        vs = VideoStream(1).start()
        # USB8MDocCam
        time.sleep(1.0)
        while True:
            frame = vs.read()
            frame = imutils.resize(frame, width=400)
            barcodes = pyzbar.decode(frame)
            for barcode in barcodes:
                (x, y, w, h) = barcode.rect
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                barcodeData = barcode.data.decode("utf-8")
                barcodeType = barcode.type
                text = "{} ({})".format(barcodeData, barcodeType)
                cv2.putText(frame, text, (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                webbrowser.open_new_tab(barcodeData)
                time.sleep(5.0)
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgbImage.shape
            bytesPerLine = ch * w
            convertToQtFormat = QImage(
                rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
            p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
            self.changePixmap.emit(p)

##########################################################################
#                       Fenêtre principale
##########################################################################

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'App Qrcode - ITS MLE - POC - Ne pas utiliser en prod'
        self.left = 200
        self.top = 200
        self.width = 700
        self.height = 500
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)

        self.show()

##########################################################################
#                       Contenu de la fenêtre Principale
##########################################################################
class MyTableWidget(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(700, 500)

        # Add tabs
        self.tabs.addTab(self.tab1, "Création")
        self.tabs.addTab(self.tab2, "Scan")

        # Create first tab
        self.tab1.layout = QGridLayout(self)
        self.datatextbox = QLineEdit(self)
        self.datatextbox.setFixedHeight(45)
        self.combo = QComboBox(self)
        self.combo.addItems(["", "Vert", "Rouge", "Blanc"])
        self.combo.activated[str].connect(self.onChanged)
        self.combo.setFixedHeight(45)
        self.Savetextbox = QLineEdit(self)
        self.Savetextbox.setFixedHeight(45)
        self.Imglabel = QLabel(self)
        self.Imglabel.setAlignment(Qt.AlignCenter)
        self.Imglabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.label1 = QLabel(self)
        self.label1.setText("Contenu du Qrcode : ")
        self.label1.setAlignment(Qt.AlignCenter)
        self.label1.setFont(QFont("Arial rounded MT bold", 13))
        self.label1.setFixedHeight(45)
        self.label2 = QLabel(self)
        self.label2.setText("Color : ")
        self.label2.setAlignment(Qt.AlignCenter)
        self.label2.setFont(QFont("Arial rounded MT bold", 13))
        self.label2.setFixedHeight(45)
        self.label3 = QLabel(self)
        self.label3.setText("Nom de l'image : ")
        self.label3.setAlignment(Qt.AlignCenter)
        self.label3.setFont(QFont("Arial rounded MT bold", 13))
        self.label3.setFixedHeight(45)
        self.button = QPushButton('Créer le Qrcode', self)
        self.button.setFixedHeight(80)
        self.Clearbutton = QPushButton('Clear', self)
        self.Clearbutton.setFixedHeight(80)

        self.tab2.layout = QGridLayout(self)
        self.Vidlabel = QLabel(self)

        # connect button to function on_click
        self.button.clicked.connect(self.on_click_create)
        self.Clearbutton.clicked.connect(self.on_click_clear)
        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()

        # layout tab1

        self.tab1.layout.addWidget(self.label1, 0, 0, 1, 1)
        self.tab1.layout.addWidget(self.datatextbox, 0, 3, 1, 1)
        self.tab1.layout.addWidget(self.label2, 1, 0, 1, 1)
        self.tab1.layout.addWidget(self.combo, 1, 3, 1, 1)
        self.tab1.layout.addWidget(self.label3, 2, 0, 1, 1)
        self.tab1.layout.addWidget(self.Savetextbox, 2, 3, 1, 1)
        self.tab1.layout.addWidget(self.button, 3, 0, 1, 1)
        self.tab1.layout.addWidget(self.Imglabel, 3, 2, 2, 2)
        self.tab1.layout.addWidget(self.Clearbutton, 4, 0, 1, 1)
        self.tab1.setLayout(self.tab1.layout)

        # layout tab2

        self.tab2.layout.addWidget(self.Vidlabel, 0, 1)
        self.tab2.setLayout(self.tab2.layout)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

##########################################################################
#                       Actions pour créer Qrcode
##########################################################################
    @pyqtSlot()
    def onChanged(self):
        global color
        if (self.combo.currentText()) == "Vert":
            color = "green"
        elif (self.combo.currentText()) == "Rouge":
            color = "red"
        elif (self.combo.currentText()) == "Blanc":
            color = "white"

    def on_click_create(self):
        global color

        datatextboxValue = self.datatextbox.text()
        SavetextboxValue = self.Savetextbox.text()
        if (self.combo.currentText()) == "":
            QMessageBox.question(
                self, 'Error', "Erreur: Vous n'avez pas choisi de couleur.", QMessageBox.Ok)
        else:
            qr.add_data(datatextboxValue)
            qr.make(fit=True)
            img = qr.make_image(fill="black", back_color=color)
            nomUtilisateur = os.getlogin()
            file_name = ("C:\\Users\\" + nomUtilisateur +
                         "\Desktop\Qrcodes\\")
            if os.path.exists(file_name + SavetextboxValue+".png"):
                QMessageBox.question(self, 'Error', "Erreur: Le fichier " +
                                     SavetextboxValue+".png existe déjà.", QMessageBox.Ok)
            else:
                if os.path.exists(file_name):
                    img.save(file_name + SavetextboxValue + ".png")
                else:
                    os.makedirs(file_name)
                    img.save(file_name + SavetextboxValue + ".png")
                pixmap = QPixmap(file_name + SavetextboxValue + ".png")
                myScaledPixmap = pixmap.scaled(
                    self.Imglabel.height(), self.Imglabel.height(), Qt.KeepAspectRatio)
                self.Imglabel.setPixmap(myScaledPixmap)
                QMessageBox.question(self, 'Info', "Le fichier: " +
                                     SavetextboxValue+".png à bien été créé.", QMessageBox.Ok)

    def on_click_clear(self):
        self.datatextbox.setText("")
        self.combo.currentText()
        self.Savetextbox.setText("")
        self.Imglabel.setPixmap(QPixmap())

    def setImage(self, image):
        self.Vidlabel.setPixmap(QPixmap.fromImage(image))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
