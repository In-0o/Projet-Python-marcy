from pyzbar import pyzbar
from imutils.video import VideoStream
import datetime
import time
import imutils
import cv2
import argparse
import webbrowser

print("[INFO] starting video stream...")
vs = VideoStream(IntegratedCamera=True).start()
time.sleep(2.0)
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
		webbrowser.open_new_tab(barcodeData)
		
		cv2.putText(frame, text, (x, y - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
	cv2.imshow("Barcode Scanner", frame)
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break
webbrowser.open_new_tab(barcodeData)
print("[INFO] cleaning up...")
cv2.destroyAllWindows()
vs.stop()
