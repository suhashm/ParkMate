
ParkMe.controller('signUpController', function($scope, $http, signUpService, userDetailsService){
    $scope.name = "welcome";
    $scope.signUP = function(){
        var uname = $scope.username;
        var pass = $scope.password;
        if(uname == undefined || uname == ""){
            toastr.error("Kindly Enter a valid Email");
            return;
        }
        if(pass == undefined || pass == ""){
            toastr.error("Kindly Enter Valid Password");
            return;
        }
        signUpService.signUpUser(uname, pass).then(function(userDetailsVal){

            userDetailsService.saveDetails(userDetailsVal.api_token, userDetailsVal.email, userDetailsVal.id, userDetailsVal.todos);
            var userDetailsVal1 = userDetailsService.getUserDetails();
            //console.log("Sign After up successful: API token "+userDetailsVal1.api_token+" email "+userDetailsVal1.email+" id "+userDetailsVal1.id+" todos "+userDetailsVal1.todos);
        });

    }
});

ParkMe.controller('loginController', function($scope, $rootScope, $http, loginService, userDetailsService, toDoService){
    $scope.loginUser = function(){

        var uname = $scope.usernameL;
        var pass = $scope.passwordL;
        if(uname == undefined || uname == ""){
            toastr.error("Kindly Enter a valid Email");
            return;
        }
        if(pass == undefined || pass == ""){
            toastr.error("Kindly Enter Valid Password");
            return;
        }
        userDetailsService.saveUserTodos("");
        loginService.loginUser(uname, pass).then(function(userDetailsVal){
           // console.log("Login success "+ userDetailsVal);
            userDetailsService.saveDetails(userDetailsVal.api_token, userDetailsVal.email, userDetailsVal.id, userDetailsVal.todos);
            //console.log("Sign up successful: API token "+userDetailsVal.api_token+" email "+userDetailsVal.email+" id "+userDetailsVal.id+" todos "+userDetailsVal.todos);
            var userDetailsVal1 = userDetailsService.getUserDetails();
            if(userDetailsVal1.todos.length > 0){
                var todoList = toDoService.getToDos(userDetailsVal1.api_token, userDetailsVal1.id);
            }
           // console.log("Login After up successful: API token "+userDetailsVal1.api_token+" email "+userDetailsVal1.email+" id "+userDetailsVal1.id+" todos "+userDetailsVal1.todos);
        });
    }
});
ParkMe.controller('signOutController', function($scope, $http, logOutService, userDetailsService, $location){
    $scope.signOutUser = function(){
       $location.path('/')
        toastr.success("Successfully logged out");

    }
});


ParkMe.controller('ToDoController', function($scope, $http, logOutService, userDetailsService, $q, toDoService){

    $scope.todoValues="";

    $scope.updateTodo = function(id, desc, status){
        var ss = $scope.done;
//      console.log("checkbox clicked "+id+" desc is "+desc+" status is "+status);
        var userDetailsVal1 = userDetailsService.getUserDetails();
        toDoService.updateToDos(userDetailsVal1.id, id, userDetailsVal1.api_token, desc, status);
    };

    $scope.getToDo = function(){
         $scope.todoValues = userDetailsService.getUserTodos();
        setTimeout(function(){
            $('.to-true').prop('checked', true);
        }, 100);
    };

    $scope.createToDo = function(todoDesc1){

        var userDetails = userDetailsService.getUserDetails();
        console.log("create todo  clicked, api key is "+userDetails.api_token+" user id "+userDetails.id);
        var desc = todoDesc1;
        var dfd = $q.defer();
        $http.post('http://recruiting-api.nextcapital.com/users/'+userDetails.id+'/todos', {"api_token":userDetails.api_token, "todo": {"description": desc}}).then(function (response) {
            if(response.status == 200){
                toastr.success("Successfully created To Do");
                $("#todoDescription").val(" ");
                toDoService.getToDos(userDetails.api_token, userDetails.id);
                dfd.resolve(response.data);
            }else{
                toastr.error("Unable to create ToDo now, please try again after sometime");
                console.log("failure create to do in inside services");
            }
        });
    }
});

