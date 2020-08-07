
app.service('formService', ['$http', '$rootScope', 

    function ($http, $rootScope) {

        var fs = this;

        fs.base_url = 'http://'+ window.location.hostname +':5000';

        fs.processing = false;

        fs.prediction_result = {};

        fs.output_model_Data = {};

        fs.integrate_model_output = {};

        fs.proccessed_Data = {};

        fs.all_features = [];

        fs.encoding_types = ["mean_encoding", "target_guided_encoding", "count_freqency_encoding"];

        //Default data for each input
        fs.default_formData = {};
        fs.default_formData.cv = 10;
        fs.default_formData.scoring = 'neg_mean_squared_error';
        fs.default_formData.search_type = "grid";
        fs.default_formData.n_iter = 10;
        fs.default_formData.random_state = 0;
        fs.default_formData.correlation = false;
        fs.default_formData.skip_first = false;
        fs.default_formData.top_imp_features = null;

        // fs.default_checked_algos = ["linear_regressor", "ridge_regressor", "lasso_regressor", "dt_regressor", "rf_regressor", "xgb_regressor"];

        // fs.default_ridge_params = {              
        //     alpha: [1e-15,1e-10,1e-8,1e-4,1e-2,1,2,4,8,10,20,30,40,50,60]
        // };

        // fs.default_lasso_params = {              
        //     alpha: [1e-15,1e-10,1e-8,1e-4,1e-2,1,2,4,8,10,20,25,30,35,40,50,60]
        // };

        // fs.default_dt_params = {              
        //     splitter: ['best','random'],
        //     max_depth: [3,5,7,9,11,13,15],
        //     min_samples_leaf: [1,2,3,4,5],
        //     min_weight_fraction_leaf: [0.1,0.2,0.3,0.4],
        //     max_features: ["auto", "log2", "sqrt", 'None'],
        //     max_leaf_nodes: [10, 20, 30, 40, 50, 60],
        // };

        // fs.default_rf_params={              
        //     n_estimators: [100,200,300,400,500,600,700,800,900,1000],
        //     min_samples_split: [2,5,10,15,100],
        //     max_features: ["auto", "sqrt"],
        //     max_depth: [6,12,18,24,30,36,42,48],
        //     min_samples_leaf: [1,2,5,10],
        // };

        // fs.default_xgb_params={              
        //     n_estimators: [100,200,300,400,500,600,700,800,900,1000],
        //     learning_rate: ["0.05", "0.1", "0.2", "0.3", "0.5", "0.6"],
        //     min_child_weight: [3,4,5,6,7],
        //     max_depth: [6,12,18,24,30,36,42,48],
        //     subsample: [0.7,0.6,0.8],
        // };


        //intialize form model-inputs
        fs.formData = {};

        // v2
        fs.openTab = function(algorithm){

            fs.formData.algorithms.map(element => element.current_tab=false);

            var this_algo = fs.formData.algorithms.find(element => element._id == algorithm._id);

            this_algo.current_tab = true;
        }

        // get the CSV files
        fs.getTheFiles = function ($files) {

            fs.formData.csvFiles = null;

            angular.forEach($files, function (value, key) {

                if(key == 0){
                    
                    fs.formData.csvFiles = value;
                }
            });
        };

        // model integration and removal methods
        fs.integrate_model = function(url, project_tag, algorithm){

            fs.processing = true;

            var API = fs.base_url + url;

            var postData = new FormData();

            var features = JSON.stringify(algorithm.success.independent_col);
            
            postData.append('project_tag', project_tag);
            postData.append('model_name', algorithm.name);
            postData.append('model_slug', algorithm.slug);
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

            postData.append('project_tag', project_tag);

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

        fs.getAllFeatures = function(url, hasCategorical){

            if(fs.formData.csvFiles == null){

                alert('Please upload Csv');
            }

            var features = [];

            var API = fs.base_url + url;

            if(hasCategorical && fs.formData.csvFiles != null){

                var postData = new FormData();

                postData.append('csvFiles', fs.formData.csvFiles);
            
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

                            fs.all_features = response.data.columns;
                        }
                    }, 

                    function (error) {

                        alert(error.data);
                    }
                );                
            }
        }

















    }
]);