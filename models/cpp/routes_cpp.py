from flask import Flask, Blueprint, render_template

from models.cpp.model_cpp import CPP
model_cpp = Blueprint('model_cpp', __name__)


@model_cpp.route('/cpp', methods=['GET', 'POST'])
def process_CPP():

    cpp = CPP()
    return cpp.process_CPP()
    

@model_cpp.route('/cpp_predict', methods=['POST'])
def predict_CPP():

    cpp = CPP()
    return cpp.predict_CPP()


@model_cpp.route('/projects/CPP/includes/result_popup.html', methods=['GET'])
def open_model_built_Popup():

    return render_template('projects/CPP/includes/result_popup.html')


@model_cpp.route('/projects/CPP/popups/add_csv.html', methods=['GET'])
def open_upload_csv_Popup():

    return render_template('projects/CPP/popups/add_csv.html')


@model_cpp.route('/projects/cpp/csv-upload', methods=['POST'])
def upload_csv():

    cpp = CPP()
    return cpp.upload_csv()


@model_cpp.route('/projects/cpp/csv-delete', methods=['POST'])
def delete_csv():

    cpp = CPP()
    return cpp.delete_csv()