from flask import Flask, render_template, url_for, request, jsonify, abort
import json, pymongo, joblib, numpy, os, dotenv
from algorithms.process import process

## retrieve env var
dotenv.load_dotenv()
MONGODB_LINK = os.getenv('MONGODB_LINK', None)
assert MONGODB_LINK

class AQI:

    client = pymongo.MongoClient(MONGODB_LINK)
    db = client['Models']
    table = db.BuildAlgorithmTable

    def process_AQI(self):

        data = {}
        data['title'] = 'AQI'
        data['header_tag'] = 'AQI Project'

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

            query = {"project": 'aqi'}
            result = AQI.table.find_one(query)

            data['build_model'] = result

            if result is None:
                data['model_present'] = False

            return render_template('projects/AQI/aqi_main.html', data=data)


    def predict_AQI(self):

        formData = request.form

        query = {"project": 'aqi'}
        query_result = AQI.table.find_one(query)

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

