
//activate navbar item on click
$(".nav a").on("click", function(){
    $(".nav").find(".active").removeClass("active");
    $(this).parent().addClass("active");
});

var ParkMe = angular.module('ParkMe',['ngRoute', 'ngResource', 'uiGmapgoogle-maps']);

ParkMe.config(['$routeProvider', '$locationProvider',
    function($routeProvider, $locationProvider){
        $routeProvider
            .when('/',{
                templateUrl: '../partials/realtime.html'
            })
            .when('/batch-hourly',{
                templateUrl: '../partials/batch_hourly.html'
            })
            .when('/batch-daily',{
                templateUrl: '../partials/batch_daily.html'
            })
            .when('/stack',{
                templateUrl: '../partials/tech_stack.html'
            })
            .otherwise({
                redirectTo: '/'
            })
    }
]);
