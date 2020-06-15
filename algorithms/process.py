from flask import jsonify
import json, operator, collections, os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, RandomizedSearchCV
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report, mean_absolute_error, mean_squared_error

from algorithms.regressor.LinearRegression import LinearRegressionClass
from algorithms.regressor.RidgeRegression import RidgeRegressionClass
from algorithms.regressor.LassoRegression import LassoRegressionClass
from algorithms.regressor.DecisionTreeRegressor import DecisionTreeRegressorClass
from algorithms.regressor.RandomForestRegressor import RandomForestRegressorClass
from algorithms.regressor.XGBOOSTRegressor import XGBOOSTRegressorClass

class process:

    o_r = {}

    def start_built(self, formData, selected_model, csv):

        process.o_r = {}
        
        process.o_r['linear_regressor_output'] = 'null'
        process.o_r['ridge_regressor_output'] = 'null'
        process.o_r['lasso_regressor_output'] = 'null'
        process.o_r['dt_regressor_output'] = 'null'
        process.o_r['rf_regressor_output'] = 'null'
        process.o_r['xgb_regressor_output'] = 'null'

        process.split(csv, formData)

        process.train_test_split(process.o_r['x'], process.o_r['y'])
        
        project_tag = formData.get('project_tag')

        if not os.path.exists("algorithms/all_fitted_models/{}".format(project_tag)):
            os.makedirs("algorithms/all_fitted_models/{}".format(project_tag))
            
        if selected_model == 'linear_regressor':
            LGR=LinearRegressionClass()
            process.o_r['linear_regressor_output'] = LGR.build(project_tag, process.o_r['x'], process.o_r['y'], process.o_r['train_x'], process.o_r['test_x'], process.o_r['train_y'], process.o_r['test_y'], cv=formData['cv'], scoring=formData['scoring'])

        if selected_model == 'ridge_regressor':
            RR=RidgeRegressionClass()
            process.o_r['ridge_regressor_output'] = RR.build(project_tag, process.o_r['x'], process.o_r['y'], process.o_r['train_x'], process.o_r['test_x'], process.o_r['train_y'], process.o_r['test_y'], formData['ridge_params'], cv=formData['cv'], scoring=formData['scoring'], search_method=formData['search_type'], n_iter=formData['n_iter'])

        if selected_model == 'lasso_regressor':
            LSSR=LassoRegressionClass()
            process.o_r['lasso_regressor_output'] = LSSR.build(project_tag, process.o_r['x'], process.o_r['y'], process.o_r['train_x'], process.o_r['test_x'], process.o_r['train_y'], process.o_r['test_y'], formData['lasso_params'], cv=formData['cv'], scoring=formData['scoring'], search_method=formData['search_type'], n_iter=formData['n_iter'])

        if selected_model == 'dt_regressor':
            DTR=DecisionTreeRegressorClass()
            process.o_r['dt_regressor_output'] = DTR.build(project_tag, process.o_r['x'], process.o_r['y'], process.o_r['train_x'], process.o_r['test_x'], process.o_r['train_y'], process.o_r['test_y'], formData['dt_params'], cv=formData['cv'], scoring=formData['scoring'], search_method=formData['search_type'], n_iter=formData['n_iter'])

        if selected_model == 'rf_regressor':
            RFR=RandomForestRegressorClass()
            process.o_r['rf_regressor_output'] = RFR.build(project_tag, process.o_r['x'], process.o_r['y'], process.o_r['train_x'], process.o_r['test_x'], process.o_r['train_y'], process.o_r['test_y'], formData['rf_params'], cv=formData['cv'], scoring=formData['scoring'], search_method=formData['search_type'], n_iter=formData['n_iter'])

        if selected_model == 'xgb_regressor':
            XGBR=XGBOOSTRegressorClass()
            process.o_r['xgb_regressor_output'] = XGBR.build(project_tag, process.o_r['x'], process.o_r['y'], process.o_r['train_x'], process.o_r['test_x'], process.o_r['train_y'], process.o_r['test_y'], formData['xgb_params'], cv=formData['cv'], scoring=formData['scoring'], search_method=formData['search_type'], n_iter=formData['n_iter'])

        response = json.dumps({
                            'linear_regressor_output': json.loads(process.o_r['linear_regressor_output']),
                            'ridge_regressor_output': json.loads(process.o_r['ridge_regressor_output']),
                            'lasso_regressor_output': json.loads(process.o_r['lasso_regressor_output']),
                            'dt_regressor_output': json.loads(process.o_r['dt_regressor_output']),
                            'rf_regressor_output': json.loads(process.o_r['rf_regressor_output']),
                            'xgb_regressor_output': json.loads(process.o_r['xgb_regressor_output']),
                            'independent_col':  list(process.o_r['independent_col']),
                            'dependent_col':  str(process.o_r['dependent_col']),
                        })

        return response
    

    @staticmethod
    def split(csv, formData):

        if csv:
            process.o_r['df'] = pd.read_csv(csv)

            if formData.get('skip_first') and formData.get('skip_first') != 'false':
                process.o_r['df'].drop(process.o_r['df'].iloc[:,0:1], inplace = True, axis = 1) 

            if formData.get('correlation') and formData.get('correlation') != 'false':
                process.remove_less_corr_features()

            if formData.get('top_imp_features') and formData.get('top_imp_features') != 'null':
                process.pluck_imp_features(formData)

            process.o_r['x'] = process.o_r['df'].iloc[:,:-1].values
            process.o_r['y'] = process.o_r['df'].iloc[:,-1].values

            df_columns = process.o_r['df'].columns
            process.o_r['independent_col'] = df_columns[:-1]
            process.o_r['dependent_col'] = df_columns[-1]

    @staticmethod
    def remove_less_corr_features():

        dependent_col = process.o_r['df'].iloc[:,-1]

        for cols in process.o_r['df'].columns:

            independent_col = process.o_r['df'][cols]
            correlation = dependent_col.corr(independent_col)
            
            if -0.2 < correlation < 0.2:
                process.o_r['df'].drop([cols], inplace = True, axis = 1)

    @staticmethod
    def pluck_imp_features(formData):
        
        cap = formData.get('top_imp_features')

        cap = int(cap) + 1
        
        dependent_col = process.o_r['df'].iloc[:,-1]

        features = {}

        for cols in process.o_r['df'].columns:

            independent_col = process.o_r['df'][cols]
            correlation = dependent_col.corr(independent_col)

            if correlation < 0:
                features[cols] = -1 * correlation
            else:
                features[cols] = correlation

        sorted_features = sorted(features.items(), key=lambda kv: kv[1], reverse=True)

        pluck_features = sorted_features[cap:]

        for cols, value in pluck_features:
            process.o_r['df'].drop([cols], inplace = True, axis = 1)


    @staticmethod
    def train_test_split(X, Y, test_size=0.25, random_state=0):
        process.o_r['train_x'], process.o_r['test_x'], process.o_r['train_y'], process.o_r['test_y'] = train_test_split(X, Y, test_size=test_size, random_state=random_state)
        

     

















