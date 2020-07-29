import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qrcode
import os


qr=qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=5

)
color = ""

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Appli Qrcode'
        self.left = 100
        self.top = 100
        self.width = 1000
        self.height = 500
        self.initUI()
    




    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
    
        # Create textbox
        self.datatextbox = QLineEdit(self)
        self.datatextbox.move(520, 20)
        self.datatextbox.resize(460,40)

        self.combo = QComboBox(self)
        self.combo.addItems(["","Vert","Rouge","Blanc"])
        self.combo.activated[str].connect(self.onChanged )
        self.combo.move(520,80)
        self.combo.resize(460,40)

        self.Savetextbox = QLineEdit(self)
        self.Savetextbox.move(520, 140)
        self.Savetextbox.resize(460,40)

        self.Imglabel = QLabel(self)
        self.Imglabel.move(620,200)
        self.Imglabel.resize(280,280)
        
        self.label1 = QLabel(self)
        self.label1.move(20, 20)
        self.label1.resize(460,40)
        self.label1.setText("Contenu du Qrcode")
        self.label1.setAlignment(Qt.AlignCenter)
        self.label1.setFont(QFont("Arial rounded MT bold", 13))
        
        self.label2 = QLabel(self)
        self.label2.move(20, 80)
        self.label2.resize(460,40)
        self.label2.setText("Color (ne marche pas)")
        self.label2.setAlignment(Qt.AlignCenter)
        self.label2.setFont(QFont("Arial rounded MT bold", 13))

        self.label3 = QLabel(self)
        self.label3.move(20, 140)
        self.label3.resize(460,40)
        self.label3.setText("Nom du fichier")
        self.label3.setAlignment(Qt.AlignCenter)
        self.label3.setFont(QFont("Arial rounded MT bold", 13))
        
        # Create a button in the window
        self.button = QPushButton('Créer le Qrcode', self)
        self.button.move(120,200)
        self.button.resize(280,50)

        self.Clearbutton = QPushButton('Clear', self)
        self.Clearbutton.move(120,270)
        self.Clearbutton.resize(280,50)

        self.Exitbutton = QPushButton('Exit',self)
        self.Exitbutton.move(120, 340)
        self.Exitbutton.resize(280,50)

        # connect button to function on_click
        self.button.clicked.connect(self.on_click_create)
        self.Clearbutton.clicked.connect(self.on_click_clear)
        self.Exitbutton.clicked.connect(self.on_click_exit)
        self.show()






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
            QMessageBox.question(self, 'Error', "Erreur: Vous n'avez pas choisi de couleur.",QMessageBox.Ok)
        else:
            qr.add_data(datatextboxValue)
            qr.make(fit=True)
            img=qr.make_image(fill="black",back_color=color)
            if os.path.exists(SavetextboxValue+".png"):
                QMessageBox.question(self, 'Error', "Erreur: Le fichier "+SavetextboxValue+".png existe déjà.",QMessageBox.Ok)
            else:
                img.save(SavetextboxValue +".png")
                pixmap = QPixmap(SavetextboxValue +".png")
                self.Imglabel.setPixmap(pixmap)
                self.Imglabel.setScaledContents(True)
                QMessageBox.question(self, 'Info', "Le fichier: " + SavetextboxValue+".png à bien été créé.", QMessageBox.Ok)
        
    def on_click_clear(self):
        self.datatextbox.setText("")
        self.combo.currentText()
        self.Savetextbox.setText("")
        self.Imglabel.setPixmap(QPixmap())

    def on_click_exit(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
