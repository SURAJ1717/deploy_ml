import pymongo, uuid, json, os, dotenv 
from flask import abort, url_for, redirect, jsonify

## retrieve env var
dotenv.load_dotenv()
MONGODB_LINK = os.getenv('MONGODB_LINK', None)
assert MONGODB_LINK

class Model:

    client = pymongo.MongoClient(MONGODB_LINK)
    db = client['Models']
    table = db.BuildAlgorithmTable

    def model_integrate(self, formData):

        project = formData.get('project')
        features = formData.get('features')
        model_name = formData.get('model_name')

        features_list = list(features.split(",")) 

        records = {
            '_id': uuid.uuid4().hex,
            'project': project,
            'features': features_list,
            'model_name': model_name,
        }

        query = {"project": project}
        result = Model.table.find_one(query)

        if result is None:

            Model.table.insert_one(records)
        else:
            new_values = { "$set": { 'features': features, 'model_name': model_name} }

            Model.table.update_one(query, new_values)


    def clear_integrated_model(self, formData):

        project_tag = formData.get('project')

        query = {"project": project_tag}
        result = Model.table.find_one(query)

        if result is None:

            abort(400, 'Model Not Found')
        else:
            Model.table.delete_one(query)

