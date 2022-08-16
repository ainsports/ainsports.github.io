from flask import Flask, redirect, url_for, request, render_template, jsonify
from args import * 
from run import initialize_model, run_test
from flask_cors import CORS
import os 


app = Flask(__name__)
CORS(app)
model = None 
print(args.CPU)

@app.route('/upload')
def upload_file():
   return render_template('uploadv2.html')

@app.route('/recieve', methods = ['GET', 'POST'])
def recieve():
    if request.method == 'POST':
        print("recieved POST")
        f = request.files['file']
        f.save('video.mp4')
        if args.CPU:
            print('prediction is done on CPU')
        dataset, model = initialize_model(args) 
        json_data = run_test(args, model, dataset)
        return json_data