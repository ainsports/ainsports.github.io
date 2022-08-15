from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/upload')
def upload_file():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def uploader_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save('video.mp4')
      return 'file uploaded successfully'
if __name__ == '__main__':
   app.run(host='0.0.0.0' , port=5000)
   
