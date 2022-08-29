from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/static/<file>')
def video(file):
   print(file)
   return render_template('stream.html',file=file)

if __name__ == '__main__':
   app.run(debug = True)
   