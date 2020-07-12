
app.controller('FormController', ['$scope', 'formService', '$http', 'ngDialog',

    function ($scope, formService, $http, ngDialog) {

        var vm = this;

        vm.postData = {};
        vm.formservice = formService;

        vm.buildModel = function (path, project_tag) {

            if(vm.formservice.formData.csvFiles == null){

                alert('Please upload Csv');
            }

            var API = $scope.base_url + path;

            vm.openProcessingPopup();
            
            if(vm.formservice.formData.search_type == 'grid'){

                vm.formservice.formData.n_iter = 100;
                vm.formservice.formData.random_state = 0;
            }

            vm.formservice.formData.project_tag = project_tag;

            var atleast_one_algo_selected = vm.formservice.formData.algorithms.find(element => element.added == true)

            if (atleast_one_algo_selected != undefined) {
                // filter out selected algorithms
                vm.formservice.formData.algorithms = vm.formservice.formData.algorithms.filter(element => element.added == true);
            }

            vm.organiseHyperParameter();

            vm.postData = new FormData();

            angular.forEach(vm.formservice.formData, function (value, key) {

                vm.postData.append(key, value);
            });

            vm.excecuteAlgorithm(API);
        };

        vm.organiseHyperParameter = function () {

            vm.formservice.formData.algorithms.forEach(function (item) {

                item.processed_hyper_parameters = {};

                item.is_request_sent = false;

                item.hyper_params.forEach(function (para_item) {

                    if (para_item.datatype == "number") {

                        if (para_item.params.length > 0) {

                            para_item.params = para_item.params.map(x => parseFloat(x));
                        }

                        if (para_item.custom_para != undefined && para_item.custom_para.length > 0) {

                            para_item.custom_para = para_item.custom_para.map(x => parseFloat(x));
                        }
                    }

                    if (para_item.custom_para != undefined && para_item.custom_para.length > 0) {

                        item.processed_hyper_parameters[para_item.slug] = para_item.custom_para;

                    } else {

                        item.processed_hyper_parameters[para_item.slug] = para_item.params;
                    }
                });
            });
        }

        vm.openProcessingPopup = function () {

            var template = $scope.base_url + '/projects/AQI/includes/result_popup.html';

            ngDialog.open({

                template: template,
                className: 'ngdialog-theme-plain',
                scope: $scope,
                width: '95%'
            });
        }

        vm.excecuteAlgorithm = function (API) {

            // get first algorithm
            var current_algo = vm.formservice.formData.algorithms.find(element => element.is_request_sent == false);

            if (current_algo != undefined) {
                
                current_algo.is_request_sent = true;

                if(vm.postData.has('hyper_parameters')){

                    vm.postData.delete('hyper_parameters');
                }

                vm.postData.append('hyper_parameters', JSON.stringify(current_algo.processed_hyper_parameters));

                if(vm.postData.has('algorithm_slug')){
                    
                    vm.postData.delete('algorithm_slug');
                }
                
                // FOR BINARY MODEL FILE NAME
                vm.postData.append('algorithm_slug', current_algo.slug);

                $http({
                    method: "POST",
                    url: API,
                    headers: {
                        'Content-Type': undefined,
                        'algorithm': current_algo.slug,
                    },
                    data: vm.postData,

                }).then(

                    function (response) {
                        //success
                        current_algo.success = response.data;

                        vm.excecuteAlgorithm(API);
                    },

                    function (error) {
                        //error
                        current_algo.error = error;
                    }
                );
            }
        };



    }
]);

