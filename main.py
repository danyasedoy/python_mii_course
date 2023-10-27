from flask import Flask, render_template, request, url_for, redirect

import pandas
import os
import datetime
from chart import create_high_avg_chart, create_low_avg_chart
import data_analysis
import average_data_add

from io import BytesIO
import base64

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

                emptyValues = {}

                for column in headers:
                    emptyValues[column] = len(df[pandas.isnull(df[column])])

                

            except pandas.errors.EmptyDataError:
                return redirect(url_for('upload_file'))
        return render_template('file_data.html', headers=headers, data=data, emptyValues = emptyValues)

    if request.method == 'POST':
        with open('upload/' + filename) as f:
            df = pandas.read_csv(f)
            headers = df.columns
            data = df.values

            emptyValues = {}

            for column in headers:
                emptyValues[column] = len(df[pandas.isnull(df[column])])


        try:
            rows_start = int(request.form.get('rowsStart')) - 1 if request.form.get('rowsStart') else 0
            rows_end = int(request.form.get('rowsEnd'))  if request.form.get('rowsEnd') else len(data)
            columns_start = int(request.form.get('columnsStart')) - 1 if request.form.get('columnsStart') else 0
            columns_end = int(request.form.get('columnsEnd'))  if request.form.get('columnsEnd') else len(headers)
        except ValueError:
            return redirect(url_for('show_file'))

        headers = headers[columns_start:columns_end]
        data = [row[columns_start:columns_end] for row in data[rows_start:rows_end]]

        return render_template('file_data.html', headers=headers, data=data, emptyValues = emptyValues)

@app.route('/analysis/', methods=['GET', 'POST'])
def analysis():
        if not os.path.isfile('upload/' + filename):
            return redirect(url_for('upload_file'))

        with open('upload/' + filename) as f:
            try:
                df = pandas.read_csv(f)

                df['Date'] = df['Date'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))

                summer_data = data_analysis.summer_analysis(df)
                winter_data = data_analysis.winter_analysis(df)
                all_years_data = data_analysis.all_years_analysis(df)

                year = None
                if request.method == 'POST':
                    if request.form['year']:
                        year = int(request.form['year'])

            except pandas.errors.EmptyDataError:
                return redirect(url_for('upload_file'))
            
            if year:
                year_data = data_analysis.year_analysis(df, year)
                return render_template(
                'analysis_data.html',
                    summer_data=summer_data,
                    winter_data=winter_data,
                    all_years_data=all_years_data,
                    year_data = year_data)
            


            return render_template(
                'analysis_data.html',
                    summer_data=summer_data,
                    winter_data=winter_data,
                    all_years_data=all_years_data
            )
        
@app.route('/analysis/average', methods=['GET'])
def analysis_average():
        if not os.path.isfile('upload/data_avg.csv'):
            return redirect(url_for('upload_file'))

        with open('upload/data_avg.csv') as f:
            try:
                df = pandas.read_csv(f)

                df['Date'] = df['Date'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))

                summer_data = data_analysis.summer_analysis(df)
                winter_data = data_analysis.winter_analysis(df)
                all_years_data = data_analysis.all_years_analysis(df)

            except pandas.errors.EmptyDataError:
                return redirect(url_for('upload_file'))
            return render_template(
                'analysis_data.html',
                    summer_data=summer_data,
                    winter_data=winter_data,
                    all_years_data=all_years_data
            )
    
@app.route('/average/', methods=['GET'])
def add_avg_data():
    with open('upload/' + filename) as f:
            try:
                df = pandas.read_csv(f)
                headers = df.columns
                data = df.values
                print("Размер оригинала: " + str(len(data)))

            except pandas.errors.EmptyDataError:
                return redirect(url_for('upload_file'))
            
    average_data_add.add_avg_data(df)
    with open('upload/data_avg.csv') as f:
        try:
            df = pandas.read_csv(f)
            headers = df.columns
            data = df.values
            print("Размер : " + str(len(data)))

        except pandas.errors.EmptyDataError:
            return redirect(url_for('upload_file'))
    return render_template('avg_data.html', headers=headers, data=data)

@app.route('/chart/<type>', methods=['GET'])
def show_chart(type):
    with open('upload/' + filename) as f:
        try:
            df = pandas.read_csv(f)
        except pandas.errors.EmptyDataError:
            return redirect(url_for('upload_file'))

    with open('upload/data_avg.csv') as f:
        try:
            new_df = pandas.read_csv(f)
        except pandas.errors.EmptyDataError:
            return redirect(url_for('upload_file'))
    if type == "high":
        fig = create_high_avg_chart(df, new_df)
    if type == "low":
        fig = create_low_avg_chart(df, new_df)
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"
    
if __name__ == "__main__":
    app.run(debug=True)
