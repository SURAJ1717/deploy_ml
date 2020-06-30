from flask import Flask, Blueprint

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

