from flask import Flask, redirect, url_for, request, render_template, jsonify
from args import * 
from run import initialize_model, run_test
from video import generateSummaryVideo
from flask_cors import CORS
import os 
import cv2
import time 
from flask import jsonify

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
        print(request.form)
        f = request.files['file']
        f.save('video.mp4')
        cap = cv2.VideoCapture("video.mp4")
        length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        print("The number of frames is ", length )
        start_time = time.time()
        if args.CPU:
            print('prediction is done on CPU')
        print(request.files)
        thresh = float(request.form['thresh'])
        print('prediction with threshold ', thresh) 
        json_data = run_test(args, model)
        end_time = time.time()
        print("Total time is ", end_time - start_time)
        return json_data


@app.route('/summarize', methods = ['GET', 'POST'])
def summarize():
    if request.method == 'POST':
        thresh = float(request.form['thresh'])
        print('summarizing with ', )
        video_url = generateSummaryVideo(thresh = thresh)
        return jsonify({'video_url':video_url})

@app.route('/static/<file>')
def video(file):
   return render_template('stream.html',file=file)

if __name__ == "__main__":
  app.run(host = "0.0.0.0")