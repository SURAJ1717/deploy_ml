
app.controller('FormController', ['$scope','formService', '$http', 'ngDialog',

    function($scope, formService, $http, ngDialog){

        var vm = this;

        vm.formData = {};
        vm.formservice = formService;
        vm.checked_algos = null;

        vm.buildModel = function(path, project_tag){

            var API = $scope.base_url + path;

            vm.formData = vm.formservice.prepareFormdata();
            
            vm.formData.append('project_tag', project_tag);

            vm.checked_algos = vm.formData.get('checked_algos');
        
            vm.checked_algos = vm.checked_algos.split(",");

            if(vm.formData.get('csvFiles') == 'null'){

                alert('Please upload Csv');
            }else{

                vm.excecuteAlgorithm(API);

                vm.openProcessingPopup();
            }

        };

        vm.openProcessingPopup = function(){
  
            var template = $scope.base_url + '/projects/AQI/includes/result_popup.html';
    
            ngDialog.open({
    
                template: template,
                className: 'ngdialog-theme-plain',
                scope: $scope,
                width: '95%'
            });
        }

        vm.excecuteAlgorithm = function(API){

            if(vm.checked_algos.length > 0){

                var Algorithm = vm.checked_algos.pop();

            }else{

                var Algorithm = 'over';
            }

            if( Algorithm == 'linear_regressor'){

                vm.builtLinearRegression(API, Algorithm);
            }

            if( Algorithm == 'ridge_regressor'){

                vm.builtRidgeRegression(API, Algorithm);
            }

            if( Algorithm == 'lasso_regressor'){

                vm.builtLassoRegression(API, Algorithm);
            }

            if( Algorithm == 'dt_regressor'){

                vm.builtDTRegression(API, Algorithm);
            }

            if( Algorithm == 'rf_regressor'){

                vm.builtRFRegression(API, Algorithm);
            }

            if( Algorithm == 'xgb_regressor'){

                vm.builtXGBRegression(API, Algorithm);
            }
        };
        

        vm.builtLinearRegression = function(API, Algorithm){

            $http({
                method : "POST",
                url : API,
                headers: {
                            'Content-Type': undefined,
                            'algorithm': Algorithm,
                        },
                data: vm.formData,
            }).then(

                function (response) {
                    //success
                    vm.formservice.output_model_Data.linear_regression = response.data;

                    if(response.status == 200){

                        vm.excecuteAlgorithm(API);
                    }
                }, 

                function (error) {
                    //error
                    vm.formservice.output_model_Data.linear_regression_error = error;

                    vm.excecuteAlgorithm(API);
                }
            );
        };

        vm.builtRidgeRegression = function(API, Algorithm){

            $http({
                method : "POST",
                url : API,
                headers: {
                            'Content-Type': undefined,
                            'algorithm': Algorithm,
                        },
                data: vm.formData,
            }).then(

                function (response) {
                    //success
                    vm.formservice.output_model_Data.ridge_regression = response.data;

                    if(response.status == 200){

                        vm.excecuteAlgorithm(API);
                    }
                }, 

                function (error) {
                    //error
                    vm.formservice.output_model_Data.ridge_regression_error = error;

                    vm.excecuteAlgorithm(API);
                }
            );
        };

        vm.builtLassoRegression = function(API, Algorithm){

            $http({
                method : "POST",
                url : API,
                headers: {
                            'Content-Type': undefined,
                            'algorithm': Algorithm,
                        },
                data: vm.formData,
            }).then(

                function (response) {
                    //success
                    vm.formservice.output_model_Data.lasso_regression = response.data;

                    if(response.status == 200){

                        vm.excecuteAlgorithm(API);
                    }
                }, 

                function (error) {
                    //error
                   vm.formservice.output_model_Data.lasso_regression_error = error;

                   vm.excecuteAlgorithm(API);
                }
            );
        };

        vm.builtDTRegression = function(API, Algorithm){

            $http({
                method : "POST",
                url : API,
                headers: {
                            'Content-Type': undefined,
                            'algorithm': Algorithm,
                        },
                data: vm.formData,
            }).then(

                function (response) {
                    //success
                    vm.formservice.output_model_Data.dt_regression = response.data;
                    if(response.status == 200){

                        vm.excecuteAlgorithm(API);
                    }
                }, 

                function (error) {
                    //error
                    vm.formservice.output_model_Data.dt_regression_error = error;

                    vm.excecuteAlgorithm(API);
                }
            );
        };

        vm.builtRFRegression = function(API, Algorithm){

            $http({
                method : "POST",
                url : API,
                headers: {
                            'Content-Type': undefined,
                            'algorithm': Algorithm,
                        },
                data: vm.formData,
            }).then(

                function (response) {
                    //success
                    vm.formservice.output_model_Data.rf_regression = response.data;

                    if(response.status == 200){

                        vm.excecuteAlgorithm(API);
                    }
                }, 

                function (error) {
                    //error
                    vm.formservice.output_model_Data.rf_regression_error = error;

                    vm.excecuteAlgorithm(API);
                }
            );
        };

        vm.builtXGBRegression = function(API, Algorithm){

            $http({
                method : "POST",
                url : API,
                headers: {
                            'Content-Type': undefined,
                            'algorithm': Algorithm,
                        },
                data: vm.formData,
            }).then(

                function (response) {
                    //success
                    vm.formservice.output_model_Data.xgb_regression = response.data;

                    if(response.status == 200){

                        vm.excecuteAlgorithm(API);
                    }
                }, 

                function (error) {
                    //error
                    vm.formservice.output_model_Data.xgb_regression_error = error;

                    vm.excecuteAlgorithm(API);
                }
            );
        };

    }
]);

