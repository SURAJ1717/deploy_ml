from flask import Flask, render_template, url_for, request, jsonify, abort
import json, pymongo, joblib, numpy, os, dotenv
from algorithms.process import process
from bson.json_util import dumps

## retrieve env var
dotenv.load_dotenv()
MONGODB_LINK = os.getenv('MONGODB_LINK', None)
assert MONGODB_LINK

class SEED:

    client = pymongo.MongoClient(MONGODB_LINK)
    AI_db = client['AI']
    agorithms_table = AI_db.agorithms

    existing_tables = AI_db.list_collection_names()
    if 'agorithms' not in existing_tables:
        agorithms_table.insert_one({'_id': 0, 'construct': 'init'})


    def Algorithms(self):

        data = {}
        data['title'] = 'Algorithms'
        data['header_tag'] = 'AI Algorithms'
     
        return render_template('seeders/Algorithms/all-algorithms.html', data=data)


    def getALLAlgorithmsAPI(self):

        data = {}
        query = {}
        all_algorithms = SEED.agorithms_table.find(query)
            
        data['algorithms'] = [algorithm for algorithm in all_algorithms]

        return data


    # def add_Algorithms(self):

    #     formData = request.form

    #     return str(output)


