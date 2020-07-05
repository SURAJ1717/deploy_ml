from flask import Flask, render_template, url_for, request, jsonify, abort
import json, pymongo, joblib, numpy, os, dotenv, uuid
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
    hyper_params_table = AI_db.hyper_params

    def Algorithms(self):

        existing_tables = SEED.AI_db.list_collection_names()
        if 'agorithms' not in existing_tables:
            SEED.agorithms_table.insert_one({'_id': 0, 'construct': 'init'})

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


    def add_Algorithms(self):

        data = {}
        formData = request.form

        records = {
            '_id': uuid.uuid4().hex,
            'name': formData.get('name'),
            'slug': formData.get('slug'),
            'type': formData.get('type'),
        }
       
        SEED.agorithms_table.insert_one(records)
        
        data['reload'] = True

        return data


    def update_Algorithms(self):

        data = {}
        formData = request.form

        id = {
            '_id': formData.get('_id')
        }
               
        records = {
            'name': formData.get('name'),
            'slug': formData.get('slug'),
            'type': formData.get('type'),
        }

        updates = { "$set" : records }

        SEED.agorithms_table.update_one(id, updates)
        
        data['reload'] = True

        return data


    def delete_Algorithms(self):

        data = {}
        formData = request.form

        id = {
            '_id': formData.get('_id')
        }
       
        SEED.agorithms_table.delete_one(id)
        
        data['reload'] = True

        return data

# ========================================================================== #

    def HyperParams(self, algorithm_id):

        existing_tables = SEED.AI_db.list_collection_names()
        if 'hyper_params' not in existing_tables:
            SEED.hyper_params_table.insert_one({'_id': 0, 'construct': 'init'})

        data = {}
        data['title'] = 'Hyper Parameters'
        data['header_tag'] = 'Hyper Parameters'
        data['algorithm_id'] = algorithm_id
     
        return render_template('seeders/Algorithms/hyper-params.html', data=data)


    def getALLHyperParamsAPI(self, algorithm_id):

        data = {}
        query = {'algorithm_id': algorithm_id}
        hyper_params = SEED.hyper_params_table.find(query)
            
        data['hyper_params'] = [params for params in hyper_params]

        return data


    def add_hyper_params(self):

        data = {}
        formData = request.form

        params = formData.get('params').split(",")

        records = {
            '_id': uuid.uuid4().hex,
            'name': formData.get('name'),
            'slug': formData.get('slug'),
            'algorithm_id': formData.get('algorithm_id'),
            'params': params,
        }
       
        SEED.hyper_params_table.insert_one(records)
        
        data['reload'] = True

        return data


    def update_hyper_params(self):

        data = {}
        formData = request.form

        id = {
            '_id': formData.get('_id')
        }
               
        params = formData.get('params').split(",")

        records = {
            'name': formData.get('name'),
            'slug': formData.get('slug'),
            'algorithm_id': formData.get('algorithm_id'),
            'params': params,
        }

        updates = { "$set" : records }

        SEED.hyper_params_table.update_one(id, updates)
        
        data['reload'] = True

        return data


    def delete_hyper_params(self):

        data = {}
        formData = request.form

        id = {
            '_id': formData.get('_id')
        }
       
        SEED.hyper_params_table.delete_one(id)
        
        data['reload'] = True

        return data














