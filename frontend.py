from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from imutils.video import VideoStream
from pyzbar import pyzbar
from pyzbar.pyzbar import ZBarSymbol
import argparse
import datetime
import imutils
import time
import cv2

frontend = Blueprint('frontend', __name__)

@frontend.route('/')
def index():
    return render_template('index.html')

@frontend.route('/scanned/<barcode>', methods=['GET'])
def scanned(barcode):
    return render_template('package.html',data=barcode)

@frontend.route('/scanbarcode', methods=['GET','POST'])
def barcode():
    if request.method == 'GET':
        return render_template('index.html')

    if request.method == 'POST':
        vs = VideoStream(src=0).start()
        time.sleep(2.0)
        barcode_data = ""
        barcodeFound = False

        while True:
            frame = vs.read()
            #frame = imutils.resize(frame, width=400)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY, dstCn=0)
            barcodes = pyzbar.decode(frame)

            for barcode in barcodes:
                barcodeData = barcode.data.decode("utf-8")
                barcodeType = barcode.type

                barcodeFound = True
                barcode_data = barcodeData

            if barcodeFound:
                break

        cv2.destroyAllWindows()
        vs.stop()
        return jsonify({'status': 'done', 'barcode': barcode_data})
