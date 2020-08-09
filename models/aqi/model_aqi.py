from flask import Flask, render_template, url_for, request, jsonify, abort
import json, pymongo, joblib, numpy, os, dotenv, uuid, boto3
from algorithms.process import process

## retrieve env var
dotenv.load_dotenv()
MONGODB_LINK = os.getenv('MONGODB_LINK', None)
S3_BUCKET = os.getenv('S3_BUCKET', None)
S3_KEY = os.getenv('S3_KEY', None)
S3_SECRET = os.getenv('S3_SECRET', None)

# assert MONGODB_LINK

class AQI:

    client = pymongo.MongoClient(MONGODB_LINK)

    db = client['Models']
    AI_db = client['AI']

    table = db.BuildAlgorithmTable
    csv_table = AI_db.csv

    s3_client = boto3.client('s3', aws_access_key_id=S3_KEY, aws_secret_access_key=S3_SECRET)

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

            query = {"project_tag": 'aqi'}

            result = AQI.table.find_one(query)
            project_csv = AQI.csv_table.find_one(query)

            data['build_model'] = result
            data['project_csv'] = project_csv

            if result is None:
                data['model_present'] = False

            return render_template('projects/AQI/aqi_main.html', data=data)


    def predict_AQI(self):

        formData = request.form

        query = {"project_tag": 'aqi'}
        query_result = AQI.table.find_one(query)

        if query_result is None:
            abort(400, 'Model Not Found')

        input_x = []

        features = query_result['features'].values()
        
        for item in features:
            input_x.append( formData.get(item['name']) ) 

        final_features = [numpy.array(input_x, dtype=float)]

        filename = 'algorithms/all_fitted_models/'+ query_result['project_tag'] +'/'+ query_result['model_slug'] +'.sav'
        loaded_model = joblib.load(filename)

        try:
            prediction_result = loaded_model.predict(final_features)
            output = round(prediction_result[0],2)
        except Exception as e:
            abort(400, str(e))

        return str(output)


    def upload_csv(self):
            
        data = {}

        formData = request.form

        csv = request.files['csv']

        content_type = request.mimetype

        uniqueFileName = uuid.uuid4().hex + csv.filename

        try:

            AQI.s3_client.put_object(Body=csv, Bucket=S3_BUCKET, Key=uniqueFileName, ContentType=content_type)

        except Exception as e:

            abort(400, str(e))
            
        s3_csv_url = uniqueFileName
        
        records = {
            '_id': uuid.uuid4().hex,
            'project_tag': formData.get('project_tag'),
            'csv': s3_csv_url,
        }
       
        AQI.csv_table.insert_one(records)
        
        data['reload'] = True

        return data


    def delete_csv(self):
            
        data = {}
       
        records = {
            'project_tag': 'aqi',
        }
       
        AQI.csv_table.delete_one(records)
        
        data['reload'] = True

        return data







































