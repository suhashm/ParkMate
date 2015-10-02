
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
//            $http.get('http://localhost:5000/get_availability_daily/'+date).success(function(data){
            $http.get('http://parakana.herokuapp.com/get_availability_daily/'+date).success(function(data){
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
//            $http.get('http://parakana.herokuapp.com/get_availability_hourly/'+date+'/'+spot_name).success(function(data){
                var spots = [];
                console.log(data);
                console.log("length is "+data.result.length);

                // get the required data for highcharts
                for(var i = 0; i < data.result.length; i++){
                    var inputs = [];
                    inputs.push(parseInt(data.result[i].timestamp+'000'));
                    inputs.push(parseInt(data.result[i].Availability));
                    spots.push(inputs);
                }
                console.log(spots);

                // bind it to highcharts

                $('#hourly_chart').highcharts({
                    chart: {
                        zoomType: 'x'
                    },
                    title: {
                        text: 'Availability of the spot over the day'
                    },
                    subtitle: {
                        text: document.ontouchstart === undefined ?
                            'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in'
                    },
                    xAxis: {
                        type: 'datetime'
                    },
                    yAxis: {
                        title: {
                            text: 'Availability trend'
                        }
                    },
                    legend: {
                        enabled: false
                    },
                    plotOptions: {
                        area: {
                            fillColor: {
                                linearGradient: {
                                    x1: 0,
                                    y1: 0,
                                    x2: 0,
                                    y2: 1
                                },
                                stops: [
                                    [0, Highcharts.getOptions().colors[0]],
                                    [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                                ]
                            },
                            marker: {
                                radius: 4
                            },
                            lineWidth: 1,
                            states: {
                                hover: {
                                    lineWidth: 1
                                }
                            },
                            threshold: null
                        }
                    },

                    series: [{
                        type: 'area',
                        name: 'Availability',
                        data: spots
                    }]
                });


            }).error(function(){
                toastr.error("Unable to get the spot names, please try again later");
            });
        }
    }
});


