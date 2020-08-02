
# source env/Scripts/activate

from flask import Flask, render_template, url_for, request, jsonify, abort
import json, pymongo, joblib, numpy, os, dotenv, boto3
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


@app.route('/download_file/<fileName>', methods=['GET'])
def download(fileName):

    S3_BUCKET = os.getenv('S3_BUCKET', None)
    S3_KEY = os.getenv('S3_KEY', None)
    S3_SECRET = os.getenv('S3_SECRET', None)

    s3_client = boto3.client('s3', aws_access_key_id=S3_KEY, aws_secret_access_key=S3_SECRET)

    path = '/Users/SURAJ/Desktop/' + fileName

    try:

        s3_client.download_file(S3_BUCKET, fileName, path)

    except Exception as e:

        abort(400, str(e))

    return 'File downloaded'


if __name__ == "__main__":
    app.run(debug=True)