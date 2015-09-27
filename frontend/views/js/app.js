
//activate navbar item on click
$(".nav a").on("click", function(){
    $(".nav").find(".active").removeClass("active");
    $(this).parent().addClass("active");
});

var ParkMe = angular.module('ParkMe',['ngRoute', 'ngResource','ui.bootstrap']);

ParkMe.config(['$routeProvider', '$locationProvider',
    function($routeProvider, $locationProvider){
        $routeProvider
            .when('/',{
                templateUrl: '../partials/realtime.html'
            })
            .when('/batch',{
                templateUrl: '../partials/batch.html'
            })
            .when('/stack',{
                templateUrl: '../partials/tech_stack.html'
            })
            .otherwise({
                redirectTo: '/'
            })
    }
]);
