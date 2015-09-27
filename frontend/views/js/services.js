
ParkMe.factory('signUpService', function($http, $q, userDetailsService, $location){
    return{
        signUpUser: function(username, password){
            var dfd = $q.defer();
            $http.post('http://recruiting-api.nextcapital.com/users', {email:username, password:password}).then(function (response) {
                //if(response.data.success){
                if(response.status == 200){
                    toastr.success("Successfully Signed UP");
                  dfd.resolve(response.data);
                    $location.path('/profile');
                }else{
                    toastr.error("Unable to Sign up now, please try again after sometime");
                    console.log("failure inside services");
                    dfd.resolve(false);
                }
            });
            return dfd.promise;
        }
    }
});

ParkMe.factory('loginService', function($http, $q, userDetailsService, $location){
    return{
        loginUser: function(username, password){
            var dfd = $q.defer();
            $http.post('http://recruiting-api.nextcapital.com/users/sign_in', {email:username, password:password}).then(function (response) {

                //if(response.data.success){
                if(response.status == 200){
                    toastr.success("Successfully Logged in");
                  dfd.resolve(response.data);
                    $location.path('/profile');
                }else{
                    toastr.error("Unable to Log in now, please try again after sometime");
                    console.log("failure log in inside services");
                    dfd.resolve(false);
                }
            });
            return dfd.promise;
        }
    }
});
ParkMe.factory('logOutService', function($http, $q, userDetailsService, $location){
    return{
        logOutUser: function(apiKey, id){
            var dfd = $q.defer();
            console.log("api key inside serv "+apiKey+" id "+id);
            $http.delete('http://recruiting-api.nextcapital.com/users/sign_out', {api_token:apiKey, user_id:id}).then(function (response) {
                //$http.delete('http://recruiting-api.nextcapital.com/users/'+id+'/sign_out').then(function (response) {
                if(response.status == 200){
                    toastr.success("Successfully Logged out");
                  dfd.resolve(response.data);
                    $location.path('/');
                }else{
                    toastr.error("Log out Error, please try again after sometime");
                    console.log("failure log out inside services");
                    dfd.resolve(false);
                }
            });
            return dfd.promise;
        }
    }
});

ParkMe.factory('toDoService', function($http, $q, userDetailsService){
    return{
        getToDos: function(apiKey, id){
            var dfd = $q.defer();
            //console.log("api key inside serv "+apiKey+" id "+id);
            $http.get('http://recruiting-api.nextcapital.com/users/'+id+'/todos.json?api_token='+apiKey).then(function (response) {

                //if(response.data.success){
                if(response.status == 200){
                    //toastr.success("Got list of todos");
                    dfd.resolve(response.data);
                    userDetailsService.saveUserTodos(response.data);
                    //$location.path('/');
                }else{
                    toastr.error("unable to get to dos");
                    console.log("failure get todo inside services");
                    dfd.resolve(false);
                }
            });
            return dfd.promise;
        },
        updateToDos: function(userId, toDoId, apiKey, desc, isComplete){
            //console.log("inside todo service "+userId+" todo id is "+toDoId+" desc is "+desc+" status is "+status);
            var dfd = $q.defer();
           $http.put('http://recruiting-api.nextcapital.com/users/'+userId+'/todos/'+toDoId, {"api_token":apiKey, "todo": {"description": desc, "is_complete": isComplete}}).then(function (response) {
                if(response.status == 200){
                    toastr.success("successfully updated a ToDo item");
                    dfd.resolve(response.data);
                }else{
                    toastr.error("unable to update toDos");
                    console.log("failure update todo inside services");
                    dfd.resolve(false);
                }
            });
            return dfd.promise;
        }

    }
});

ParkMe.factory('userDetailsService', function(){
   var userDetails = {};
    var todos ={};
    return{
        saveDetails: function(api, email, id, todoList){
            userDetails.api_token = api;
            userDetails.email = email;
            userDetails.id = id;
            userDetails.todos = todoList;
        },

        getUserDetails: function(){
            return userDetails;
        },

        saveUserTodos: function(todo){
        todos = todo;
        },

        getUserTodos: function(){
            return todos;
        }
    }
});
