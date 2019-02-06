import json

from flask import Blueprint, render_template, request, jsonify, session
from imutils.video import VideoStream
import requests
from pyzbar import pyzbar
import time
import cv2
import time
import serial

ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=115200
)

frontend = Blueprint('frontend', __name__)

@frontend.route('/')
def index():
    return render_template('index.html')

@frontend.route('/pickup')
def pickup():
    headers = {'Authorization' : session['token']}
    req = requests.get("http://142.93.224.133/api/parcel/", headers=headers)
    obj = json.loads(req.text)
    return render_template('process.html', packages=obj, send=False)

@frontend.route('/send')
def send():
    # Get all the parcels that are associated with this user
    headers = {'Authorization' : session['token']}
    req = requests.get("http://142.93.224.133/api/parcel/", headers=headers)
    obj = json.loads(req.text)
    return render_template('process.html', packages=obj, send=True)

@frontend.route('/packagedetail/<id>')
def pickupdetail(id):
    headers = {'Authorization': session['token']}
    req = requests.get("http://142.93.224.133/api/parcel/" + id, headers=headers)
    return render_template('packagedetail.html', package=req.json())

@frontend.route('/scanned/', methods=['GET'])
def scanned():
    # Check if we detect a QRCCODE or a normal barcode
    if(session['barcode_type'] == "QRCODE"):
        req = requests.get("http://142.93.224.133/api/login/" + session['barcode'])

        # Login our user with a QRCode
        if req.status_code == 201:
            session['user'] = req.json()['user']
            session['token'] = req.json()['token']
            return render_template('package.html', authorized=True)
        else:
            return render_template('package.html', authorized=False)
    else:

        # Fetch a parcel that's associated with te barcode if we can find it
        req = requests.get("http://142.93.224.133/api/parcel/delivery/" + session['barcode'])
        if req.status_code == 201:
            return render_template('process.html', package=req.json(), send=True)
        else:
            return render_template('index.html')

@frontend.route('/openlocker/<id>')
def openlocker(id):

    # Lampje aanzetten
    for i in range(2000):
        ser.write(id)

    # Do a call to  the ESP32
    return render_template('index.html')

@frontend.route('/scanbarcode', methods=['GET','POST'])
def barcode():

    # When we get a GET request just show our index page
    if request.method == 'GET':
        return render_template('index.html')

    # When a POST request arrives we kickoff the barcode scanning code
    if request.method == 'POST':
        # Start up the camera
        vs = VideoStream(src=0).start()
        # Wait till camera is initialized
        time.sleep(2.0)
        barcode_data = ""
        barcode_type = ""
        barcode_found = False

        # Keep looping until we detect a barcode
        while True:
            # Read a frame from our camera
            frame = vs.read()

            # Make it grayscale for easier detection
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY, dstCn=0)

            # Let pyzbar decode our image into barcode(s)
            barcodes = pyzbar.decode(frame)

            # Loop through all the found barcodes
            for barcode in barcodes:
                barcode_data = barcode.data.decode("utf-8")
                barcode_type = barcode.type

                barcode_found = True

            if barcode_found:
                break

        # Stop our camera
        vs.stop()

        # Add the found type and data to our session
        session['barcode'] = barcode_data
        session['barcode_type'] = barcode_type

        # Return a status for our client-side script
        return jsonify({'status': 'done'})
