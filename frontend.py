from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify, session
from imutils.video import VideoStream
import requests
from pyzbar import pyzbar
import time
import cv2

frontend = Blueprint('frontend', __name__)

@frontend.route('/')
def index():
    return render_template('index.html')

@frontend.route('/pickup')
def pickup():
    headers = {'Authorization' : session['token']}
    req = requests.get("http://142.93.224.133/api/parcel/", headers=headers)
    return render_template('pickup.html', packages=req.json())

@frontend.route('/pickupdetail/<id>')
def pickupdetail(id):
    headers = {'Authorization': session['token']}
    req = requests.get("http://142.93.224.133/api/parcel/" + id, headers=headers)
    return render_template('pickupdetail.html' ,package=req.json())

@frontend.route('/scanned/', methods=['GET'])
def scanned():
    if(session['barcode_type'] == "QRCODE"):
        req = requests.get("http://142.93.224.133/api/login/" + session['barcode'])
        session['user'] = req.json()['user']
        session['token'] = req.json()['token']

    return render_template('package.html')

@frontend.route('/openlocker/<id>')
def openlocker(id):
    # DO Beautiful Things here to open the locker
    return render_template('index.html')

@frontend.route('/scanbarcode', methods=['GET','POST'])
def barcode():

    if request.method == 'GET':
        return render_template('index.html')

    if request.method == 'POST':
        vs = VideoStream(src=0).start()
        time.sleep(2.0)
        barcode_data = ""
        barcode_type = ""
        barcode_found = False

        while True:
            frame = vs.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY, dstCn=0)
            barcodes = pyzbar.decode(frame)

            for barcode in barcodes:
                barcode_data = barcode.data.decode("utf-8")
                barcode_type = barcode.type

                barcode_found = True

            if barcode_found:
                break

        cv2.destroyAllWindows()
        vs.stop()
        session['barcode'] = barcode_data;
        session['barcode_type'] = barcode_type;
        return jsonify({'status': 'done'})
