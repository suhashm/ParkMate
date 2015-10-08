ParkMe.controller('realtimeController', function($scope, $rootScope, $http, getParkingSpots){
    var initial_latitude = 37.78975175827529;
    var initial_longitute = -122.39758738329999;
    $scope.map = { center: { latitude: initial_latitude, longitude: initial_longitute}, zoom: 16 };

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

    $rootScope.randomMarkers = [];
    getParkingSpots.availableSpots(initial_latitude, initial_longitute);
    $scope.circles = [
        {
            id: 1,
            center: {
                latitude: initial_latitude,
                longitude: initial_longitute
            },
            radius: 450,
            stroke: {
                color: '#08B21F',
                weight: 2,
                opacity: 1
            },
            fill: {
                color: '#08B21F',
                opacity: 0.5
            },
            geodesic: true,
            draggable: true,
            clickable: true,
            editable: true,
            visible: true,
            control: {},
            events: {
                dragend: function (marker, eventName, args) {
                    $rootScope.randomMarkers = [];
                    var lat = marker.getCenter().lat();
                    var lon = marker.getCenter().lng();
                    console.log(lat+", "+lon);
                    getParkingSpots.availableSpots(lat, lon);
                }
            }
        }
    ];

});