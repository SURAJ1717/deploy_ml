
# source env/Scripts/activate

from flask import Flask, render_template, url_for, request, jsonify, abort
import json, pymongo, joblib, numpy
from algorithms.process import process
from models.routes import model_app


app = Flask(__name__)

app.register_blueprint(model_app)

@app.route('/', methods=['GET'])
def dashboard():

    data = {}
    data['title'] = 'Dashboard'
    data['header_tag'] = 'AI Dashboard'

    return render_template('dashboard.html', data=data)


@app.route('/aqi', methods=['GET', 'POST'])
def aqi():

    data = {}
    data['title'] = 'AQI'
    data['header_tag'] = 'AQI Project'

    link = 'mongodb://127.0.0.1:27017'

    if request.method == 'POST':

        model = request.headers['algorithm']

        csv = request.files[u'csvFiles']

        formData = request.form

        initprocess = process()

        try:

            build_response =  initprocess.start_built(formData, model, csv)

        except Exception as e:

            abort(400, str(e))

        return build_response
    
    else:

        data['model_present'] = True
        data['build_model'] = {}

        client = pymongo.MongoClient(link)
        db = client['Models']
        table = db.BuildAlgorithmTable

        query = {"project": 'aqi'}
        result = table.find_one(query)

        data['build_model'] = result

        if result is None:
            data['model_present'] = False

        return render_template('projects/AQI/aqi_main.html', data=data)

@app.route('/aqi_predict', methods=['POST'])
def aqi_predict():

    formData = request.form
    link = 'mongodb://127.0.0.1:27017'

    client = pymongo.MongoClient(link)
    db = client['Models']
    table = db.BuildAlgorithmTable

    query = {"project": 'aqi'}
    query_result = table.find_one(query)

    if query_result is None:
        abort(400, 'Model Not Found')

    input_x = []

    for item in query_result['features']:
        input_x.append( int( formData.get(item) ) )

    final_features = [numpy.array(input_x)]

    filename = 'algorithms/all_fitted_models/aqi/'+ query_result['model_name'] +'.sav'
    loaded_model = joblib.load(filename)

    try:
        prediction_result = loaded_model.predict(final_features)
        output = round(prediction_result[0],2)
    except Exception as e:
        abort(400, str(e))

    return str(output)



if __name__ == "__main__":
    app.run(debug=True)