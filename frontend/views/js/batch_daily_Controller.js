ParkMe.controller('batchDailyController', function($scope, $http, $rootScope, getParkingSpots){
    $scope.dayValue = "20150926";

    $scope.displayDailyStats = false;

    var initial_latitude = 37.7568400419;
    var initial_longitute = -122.4204335636;
    $scope.map = { center: { latitude: initial_latitude, longitude: initial_longitute}, zoom: 18 };

    $scope.marker = {
        id: 0,
        coords: {
            latitude: initial_latitude,
            longitude: initial_longitute
        },
        options:{
            icon:'../css/parking_marker.png'
        }
    };

    $rootScope.dailyMarkers = [];


    $scope.getDailyStats = function(){
        getParkingSpots.getDailyAggregate($scope.dayValue);
        $scope.displayDailyStats = true;
    };



});