from flask import Flask, redirect, url_for, request, render_template, jsonify
from args import * 
from run import initialize_model, run_test
from flask_cors import CORS
import os 
import cv2
import time 

app = Flask(__name__)
CORS(app)
model = initialize_model(args) 
print(args.CPU)

@app.route('/upload')
def upload_file():
   return render_template('uploadv2.html')

@app.route('/recieve', methods = ['GET', 'POST'])
def recieve():
    if request.method == 'POST':
        print("recieved POST")
        f = request.files['file']
        # print("ok")
        f.save('video.mp4')
        cap = cv2.VideoCapture("video.mp4")
        length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        print("The number of frames is ", length )
        start_time = time.time()
        if args.CPU:
            print('prediction is done on CPU')
        # model = initialize_model(args) 
        json_data = run_test(args, model)
        end_time = time.time()
        print("Total time is ", end_time - start_time)
        return json_data