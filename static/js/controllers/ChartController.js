
app.controller('ChartController', ['$scope', '$http', 'ngDialog', 'formService',

function ($scope, $http, ngDialog, formService) {

    var vm = this;

    vm.id = 'aqi_actual_vs_pred_line';

    vm.formservice = formService;

    vm.getLineChart = function(algorithm){
        
        var actual_val = algorithm.success.output.actual_output.map(element => parseFloat(element.toFixed(1)) );
        
        var predicted_val = algorithm.success.output.predicted_output.map(element => parseFloat(element.toFixed(1)) );

        var difference = actual_val.map(function(item, index) { return item - predicted_val[index]; });

        var diff_round = difference.map(element => element.toFixed(1) );

        console.log(actual_val, predicted_val, diff_round);

        Highcharts.chart( algorithm.slug , {

            chart: {
                type: 'line',
                zoomType: 'x'
            },
            title: {
                text: 'Difference between Actual and Predicted Values'
            },
            // subtitle: {
            //     text: 'Source: WorldClimate.com'
            // },
            xAxis: {
                categories: diff_round,
                title: {
                    text: 'Actual vs Pediction difference'
                }
            },
            yAxis: {
                title: {
                    text: 'Actual vs Pediction range'
                }
            },
            plotOptions: {
                line: {
                    dataLabels: {
                        enabled: true
                    },
                    enableMouseTracking: false
                }
            },
            series: [{
                name: 'Predicted',
                data: predicted_val
            }, {
                name: 'Actual',
                data: actual_val
            }]
        });
    }


}
]);

