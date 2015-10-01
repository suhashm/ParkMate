
ParkMe.factory('getParkingSpots', function($http,$rootScope){
    return{
        availableSpots: function(lat, lon){
            var numSpots = 20;
//            $http.get('http://127.0.0.1:5000/get_nearest_spot/'+numSpots+'/'+lat+'/'+lon+'/').success(function(data){
            $http.get('https://parakana.herokuapp.com/get_nearest_spot/'+numSpots+'/'+lat+'/'+lon+'/').success(function(data){
                var spots = [];
                for(var i =0; i < data.length; i++){
                    if(data[i]._source.availability != 0) {
                        var d = {};
                        d['id'] = data[i]._id;
                        d['latitude'] = data[i]._source.location.lat;
                        d['longitude'] = data[i]._source.location.lon;
                        var name = data[i]._id.replace(/_/g, ' ');
                        var availability = data[i]._source.availability;
                        d['title'] = '<div><p>' + name + '</p><p><b>Availability: </b>' + availability + '</p></div>';
                        spots.push(d);
                    }

                }
                $rootScope.randomMarkers = spots;
            }).error(function(data){
                toastr.error("Unable to get the nearest parking, please try again after sometime");
            });
        },
        getDailyAggregate: function(date){
            console.log("date is "+date);
            $http.get('http://localhost:5000/get_availability_daily/'+date).success(function(data){
                console.log(data);
                console.log("length is "+data.result.length);
                var spots = [];
                for(var i =0; i < data.result.length; i++){
                        var d = {};
                        d['id'] = i;
                        d['latitude'] = data.result[i].lat;
                        d['longitude'] = data.result[i].lon;
                        var name = data.result[i].spot_name.replace(/_/g, ' ');
                        var availability = data.result[i].Availability;
                        d['title'] = '<div><p>' + name + '</p><p><b>Average Availability: </b>' + availability + '</p></div>';
                        spots.push(d);


                }
                $rootScope.dailyMarkers = spots;

            }).error(function(){
                toastr.error("Unable to get the spot names, please try again later");
            });
        },
        getHourlyAggregate: function(date, spot_name){
            console.log("date is "+date+" spot name is "+spot_name);
            $http.get('http://localhost:5000/get_availability_hourly/'+date+'/'+spot_name).success(function(data){
                var spots = [];
                console.log(data);
                console.log("length is "+data.result.length);

            }).error(function(){
                toastr.error("Unable to get the spot names, please try again later");
            });
        }
    }
});


