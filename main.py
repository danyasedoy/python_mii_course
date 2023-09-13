from flask import Flask, render_template, request

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "/upload"


@app.route("/upload")
def index():
    return render_template('index.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save("upload/" + f.filename)
      return 'file uploaded successfully'

if __name__=="__main__":
    app.run(debug=True)
