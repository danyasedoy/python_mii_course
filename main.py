from flask import Flask, render_template, request, url_for, redirect
import pandas
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "/upload"

filename = "data.csv"


@app.route('/uploader/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return render_template('upload.html')
    if request.method == 'POST':
        f = request.files['file']
        f.save("upload/" + filename)
        return redirect(url_for('show_file'))


@app.route('/file/', methods=['GET', 'POST'])
def show_file():
    if request.method == 'GET':
        if not os.path.isfile('upload/' + filename):
            return redirect(url_for('upload_file'))

        with open('upload/' + filename) as f:
            try:
                df = pandas.read_csv(f)
                headers = df.columns
                data = df.values
            except pandas.errors.EmptyDataError:
                return redirect(url_for('upload_file'))
        return render_template('file_data.html', headers=headers, data=data)

    if request.method == 'POST':
        with open('upload/' + filename) as f:
            df = pandas.read_csv(f)
            headers = df.columns
            data = df.values

        try:
            rows_start = int(request.form.get('rowsStart')) - 1 if request.form.get('rowsStart') else 0
            rows_end = int(request.form.get('rowsEnd'))  if request.form.get('rowsEnd') else len(data)
            columns_start = int(request.form.get('columnsStart')) - 1 if request.form.get('columnsStart') else 0
            columns_end = int(request.form.get('columnsEnd'))  if request.form.get('columnsEnd') else len(headers)
        except ValueError:
            return redirect(url_for('show_file'))

        headers = headers[columns_start:columns_end]
        data = [row[columns_start:columns_end] for row in data[rows_start:rows_end]]

        return render_template('file_data.html', headers=headers, data=data)


if __name__ == "__main__":
    app.run(debug=True)
