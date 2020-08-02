from flask import Flask, Blueprint, render_template

from models.aqi.model_aqi import AQI
model_aqi = Blueprint('model_aqi', __name__)


@model_aqi.route('/aqi', methods=['GET', 'POST'])
def process_AQI():

    aqi = AQI()
    return aqi.process_AQI()
    

@model_aqi.route('/aqi_predict', methods=['POST'])
def predict_AQI():

    aqi = AQI()
    return aqi.predict_AQI()


@model_aqi.route('/projects/AQI/includes/result_popup.html', methods=['GET'])
def open_model_built_Popup():

    return render_template('projects/AQI/includes/result_popup.html')


@model_aqi.route('/projects/AQI/popups/add_csv.html', methods=['GET'])
def open_upload_csv_Popup():

    return render_template('projects/AQI/popups/add_csv.html')


@model_aqi.route('/projects/aqi/csv-upload', methods=['POST'])
def upload_csv():

    aqi = AQI()
    return aqi.upload_csv()


@model_aqi.route('/projects/aqi/csv-delete', methods=['POST'])
def delete_csv():

    aqi = AQI()
    return aqi.delete_csv()