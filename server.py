from flask import Flask, redirect, url_for, request, render_template, jsonify
from args import * 
from run import initialize_model, run_test
from video import generateSummaryVideo
from flask_cors import CORS
import os 
import cv2
import time 
from flask import jsonify
import datetime
from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    get_jwt_identity,
    unset_jwt_cookies,
    set_access_cookies,
)
from flask_cors import CORS
import datetime

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "your-secret-key"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(hours=1)  # Set token expiration to 1 hour
jwt = JWTManager(app)
CORS(app)

# Sample user data (replace with your user authentication logic)
users = {
    "user1": {
        "username": "user1",
        "password": "password1",
    }
}

model = initialize_model(args) 
print(args.CPU)

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = users.get(username)

    if user and password == user["password"]:
        access_token = create_access_token(identity=username)
        response = jsonify(message="Login successful", access_token=access_token)
        set_access_cookies(response, access_token)  # Set the access token as a cookie
        return response, 200
    else:
        return jsonify(message="Invalid credentials"), 401

@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(message=f"Hello, {current_user}! This is a protected endpoint.")

@app.route("/logout", methods=["POST"])
def logout():
    response = jsonify(message="Logged out successfully")
    unset_jwt_cookies(response)  # Clear the JWT cookies on logout
    return response, 200

@app.route('/upload')
@jwt_required()
def upload_file():
   return render_template('uploadv2.html')

@app.route('/recieve', methods = ['GET', 'POST'])
@jwt_required()
def recieve():
    if request.method == 'POST':
        print("recieved POST")
        print(request.form)
        f = request.files['file']
        time_stamp  = datetime.datetime.now().strftime('%m_%d_%Y_%H_%M_%S')
        video_path = f'video-{time_stamp}.mp4'
        f.save(video_path)
        cap = cv2.VideoCapture(video_path)
        length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        print("The number of frames is ", length )
        start_time = time.time()
        if args.CPU:
            print('prediction is done on CPU')
        print(request.files)
        thresh = float(request.form['thresh'])
        print('prediction with threshold ', thresh) 
        json_data = run_test(args, model, video_path)
        end_time = time.time()
        print("Total time is ", end_time - start_time)
        return json_data


@app.route('/summarize', methods = ['GET', 'POST'])
@jwt_required()
def summarize():
    if request.method == 'POST':
        thresh = float(request.form['thresh'])
        time_stamp = request.form['time_stamp']
        print('summarizing with ', thresh)
        video_url = generateSummaryVideo(time_stamp, thresh = thresh)
        return jsonify({'video_url':video_url})

@app.route('/static/<file>')
@jwt_required()
def video(file):
   return render_template('stream.html',file=file)

if __name__ == "__main__":
  app.run(host = "0.0.0.0")
