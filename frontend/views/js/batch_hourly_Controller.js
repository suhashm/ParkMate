ParkMe.controller('batchHourlyController', function($scope, $http, getParkingSpots){
    $scope.dayValue = "20150927";
    $scope.getHourlyStats = function(){
        getParkingSpots.getHourlyAggregate($scope.dayValue, $scope.spotName.replace(/ /g, '_'));
    };

    // get all the spot names from the DB
    $http.get('http://parakana.herokuapp.com/get_spot_names/').success(function(data){
        var result = [];

        for(var i = 0; i < data.result.length; i++){
            result.push(data.result[i][0].replace(/_/g, ' '));
        }
        $scope.options_values = result;
        console.log("length is "+data.result.length);

    }).error(function(){
        toastr.error("Unable to get the spot names, please try again later");
    });





});