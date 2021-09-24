import os
import face_recognition
import base64
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS
import smtplib
import ssl
import random
import string

first_name = "Saptarshi"
last_name = "Paul"
email = "paulsapto@gmail.com"

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route('/')
def index():
	return 'Hello to PathLearn Flask API services!'

def saveImage(image, name, method):
    if (method == 'Register'):
        file_name = name + '.jpg'
        print(first_name)
        with open(file_name, "wb") as fh:
            fh.write(base64.b64decode(image))
    else:
        with open("unknown.jpg", "wb") as fh:
            fh.write(base64.b64decode(image))


def regImage(image, name):
    print('here')
    # image_data = image
    # with open("imageToSave.jpg", "wb") as fh:
    #     fh.write(base64.b64decode(image_data))

    image_path = name + '.jpg'
    print(image_path)
    known_image = face_recognition.load_image_file(image_path)
    print(known_image)
    unknown_image = face_recognition.load_image_file("unknown.jpg")

    refImage_encoding = face_recognition.face_encodings(known_image)[0]
    unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

    results = face_recognition.compare_faces([refImage_encoding], unknown_encoding)
    print(results)

    return results



@app.route("/api/register", methods=['POST'])
def register():
    userDetails = {

        'email': request.json['email'],
        'password': request.json['password'],
        'phone': request.json['phone'],
        'firstName': request.json['firstName'],
        'lastName': request.json['lastName'],
        'image': request.json['image'],
    }
    result = {
        'success': '1',
        'firstName': userDetails['firstName'],
        'lastName': userDetails['lastName'],
        'email': userDetails['email']
    }

    global first_name
    global last_name
    global email
    
    first_name = userDetails['firstName']
    last_name = userDetails['lastName']
    email = userDetails['email']
    saveImage(userDetails['image'], first_name, 'Register');
    # regImage()
    return jsonify({'result': result})


@app.route("/api/verification", methods=['POST'])
def verification():
    global first_name
    global last_name
    global email
    userVerification = {
        'image': request.json['image'],
        'email': request.json['email']
    }
    saveImage(userVerification['image'], None, 'verification')
    verified_face = regImage(userVerification['image'], first_name)
    if (verified_face[0] == True):
        verify = '1'
    else:
        verify = '0'

    print(verified_face[0])
    result = {
        'success': '1',
        'firstName': first_name,
        'lastName': last_name,
        'email': userVerification['email'],
        'verify': verify
    }
    return jsonify({'result': result})

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    print("Random string of length", length, "is:", result_str)
    return result_str

@app.route("/api/voting", methods=['GET'])
def voting():
    OTP = get_random_string(8)
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = "smtp.paul123@gmail.com"
    receiver_email = "paulsapto@gmail.com"
    password = "Abcd12341!"
    message = """\
    Subject: OTP

    This is your OTP Number: {}""".format(OTP)

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
    
    result = {
        'OTP': OTP
    }

    return jsonify({'result': result})

    
# with open("imageToSave.jpg", "wb") as fh:
# fh.write(base64.b64decode(image_data))


