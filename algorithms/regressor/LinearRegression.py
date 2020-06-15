
import numpy as np
import json, joblib
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, RandomizedSearchCV
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report, mean_absolute_error, mean_squared_error

from sklearn.linear_model import LinearRegression

class LinearRegressionClass:
    
    output = {}

    def build(self, project_tag, X, Y, train_x, test_x, train_y, test_y, cv=5, scoring=None):
        
        cv = int(cv)
        
        model = LinearRegression()
        model.fit(train_x,train_y)

        filename = 'algorithms/all_fitted_models/'+ project_tag +'/linear_regression.sav'
        joblib.dump(model, filename)

        cv_r2 = cross_val_score(model, X, Y, scoring=scoring, cv=cv) 
        LinearRegressionClass.output['mean_cv_r2'] = cv_r2.mean()
        
        pred_y = model.predict(test_x)
        LinearRegressionClass.output['predicted_output'] = pred_y.tolist()
        
        mean_absolute_err = mean_absolute_error(test_y, pred_y)
        LinearRegressionClass.output['MAE'] = mean_absolute_err
        
        mean_squared_err = mean_squared_error(test_y, pred_y)
        LinearRegressionClass.output['MSE'] = mean_squared_err
        
        root_mean_squared_err = np.sqrt(mean_squared_err)
        LinearRegressionClass.output['RMSE'] = root_mean_squared_err
                
        LinearRegressionClass.output['train_r2'] = model.score(train_x, train_y)
        LinearRegressionClass.output['test_r2'] = model.score(test_x, test_y)

        actual_output = list(test_y)

        response = json.dumps({
                            'mean_cv_r2': LinearRegressionClass.output['mean_cv_r2'],
                            'MAE': LinearRegressionClass.output['MAE'],
                            'MSE': LinearRegressionClass.output['MSE'],
                            'RMSE': LinearRegressionClass.output['RMSE'],
                            'R_Sq_train': LinearRegressionClass.output['train_r2'],
                            'R_Sq_test': LinearRegressionClass.output['test_r2'],
                            'predicted_output': LinearRegressionClass.output['predicted_output'],
                            'actual_output': actual_output,
                        })
        
        return response


        