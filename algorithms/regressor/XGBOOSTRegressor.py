from flask import jsonify
import json, joblib

import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, RandomizedSearchCV
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report, mean_absolute_error, mean_squared_error

import xgboost as xgb

class XGBOOSTRegressorClass:
    
    output = {}

    def build(self, project_tag, algorithm_slug, X, Y, train_x, test_x, train_y, test_y, params, cv=5, scoring=None, search_method='grid', n_iter=20):
        
        cv = int(cv)

        n_iter = int(n_iter)
        
        params = json.loads(params)

        model = xgb.XGBRegressor()

        if search_method == 'grid':
            xgb_regressor = GridSearchCV(model, params, scoring=scoring, cv=cv, n_jobs=-1)
            xgb_regressor.fit(train_x,train_y)
        elif search_method == 'rand':
            xgb_regressor = RandomizedSearchCV(estimator=model, param_distributions=params, scoring=scoring, cv=cv, n_iter=n_iter, random_state=0, n_jobs=-1)
            xgb_regressor.fit(train_x,train_y)
        
        filename = 'algorithms/all_fitted_models/' + project_tag + '/' + algorithm_slug + '.sav'

        joblib.dump(xgb_regressor, filename)

        XGBOOSTRegressorClass.output['best_params'] = xgb_regressor.best_params_
        XGBOOSTRegressorClass.output['best_score'] = xgb_regressor.best_score_
        
        pred_y = xgb_regressor.predict(test_x)
        XGBOOSTRegressorClass.output['predicted_output'] = pred_y.tolist()

        mean_absolute_err = mean_absolute_error(test_y, pred_y)
        XGBOOSTRegressorClass.output['MAE'] = mean_absolute_err
        
        mean_squared_err = mean_squared_error(test_y, pred_y)
        XGBOOSTRegressorClass.output['MSE'] = mean_squared_err
        
        root_mean_squared_err = np.sqrt(mean_squared_err)
        XGBOOSTRegressorClass.output['RMSE'] = root_mean_squared_err  

        actual_output = list(test_y)

        response = json.dumps({
                            'best_params': XGBOOSTRegressorClass.output['best_params'],
                            'best_score': XGBOOSTRegressorClass.output['best_score'],
                            'MAE': XGBOOSTRegressorClass.output['MAE'],
                            'MSE': XGBOOSTRegressorClass.output['MSE'],
                            'RMSE': XGBOOSTRegressorClass.output['RMSE'],
                            'predicted_output': XGBOOSTRegressorClass.output['predicted_output'],
                            'actual_output': actual_output,
                        })
        
        return response