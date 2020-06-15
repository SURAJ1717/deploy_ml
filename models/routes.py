from flask import request, abort
from __main__ import app
from models.models import Model

from sklearn.linear_model import LinearRegression


@app.route('/model_integrate', methods=['POST'])
def integrate():

    formData = request.form
    
    model = Model()
    
    try:

        model.model_integrate(formData)

    except Exception as e:

        abort(400, str(e))

    return 'Model saved successfully', 200


@app.route('/clear_integrated_model', methods=['POST'])
def remove_integrated():

    formData = request.form
    
    model = Model()
    
    try:

        model.clear_integrated_model(formData)

    except Exception as e:

        abort(400, str(e))

    return 'Model Removed successfully', 200
