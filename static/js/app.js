var app = angular.module('AIworks', ['ngDialog', 'ngSanitize', 'ui.select']);

app.config(function ($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
});

app.controller('AppController', ['$scope', '$http', 'ngDialog', function ($scope, $http, ngDialog) {

    $scope.base_url = 'http://'+ window.location.hostname +':5000';
    $scope.processing = false;
    var aap_con = this;

    $scope.round_int = function(int, len){

        var value = int.toFixed(len);

        return value;
    }

    $scope.fetchAPIData = function(API, Data){
  
        var url = $scope.base_url + API;
        
        var requestData = new FormData();

        angular.forEach(Data, function (value, key) {
                        
            requestData.append(key, value);
        });

        var request = new XMLHttpRequest();
        request.open('POST', url, false);  // `false` makes the request synchronous
        request.send(requestData);
        
        if (request.status === 200) {

            return JSON.parse(request.response);
        }else{

            return {'error': true};
        }

    }

    $scope.openPopup = function(API, Data){
  
        var template = $scope.base_url + API;

        $scope.popupData = Data;

        ngDialog.open({

            template: template,
            className: 'ngdialog-theme-default',
            scope: $scope,
        });
    }

    $scope.postForm = function(API, Data){

        $scope.processing = true;

        var url = $scope.base_url + API;
        
        var requestData = new FormData();

        angular.forEach(Data, function (value, key) {
                        
            requestData.append(key, value);
        });

        
        $http({
            method : "POST",
            url : url,
            headers: {
                        'Content-Type': undefined,
                    },
            data: requestData,
        }).then(

            function (response) {
                
                aap_con.handleFormResponse(response.data);
                $scope.processing = false;
            }, 

            function (error) {

                aap_con.handleFormResponse(error.data);
                $scope.processing = false;
            }
        );
    }

    aap_con.handleFormResponse = function(data){
    
        if(data.reload != undefined){

            location.reload();
        }

        if(data.redirect != undefined){

            var url = $scope.base_url + data.redirect;

            window.location = url;
        }
    }

}]);

app.filter('to_trusted', ['$sce', function($sce){
    return function(text) {
        return $sce.trustAsHtml(text);
    };
}]);

app.directive("ngFiles",  ['$parse', function ($parse) {

    function fn_link(scope, element, attrs) {
        var onChange = $parse(attrs.ngFiles);
        element.on('change', function (event) {
            onChange(scope, { $files: event.target.files });
        });
    };

    return {
        link: fn_link
    }
} ]);
