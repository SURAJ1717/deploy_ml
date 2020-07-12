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

        project_tag = formData.get('project_tag')
        features = formData.get('features')
        model_name = formData.get('model_name')
        model_slug = formData.get('model_slug')

        features_list = json.loads(features)

        records = {
            '_id': uuid.uuid4().hex,
            'project_tag': project_tag,
            'features': features_list,
            'model_name': model_name,
            'model_slug': model_slug,
        }

        query = {"project_tag": project_tag}
        result = Model.table.find_one(query)

        if result is None:

            Model.table.insert_one(records)
        else:
            new_values = { "$set": { 'model_slug': model_slug, 'model_name': model_name} }

            Model.table.update_one(query, new_values)


    def clear_integrated_model(self, formData):

        project_tag = formData.get('project_tag')

        query = {"project_tag": project_tag}
        result = Model.table.find_one(query)

        if result is None:

            abort(400, 'Model Not Found')
        else:
            Model.table.delete_one(query)

