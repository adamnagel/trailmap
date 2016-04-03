'use strict';

/* Controllers */

var trailmapApp = angular.module('trailmapApp', ['ui.bootstrap']);

trailmapApp.controller('TrailmapCtrl', ['$scope', '$http', function ($scope, $http) {
    $scope.trailsystems = {};

    $http.get('api/list_trailsystems').success(function (data) {
        var trailsystems = data['trailsystems']

        angular.forEach(trailsystems, function (trailsystem) {
            $scope.trailsystems[trailsystem] = {};
        });

        angular.forEach(trailsystems, function (trailsystem) {
            $http.get('api/traildata/' + trailsystem).success(function (traildata) {
                $scope.trailsystems[trailsystem] = traildata;
            });
        });
    });
}]);