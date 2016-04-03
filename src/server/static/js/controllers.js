'use strict';

/* Controllers */

var trailmapApp = angular.module('trailmapApp', ['ui.bootstrap']);

trailmapApp.controller('TrailmapCtrl', ['$scope', '$http', '$q', '$timeout',
    function ($scope, $http, $q, $timeout) {
        $scope.trailsystems = {};

        $http.get('api/list_trailsystems').success(function (data) {
            var trailsystems = data['trailsystems']

            // Get list of trails
            angular.forEach(trailsystems, function (trailsystem) {
                $scope.trailsystems[trailsystem] = {};
            });

            // Fetch trail data
            angular.forEach(trailsystems, function (trailsystem) {
                $http.get('api/traildata/' + trailsystem).success(function (traildata) {
                    $scope.trailsystems[trailsystem] = traildata;
                });
            });
        });

        $timeout(function () {
            // Build visualizations

            var name_div = '#diag';
            console.log(name_div);

            var diagram_data = [
                {
                    group: 'nodes',
                    data: {
                        name: 'thing1',
                        id: 0
                    }
                },
                {
                    group: 'nodes',
                    data: {
                        name: 'thing2',
                        id: 1
                    }
                }
            ];
            var cy = cytoscape({
                container: $('#diag')[0],
                style: cytoscape.stylesheet()
                    .selector('node')
                    .css({
                        'content': 'data(name)',
                        'height': 80,
                        'width': 20,
                        'text-valign': 'center',
                        'color': 'white',
                        'text-outline-width': 2,
                        'text-outline-color': '#888'
                    })
                    .selector('edge')
                    .css({
                        'target-arrow-shape': 'triangle'
                    })
                    .selector(':selected')
                    .css({
                        'background-color': 'black',
                        'line-color': 'black',
                        'target-arrow-color': 'black',
                        'source-arrow-color': 'black',
                        'text-outline-color': 'black'
                    }),
                layout: {
                    name: 'cose',
                    padding: 10
                },
                elements: diagram_data,
                ready: function () {
                    $q.defer().resolve(this);
                }
            });
        }, 2000);
    }]);