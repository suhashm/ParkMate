ParkMe.controller('batchHourlyController', function($scope, $http, getParkingSpots){
    $scope.dayValue = "20150926";
    $scope.getHourlyStats = function(){
//        alert($scope.dayValue+"-"+$scope.spotName.replace(/ /g, '_'));
        getParkingSpots.getHourlyAggregate($scope.dayValue, $scope.spotName.replace(/ /g, '_'));
    };

    // get all the spot names from the DB
    $http.get('http://localhost:5000/get_spot_names/').success(function(data){
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