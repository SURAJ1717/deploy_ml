from flask import Flask, Blueprint, render_template

from models.seeder.my_seeds import SEED
seed_app = Blueprint('seed_app', __name__)

# Algorithm API =======================================================================
@seed_app.route('/view_seed/algorithms', methods=['GET'])
def Algorithms():

    aqi = SEED()
    return aqi.Algorithms()

@seed_app.route('/api_seed/algorithms/all', methods=['POST'])
def getALLAlgorithmsAPI():

    aqi = SEED()
    return aqi.getALLAlgorithmsAPI()
    
@seed_app.route('/seeders/Algorithms/popup/add-algorithm.html', methods=['GET'])
def add_Algorithms_Popup():

    return render_template('seeders/Algorithms/popup/add-algorithm.html')

@seed_app.route('/api_seed/add_algorithms', methods=['POST'])
def add_Algorithms():

    aqi = SEED()
    return aqi.add_Algorithms()

@seed_app.route('/seeders/Algorithms/popup/edit-algorithm.html', methods=['GET'])
def edit_Algorithms_Popup():

    return render_template('seeders/Algorithms/popup/edit-algorithm.html')

@seed_app.route('/api_seed/update_algorithms', methods=['POST'])
def update_Algorithms():

    aqi = SEED()
    return aqi.update_Algorithms()

@seed_app.route('/api_seed/delete_algorithms', methods=['POST'])
def delete_Algorithms():

    aqi = SEED()
    return aqi.delete_Algorithms()



# Algorithm Hyper Param =================================================================
@seed_app.route('/api_seed/algorithm/<algorithm_id>/hyper-params', methods=['GET'])
def HyperParams(algorithm_id):

    aqi = SEED()
    return aqi.HyperParams(algorithm_id)

@seed_app.route('/api_seed/<algorithm_id>/HyperParams/all', methods=['POST'])
def getALLHyperParamsAPI(algorithm_id):

    aqi = SEED()
    return aqi.getALLHyperParamsAPI(algorithm_id)
    
@seed_app.route('/seeders/Algorithms/popup/add-hyper-param.html', methods=['GET'])
def add_HyperParam_Popup():

    return render_template('seeders/Algorithms/popup/add-hyper-param.html')

@seed_app.route('/api_seed/hyper-params/add', methods=['POST'])
def add_hyper_params():

    aqi = SEED()
    return aqi.add_hyper_params()

@seed_app.route('/seeders/Algorithms/popup/edit-hyper-param.html', methods=['GET'])
def edit_HyperParam_Popup():

    return render_template('seeders/Algorithms/popup/edit-hyper-param.html')

@seed_app.route('/api_seed/hyper-params/update', methods=['POST'])
def update_hyper_params():

    aqi = SEED()
    return aqi.update_hyper_params()

@seed_app.route('/api_seed/hyper-params/delete', methods=['POST'])
def delete_hyper_params():

    aqi = SEED()
    return aqi.delete_hyper_params()























