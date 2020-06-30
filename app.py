
# source env/Scripts/activate

from flask import Flask, render_template, url_for, request, jsonify, abort
import json, pymongo, joblib, numpy, os, dotenv
from algorithms.process import process



app = Flask(__name__)

from models.integration.routes import model_app
app.register_blueprint(model_app)

from models.aqi.routes_aqi import model_aqi
app.register_blueprint(model_aqi)

from models.seeder.routes_seed import seed_app
app.register_blueprint(seed_app)


@app.route('/', methods=['GET'])
def dashboard():

    data = {}
    data['title'] = 'Dashboard'
    data['header_tag'] = 'AI Dashboard'

    return render_template('dashboard.html', data=data)

if __name__ == "__main__":
    app.run(debug=True)