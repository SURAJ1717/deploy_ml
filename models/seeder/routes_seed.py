from flask import Flask, Blueprint, render_template

from models.seeder.my_seeds import SEED
seed_app = Blueprint('seed_app', __name__)


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

# @seed_app.route('/api_seed/add_algorithms', methods=['POST'])
# def add_Algorithms():

#     aqi = SEED()
#     return aqi.add_Algorithms()


# @seed_app.route('/api_seed/update_algorithms', methods=['POST'])
# def update_Algorithms():

#     aqi = SEED()
#     return aqi.update_Algorithms()


# @seed_app.route('/api_seed/delete_algorithms', methods=['POST'])
# def delete_Algorithms():

#     aqi = SEED()
#     return aqi.delete_Algorithms()