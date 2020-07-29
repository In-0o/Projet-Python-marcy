
import sys
from pyzbar import pyzbar
from imutils.video import VideoStream
import imutils
import cv2
import argparse
import webbrowser
import time
from PyQt5.QtWidgets import QWidget, QLabel, QApplication
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap


class Thread(QThread):
	changePixmap = pyqtSignal(QImage)

	def run(self):
		vs = VideoStream(IntegratedCamera=True).start()
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

class App(QWidget):
	def __init__(self):
		super().__init__()
		self.title = 'PyQt5 Video'
		self.left = 100
		self.top = 100
		self.width = 640
		self.height = 480
		self.initUI()

	@pyqtSlot(QImage)
	def setImage(self, image):
		self.label.setPixmap(QPixmap.fromImage(image))

	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		self.resize(1800, 1200)
		# create a label
		self.label = QLabel(self)
		self.label.move(280, 120)
		self.label.resize(640, 480)
		th = Thread(self)
		th.changePixmap.connect(self.setImage)
		th.start()
		self.show()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())
