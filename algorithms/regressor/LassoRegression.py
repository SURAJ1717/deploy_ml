from flask import jsonify
import json, joblib

import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, RandomizedSearchCV
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report, mean_absolute_error, mean_squared_error

from sklearn.linear_model import Lasso

class LassoRegressionClass:
    
    output = {}

    def build(self, project_tag, X, Y, train_x, test_x, train_y, test_y, params, cv=5, scoring=None, search_method='grid', n_iter=20):
        
        cv = int(cv)

        n_iter = int(n_iter)
        
        params = json.loads(params)

        model = Lasso()

        if search_method == 'grid':
            lasso_regressor = GridSearchCV(model, params, scoring=scoring, cv=cv, n_jobs=-1)
            lasso_regressor.fit(train_x,train_y)
        elif search_method == 'rand':
            lasso_regressor = RandomizedSearchCV(estimator=model, param_distributions=params, scoring=scoring, cv=cv, n_iter=n_iter, random_state=0, n_jobs=-1)
            lasso_regressor.fit(train_x,train_y)
        
        filename = 'algorithms/all_fitted_models/'+ project_tag +'/lasso_regression.sav'
        joblib.dump(lasso_regressor, filename)

        LassoRegressionClass.output['best_params'] = lasso_regressor.best_params_
        LassoRegressionClass.output['best_score'] = lasso_regressor.best_score_
        
        pred_y = lasso_regressor.predict(test_x)
        LassoRegressionClass.output['predicted_output'] = pred_y.tolist()
        
        mean_absolute_err = mean_absolute_error(test_y, pred_y)
        LassoRegressionClass.output['MAE'] = mean_absolute_err
        
        mean_squared_err = mean_squared_error(test_y, pred_y)
        LassoRegressionClass.output['MSE'] = mean_squared_err
        
        root_mean_squared_err = np.sqrt(mean_squared_err)
        LassoRegressionClass.output['RMSE'] = root_mean_squared_err

        actual_output = list(test_y)

        response = json.dumps({
                            'best_params': LassoRegressionClass.output['best_params'],
                            'best_score': LassoRegressionClass.output['best_score'],
                            'MAE': LassoRegressionClass.output['MAE'],
                            'MSE': LassoRegressionClass.output['MSE'],
                            'RMSE': LassoRegressionClass.output['RMSE'],
                            'predicted_output': LassoRegressionClass.output['predicted_output'],
                            'actual_output': actual_output,
                        })
        
        return response