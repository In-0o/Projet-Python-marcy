import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Tab(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("liseuse de BD")
        self.setWindowIcon(QIcon("icon.png"))

        vbox = QVBoxLayout()
        tabWidget = QTabWidget()

        tabWidget.addTab(TabContact(),"Contact Details")

        vbox.addWidget(tabWidget)

        self.setlayout(vbox)

if __name__ == '__main__':

       app = QApplication(sys.argv)
       window = Tab()
       window.show()
       sys.exit(app.exec_())