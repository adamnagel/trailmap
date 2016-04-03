'use strict';

/* Controllers */

var trailmapApp = angular.module('trailmapApp', ['ui.bootstrap']);

trailmapApp.controller('TrailmapCtrl', ['$scope', '$http', function ($scope, $http) {
    $scope.trailsystems = [];

    $http.get('api/list_trailsystems').success(function (data) {
        $scope.trailsystems = data['trailsystems'];
        });
}]);