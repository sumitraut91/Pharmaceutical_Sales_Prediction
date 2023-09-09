import errno
from flask import Flask, request, render_template
from flask.helpers import send_file
from werkzeug.exceptions import Forbidden, HTTPException, NotFound, RequestTimeout, Unauthorized
from werkzeug.utils import secure_filename
import os
# TODO: refactor into own preprocess component
import pandas as pd
import numpy as np
# from modules import predict
import sys
import pickle

from zmq import Errno
# # sys.path.insert(0, '../modules')
# from modules import predict
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.errorhandler(NotFound)
def page_not_found_handler(e: HTTPException):
    return '<h1>404.html</h1>', 404


@app.errorhandler(Unauthorized)
def unauthorized_handler(e: HTTPException):
    return '<h1>401.html</h1>', 401


@app.errorhandler(Forbidden)
def forbidden_handler(e: HTTPException):
    return '<h1>403.html</h1>', 403


@app.errorhandler(RequestTimeout)
def request_timeout_handler(e: HTTPException):
    return '<h1>408.html</h1>', 408


FEATURES = ['Store', 'DayOfWeek', 'Open', 'Promo', 'StateHoliday',
            'SchoolHoliday', 'Year', 'Month', 'Day', 'WeekOfYear']


def make_prediction(df):
    loaded_model = pickle.load(open("C:/Users/Sumit/Desktop/Sumit/Internship/Project 2/models/model.pkl", 'rb'))
    df = df[FEATURES]
    result = loaded_model.predict(df)
    print("RESULT:", np.exp(result))
    return np.exp(result)


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    global class_names
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads/', secure_filename(f.filename))
        f.save(file_path)
        print(f)
        df = pd.read_csv(file_path, parse_dates=True, index_col="Date")
        df['Year'] = df.index.year
        df['Month'] = df.index.month
        df['Day'] = df.index.day
        df['WeekOfYear'] = df.index.weekofyear
        print(df.head())
        print("Index", df.index)
        # TODO: feed into sklearn pipeline
        # TODO: make prediction

    results = make_prediction(df)
    dates = df.index.values
    dates = dates.astype(str).tolist()
    # TODO: should return prediction data points
    df['Sales'] = results
    df['Sales'] = df['Sales'].astype(int)
    df.to_csv('output/response.csv')
    data = {
        "x": dates,
        "y": list(results)
    }
    return data

    # TODO: send prediction output back

    # Make prediction
    # shutil.rmtree('./uploads/zz')
    # os.mkdir('./uploads/zz')


@app.route('/download')
def download():
    return send_file('./output/response.csv', as_attachment=True)


@app.route('/prediction')
def predict():
    return render_template('file-upload.html')


@app.route('/analysis')
def analysis():
    return render_template('dashboard.html')
# TODO: refactor analysis route to prediction
# TODO: add analysis route.... analysis for existing data using powerbi

def initialize():
    # This function will run before the first request
    make_output_dir() 

@app.before_first_request
def make_output_dir():
    try:
        if not os.path.exists('./output'):
            os.makedirs('./output')
    except OSError as e:
        if e.errno != Errno.EEXIST:
            raise



@app.before_first_request
def make_uploads_dir():
    try:
        if not os.path.exists('./uploads'):
            os.makedirs('./uploads')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


if __name__ == '__main__':
    os.environ.setdefault('Flask_SETTINGS_MODULE', 'helloworld.settings')
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    port = int(os.environ.get("PORT", 33507))
    app.run(debug=True)