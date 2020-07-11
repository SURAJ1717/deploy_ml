
app.service('formService', ['$http', '$rootScope', 

    function ($http, $rootScope) {

        var fs = this;

        fs.base_url = 'http://'+ window.location.hostname +':5000';

        fs.processing = false;

        fs.prediction_result = {};

        fs.output_model_Data = {};

        fs.integrate_model_output = {};

        fs.proccessed_Data = {};

        //Default data for each input
        fs.default_formData = {};
        fs.default_formData.cv = 10;
        fs.default_formData.scoring = 'neg_mean_squared_error';
        fs.default_formData.search_type = "grid";
        fs.default_formData.n_iter = 100;
        fs.default_formData.random_state = 0;
        fs.default_formData.correlation = false;
        fs.default_formData.skip_first = false;
        fs.default_formData.top_imp_features = null;

        fs.default_checked_algos = ["linear_regressor", "ridge_regressor", "lasso_regressor", "dt_regressor", "rf_regressor", "xgb_regressor"];

        fs.default_ridge_params = {              
            alpha: [1e-15,1e-10,1e-8,1e-4,1e-2,1,2,4,8,10,20,30,40,50,60]
        };

        fs.default_lasso_params = {              
            alpha: [1e-15,1e-10,1e-8,1e-4,1e-2,1,2,4,8,10,20,25,30,35,40,50,60]
        };

        fs.default_dt_params = {              
            splitter: ['best','random'],
            max_depth: [3,5,7,9,11,13,15],
            min_samples_leaf: [1,2,3,4,5],
            min_weight_fraction_leaf: [0.1,0.2,0.3,0.4],
            max_features: ["auto", "log2", "sqrt", 'None'],
            max_leaf_nodes: [10, 20, 30, 40, 50, 60],
        };

        fs.default_rf_params={              
            n_estimators: [100,200,300,400,500,600,700,800,900,1000],
            min_samples_split: [2,5,10,15,100],
            max_features: ["auto", "sqrt"],
            max_depth: [6,12,18,24,30,36,42,48],
            min_samples_leaf: [1,2,5,10],
        };

        fs.default_xgb_params={              
            n_estimators: [100,200,300,400,500,600,700,800,900,1000],
            learning_rate: ["0.05", "0.1", "0.2", "0.3", "0.5", "0.6"],
            min_child_weight: [3,4,5,6,7],
            max_depth: [6,12,18,24,30,36,42,48],
            subsample: [0.7,0.6,0.8],
        };


        //intialize form model-inputs
        fs.formData = {};
        fs.csvFiles = null;
        fs.checked_algos = [];
        fs.checked_algos_form = [];

        fs.linear_tab = false;
        fs.ridge_tab = false;
        fs.lasso_tab = false;
        fs.dt_tab = false;
        fs.rf_tab = false;
        fs.xgb_tab = false;

        fs.ridge_params = {              
                            alpha: []
                        };

        fs.lasso_params = {              
                            alpha: []
                        };

        fs.dt_params = {              
                        splitter: [],
                        max_depth: [],
                        min_samples_leaf: [],
                        min_weight_fraction_leaf: [],
                        max_features: [],
                        max_leaf_nodes: [],
                    };

        fs.rf_params={              
                        n_estimators: [],
                        min_samples_split: [],
                        max_features: [],
                        max_depth: [],
                        min_samples_leaf: [],
                    };

        fs.xgb_params={              
                        n_estimators: [],
                        learning_rate: [],
                        min_child_weight: [],
                        max_depth: [],
                        subsample: [],
                    };


        fs.selected_algo = function(){
            
            angular.forEach(fs.formData.algorithms, function (value, key) { 

                if(value){

                    fs.checked_algos.push(key); 

                    fs.checked_algos_form.push(key); 
                }
            });

            if(fs.formData.algorithms == undefined){

                fs.checked_algos = fs.checked_algos_form = fs.default_checked_algos;
            }
        }

        fs.reset_algos = function(){

            fs.checked_algos=[]; 
            fs.checked_algos_form=[];

            fs.linear_tab = fs.ridge_tab = fs.lasso_tab = fs.dt_tab = fs.rf_tab = fs.xgb_tab = false;
        }

        // v2
        fs.openTab = function(algorithm){

            fs.formData.algorithms.map(element => element.current_tab=false);

            var this_algo = fs.formData.algorithms.find(element => element._id == algorithm._id);

            this_algo.current_tab = true;
        }

        // get the CSV files
        fs.getTheFiles = function ($files) {

            fs.csvFiles = null;

            angular.forEach($files, function (value, key) {

                if(key == 0){
                    
                    fs.csvFiles = value;
                }
            });
        };


        //Prepare formdata for build model
        fs.prepareFormdata = function(){

            fs.proccessed_Data.formData = fs.formData;
            fs.proccessed_Data.formData.csvFiles = fs.csvFiles;
            fs.proccessed_Data.formData.checked_algos = fs.checked_algos;
            fs.proccessed_Data.formData.ridge_params = fs.ridge_params;
            fs.proccessed_Data.formData.lasso_params = fs.lasso_params;
            fs.proccessed_Data.formData.dt_params = fs.dt_params;
            fs.proccessed_Data.formData.rf_params = fs.rf_params;
            fs.proccessed_Data.formData.xgb_params = fs.xgb_params;

            if(fs.proccessed_Data.formData.checked_algos.length == 0){

                fs.proccessed_Data.formData.checked_algos = fs.default_checked_algos;
            }

            if(fs.proccessed_Data.formData.cv == undefined || fs.proccessed_Data.formData.cv == ''){

                fs.proccessed_Data.formData.cv = fs.default_formData.cv;
            }

            if(fs.proccessed_Data.formData.scoring == undefined || fs.proccessed_Data.formData.scoring == ''){

                fs.proccessed_Data.formData.scoring = fs.default_formData.scoring;
            }

            if(fs.proccessed_Data.formData.search_type == undefined || fs.proccessed_Data.formData.search_type == ''){

                fs.proccessed_Data.formData.search_type = fs.default_formData.search_type;
            }

            if(fs.proccessed_Data.formData.n_iter == undefined || fs.proccessed_Data.formData.n_iter == ''){

                fs.proccessed_Data.formData.n_iter = fs.default_formData.n_iter;
            }

            if(fs.proccessed_Data.formData.random_state == undefined || fs.proccessed_Data.formData.random_state == ''){

                fs.proccessed_Data.formData.random_state = fs.default_formData.random_state;
            }

            if(fs.proccessed_Data.formData.correlation == undefined || fs.proccessed_Data.formData.correlation == ''){

                fs.proccessed_Data.formData.correlation = fs.default_formData.correlation;
            }

            if(fs.proccessed_Data.formData.skip_first == undefined || fs.proccessed_Data.formData.skip_first == ''){

                fs.proccessed_Data.formData.skip_first = fs.default_formData.skip_first;
            }

            if(fs.proccessed_Data.formData.top_imp_features == undefined || fs.proccessed_Data.formData.top_imp_features == ''){

                fs.proccessed_Data.formData.top_imp_features = fs.default_formData.top_imp_features;
            }

            //process ridge hyper param
            fs.process_ridge_params();

            //process lasso hyper param
            fs.process_lasso_params();

            //process Decision tree hyper param
            fs.process_dt_params();

            //process Random forest hyper param
            fs.process_rf_params();
            
            //process Xgboost hyper param
            fs.process_xgb_params();

            
            var postData = new FormData();
            
            angular.forEach(fs.proccessed_Data.formData, function (value, key) {

                if( key == 'algorithms' || key == 'ridge_params' || key =='lasso_params' || key =='dt_params' || key =='rf_params' || key =='xgb_params'){
                    postData.append(key, JSON.stringify(value));
                }else{  
                    postData.append(key, value);
                }
            });

            return  postData;
        }

        fs.process_ridge_params = function(){
        
            if(fs.proccessed_Data.formData.ridge_params.alpha.length == 0){

                fs.proccessed_Data.formData.ridge_params.alpha = fs.default_ridge_params.alpha;
            }
        }

        fs.process_lasso_params = function(){
        
            if(fs.proccessed_Data.formData.lasso_params.alpha.length == 0){

                fs.proccessed_Data.formData.lasso_params.alpha = fs.default_lasso_params.alpha;
            }
        }

        fs.process_dt_params = function(){

            if(fs.proccessed_Data.formData.dt_params.splitter.length == 0){

                fs.proccessed_Data.formData.dt_params.splitter = fs.default_dt_params.splitter;
            }

            if(fs.proccessed_Data.formData.dt_params.max_depth.length == 0){

                fs.proccessed_Data.formData.dt_params.max_depth = fs.default_dt_params.max_depth;
            }

            if(fs.proccessed_Data.formData.dt_params.min_samples_leaf.length == 0){

                fs.proccessed_Data.formData.dt_params.min_samples_leaf = fs.default_dt_params.min_samples_leaf;
            }

            if(fs.proccessed_Data.formData.dt_params.min_weight_fraction_leaf.length == 0){

                fs.proccessed_Data.formData.dt_params.min_weight_fraction_leaf = fs.default_dt_params.min_weight_fraction_leaf;
            }

            if(fs.proccessed_Data.formData.dt_params.max_features.length == 0){

                fs.proccessed_Data.formData.dt_params.max_features = fs.default_dt_params.max_features;
            }

            if(fs.proccessed_Data.formData.dt_params.max_leaf_nodes.length == 0){

                fs.proccessed_Data.formData.dt_params.max_leaf_nodes = fs.default_dt_params.max_leaf_nodes;
            }
        }

        fs.process_rf_params = function(){

            if(fs.proccessed_Data.formData.rf_params.n_estimators.length == 0){

                fs.proccessed_Data.formData.rf_params.n_estimators = fs.default_rf_params.n_estimators;
            }

            if(fs.proccessed_Data.formData.rf_params.min_samples_split.length == 0){

                fs.proccessed_Data.formData.rf_params.min_samples_split = fs.default_rf_params.min_samples_split;
            }

            if(fs.proccessed_Data.formData.rf_params.max_features.length == 0){

                fs.proccessed_Data.formData.rf_params.max_features = fs.default_rf_params.max_features;
            }

            if(fs.proccessed_Data.formData.rf_params.max_depth.length == 0){

                fs.proccessed_Data.formData.rf_params.max_depth = fs.default_rf_params.max_depth;
            }

            if(fs.proccessed_Data.formData.rf_params.min_samples_leaf.length == 0){

                fs.proccessed_Data.formData.rf_params.min_samples_leaf = fs.default_rf_params.min_samples_leaf;
            }
        }

        fs.process_xgb_params = function(){

            if(fs.proccessed_Data.formData.xgb_params.n_estimators.length == 0){

                fs.proccessed_Data.formData.xgb_params.n_estimators = fs.default_xgb_params.n_estimators;
            }

            if(fs.proccessed_Data.formData.xgb_params.learning_rate.length == 0){

                fs.proccessed_Data.formData.xgb_params.learning_rate = fs.default_xgb_params.learning_rate;
            }

            if(fs.proccessed_Data.formData.xgb_params.min_child_weight.length == 0){

                fs.proccessed_Data.formData.xgb_params.min_child_weight = fs.default_xgb_params.min_child_weight;
            }

            if(fs.proccessed_Data.formData.xgb_params.max_depth.length == 0){

                fs.proccessed_Data.formData.xgb_params.max_depth = fs.default_xgb_params.max_depth;
            }

            if(fs.proccessed_Data.formData.xgb_params.subsample.length == 0){

                fs.proccessed_Data.formData.xgb_params.subsample = fs.default_xgb_params.subsample;
            }

        }


        // model integration and removal methods
        fs.integrate_model = function(url, project_tag, algorithm_name){

            fs.processing = true;

            var API = fs.base_url + url;

            var postData = new FormData();

            var features = fs.getfeatures(algorithm_name);

            postData.append('project', project_tag);
            postData.append('model_name', algorithm_name);
            postData.append('features', features);

            $http({
                method : "POST",
                url : API,
                headers: {
                            'Content-Type': undefined,
                        },
                data: postData,
            }).then(

                function (response) {
                    
                    if(response.status == 200){

                        fs.integrate_model_output.success = true;
                    }

                    fs.processing = false;
                }, 

                function (error) {

                    fs.integrate_model_output.error = error;

                    fs.processing = false;
                }
            );
        }

        fs.clear_integrated_model = function(url, project_tag){

            fs.processing = true;

            var API = fs.base_url + url;

            var postData = new FormData();

            postData.append('project', project_tag);

            $http({
                method : "POST",
                url : API,
                headers: {
                            'Content-Type': undefined,
                        },
                data: postData,
            }).then(

                function (response) {

                    fs.processing = false;

                    if(response.status == 200){

                        location.reload();
                    }
                }, 

                function (error) {

                    fs.processing = false;
                }
            );
        }

        fs.getfeatures = function(algorithm_name){

            var this_features = null;

            if(algorithm_name == 'linear_regression'){

                this_features = fs.output_model_Data.linear_regression.independent_col;
            }

            if(algorithm_name == 'ridge_regression'){

                this_features = fs.output_model_Data.ridge_regression.independent_col;
            }

            if(algorithm_name == 'lasso_regression'){

                this_features = fs.output_model_Data.lasso_regression.independent_col;
            }

            if(algorithm_name == 'dt_regression'){

                this_features = fs.output_model_Data.dt_regression.independent_col;
            }

            if(algorithm_name == 'rf_regression'){

                this_features = fs.output_model_Data.rf_regression.independent_col;
            }

            if(algorithm_name == 'xgb_regression'){

                this_features = fs.output_model_Data.xgb_regression.independent_col;
            }

            return this_features;
        }

        fs.predictResult = function(url, inputData){

            fs.processing = true;

            var API = fs.base_url + url;

            var postData = new FormData();

            angular.forEach(inputData, function(value, key) {

                postData.append(key, value);
            });

            $http({
                method : "POST",
                url : API,
                headers: {
                            'Content-Type': undefined,
                        },
                data: postData,
            }).then(

                function (response) {
                    
                    if(response.status == 200){

                        fs.prediction_result.output = response.data;

                        fs.processing = false;
                    }
                }, 

                function (error) {

                    fs.prediction_result.error = error;

                    fs.processing = false;
                }
            );
        }

    }
]);