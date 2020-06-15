from flask import jsonify
import json, joblib

import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, RandomizedSearchCV
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report, mean_absolute_error, mean_squared_error

from sklearn.ensemble import RandomForestRegressor

class RandomForestRegressorClass:
    
    output = {}

    def build(self, project_tag, X, Y, train_x, test_x, train_y, test_y, params, cv=5, scoring=None, search_method='grid', n_iter=20):
        
        cv = int(cv)
        
        n_iter = int(n_iter)
        
        params = json.loads(params)

        model = RandomForestRegressor()

        if search_method == 'grid':
            rf_regressor = GridSearchCV(model, params, scoring=scoring, cv=cv, n_jobs=-1)
            rf_regressor.fit(train_x,train_y)
        elif search_method == 'rand':
            rf_regressor = RandomizedSearchCV(estimator=model, param_distributions=params, scoring=scoring, cv=cv, n_iter=n_iter, random_state=0, n_jobs=-1)
            rf_regressor.fit(train_x,train_y)
        
        filename = 'algorithms/all_fitted_models/'+ project_tag +'/rf_regression.sav'
        joblib.dump(rf_regressor, filename)

        RandomForestRegressorClass.output['best_params'] = rf_regressor.best_params_
        RandomForestRegressorClass.output['best_score'] = rf_regressor.best_score_
        
        pred_y = rf_regressor.predict(test_x)
        RandomForestRegressorClass.output['predicted_output'] = pred_y.tolist()
        
        mean_absolute_err = mean_absolute_error(test_y, pred_y)
        RandomForestRegressorClass.output['MAE'] = mean_absolute_err
        
        mean_squared_err = mean_squared_error(test_y, pred_y)
        RandomForestRegressorClass.output['MSE'] = mean_squared_err
        
        root_mean_squared_err = np.sqrt(mean_squared_err)
        RandomForestRegressorClass.output['RMSE'] = root_mean_squared_err

        actual_output = list(test_y)

        response = json.dumps({
                            'best_params': RandomForestRegressorClass.output['best_params'],
                            'best_score': RandomForestRegressorClass.output['best_score'],
                            'MAE': RandomForestRegressorClass.output['MAE'],
                            'MSE': RandomForestRegressorClass.output['MSE'],
                            'RMSE': RandomForestRegressorClass.output['RMSE'],
                            'predicted_output': RandomForestRegressorClass.output['predicted_output'],
                            'actual_output': actual_output,
                        })
        
        return response