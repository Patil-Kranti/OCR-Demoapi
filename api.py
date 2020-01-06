from flask import Flask, request, redirect, jsonify, session
import json
from PIL import Image
import pytesseract
import argparse
import cv2
import base64
import os
import io
app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET', 'POST'])
def home():
    try:
        if request.method == 'POST':
            imagedata = request.json.get("image").encode()
            print("1")

            with open("img.png", "wb") as fh:
                fh.write(base64.decodebytes(imagedata))
            image = cv2.imread("img.png")
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            print("2")

            cv2.imshow("Image", gray)
            print("3")

            gray = cv2.threshold(gray, 0, 255,
                                 cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
            print("4")

            filename = "{}.png".format(os.getpid())
            cv2.imwrite(filename, gray)
            print("5")

            text = pytesseract.image_to_string(Image.open(filename))
            os.remove(filename)
            print(text)
            print("6")

            return jsonify(text)

        else:
            return "no result"
    except Exception as e:
        print(str(e))
        return str(e)


app.run(host='0.0.0.0', port=80)
