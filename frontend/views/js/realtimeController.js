ParkMe.controller('realtimeController', function($scope, $http){

    $scope.map = { center: { latitude: 37.788853, longitude: -122.400570 }, zoom: 14 };

    $scope.marker = {
        id: 0,
        coords: {
            latitude: 37.788853,
            longitude: -122.400570
        }
    };

    $scope.randomMarkers = [];
    var d = {
        'id': 0,
        'latitude': 37.688853,
        'longitude': -122.300570,
        'title': '<ul><li>first</li><li>second</li></ul>'

    };
    var e = {
        'id': 1,
        'latitude': 38.688853,
        'longitude': -121.300570,
        'title': '<ul><li>first</li><li>second</li></ul>'
    };

    $scope.randomMarkers.push(d);
    $scope.randomMarkers.push(e);

    $scope.circles = [
        {
            id: 1,
            center: {
                latitude: 37.788853,
                longitude: -122.400570
            },
            radius: 500,
            stroke: {
                color: '#08B21F',
                weight: 2,
                opacity: 1
            },
            fill: {
                color: '#08B21F',
                opacity: 0.5
            },
            geodesic: true, // optional: defaults to false
            draggable: true, // optional: defaults to false
            clickable: true, // optional: defaults to true
            editable: true, // optional: defaults to false
            visible: true, // optional: defaults to true
            control: {},
            events: {
                dragend: function (marker, eventName, args) {
                    var lat = marker.getCenter().lat();
                    var lon = marker.getCenter().lng();
                    console.log(lat+", "+lon);
                }
            }
        }
    ];

});