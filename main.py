from flask import Flask, render_template, request, url_for, redirect
import csv
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
            reader = csv.reader(f)
            headers = next(reader)
            data = list(reader)
        return render_template('file_data.html', headers=headers, data=data)

    if request.method == 'POST':
        try:
            rows_start = int(request.form.get('rowsStart'))
            rows_end = int(request.form.get('rowsEnd'))
            columns_start = int(request.form.get('columnsStart'))
            columns_end = int(request.form.get('columnsEnd'))
        except ValueError:
            return redirect(url_for('show_file'))

        with open('upload/' + filename) as f:
            reader = csv.reader(f)
            headers = next(reader)
            data = list(reader)

            if rows_start >= rows_end or not (0 <= rows_start <= len(data) - 1) or not (1 <= rows_end <= len(data)):
                return render_template('file_data.html', headers=headers, data=data, message="Некорректный ввод строк")

            if columns_start >= columns_end or not (0 <= columns_start <= len(headers) - 1) or not (1 <= columns_end <= len(headers)):
                return render_template('file_data.html', headers=headers, data=data, message="Некорректный ввод столбцов")

            headers = headers[columns_start:columns_end]
            data = [row[columns_start:columns_end] for row in data[rows_start:rows_end]]

        return render_template('file_data.html', headers=headers, data=data)


if __name__ == "__main__":
    app.run(debug=True)
