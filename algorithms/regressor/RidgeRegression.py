
import numpy as np
import json, joblib
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, RandomizedSearchCV
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report, mean_absolute_error, mean_squared_error

from sklearn.linear_model import Ridge

class RidgeRegressionClass:
    
    output = {}

    def build(self, project_tag, X, Y, train_x, test_x, train_y, test_y, params, cv=5, scoring=None, search_method='grid', n_iter=20):
        
        cv = int(cv)
        
        n_iter = int(n_iter)
        
        params = json.loads(params)

        model = Ridge()

        if search_method == 'grid':
            ridge_regressor = GridSearchCV(model, params, scoring=scoring, cv=cv, n_jobs=-1)
            ridge_regressor.fit(train_x,train_y)
        elif search_method == 'rand':
            ridge_regressor = RandomizedSearchCV(estimator=model, param_distributions=params, scoring=scoring, cv=cv, n_iter=n_iter, random_state=0, n_jobs=-1)
            ridge_regressor.fit(train_x,train_y)

        filename = 'algorithms/all_fitted_models/'+ project_tag +'/ridge_regression.sav'
        joblib.dump(ridge_regressor, filename)

        RidgeRegressionClass.output['best_params'] = ridge_regressor.best_params_
        RidgeRegressionClass.output['best_score'] = ridge_regressor.best_score_
        
        pred_y = ridge_regressor.predict(test_x)
        RidgeRegressionClass.output['predicted_output'] = pred_y.tolist()
        
        mean_absolute_err = mean_absolute_error(test_y, pred_y)
        RidgeRegressionClass.output['MAE'] = mean_absolute_err
        
        mean_squared_err = mean_squared_error(test_y, pred_y)
        RidgeRegressionClass.output['MSE'] = mean_squared_err
        
        root_mean_squared_err = np.sqrt(mean_squared_err)
        RidgeRegressionClass.output['RMSE'] = root_mean_squared_err
        
        actual_output = list(test_y)

        response = json.dumps({
                            'best_params': RidgeRegressionClass.output['best_params'],
                            'best_score': RidgeRegressionClass.output['best_score'],
                            'MAE': RidgeRegressionClass.output['MAE'],
                            'MSE': RidgeRegressionClass.output['MSE'],
                            'RMSE': RidgeRegressionClass.output['RMSE'],
                            'predicted_output': RidgeRegressionClass.output['predicted_output'],
                            'actual_output': actual_output,
                        })
        
        return response
