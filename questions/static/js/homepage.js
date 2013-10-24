rotated = ['YouTubers', 'actors', 'musicians', 'athletes', 'politicians', 'astronauts', 'comedians', 'anyone'];

var homepage = angular.module('homepage', []);

homepage.controller("RotateCtrl", function RotateCtrl($scope){
	$scope.item = rotated.sort(function() {return 0.5 - Math.random()})[0];
});

homepage.controller("CreateCtrl", function CreateCtrl($scope, $http){
	$scope.date = moment().format("YYYY-MM-DD");
	$scope.time = moment().format("HH:mm");
	$scope.duration = 1;
    $("#create-session").ajaxForm({
        success:function(data){
            document.location = "/s/"+data.slug;
        },
        error:function(xhr){
            var err = xhr.responseText && $.parseJSON(xhr.responseText) || {};
            $scope.error = err.reason || 'error';
            $scope.$apply();
        }
    })
});

homepage.controller("SigninCtrl", function SigninCtrl($scope, $http){
    $scope.error = null;
    $scope.working = false;
    $scope.login = function(){
        $scope.error = null;
        $scope.working = true;
        $http({
            method: 'POST',
            url: "/api/v1/user/login/",
            data: $.param({
                username: $scope.username,
                password: $scope.password}),
            headers: {'Content-Type': 'application/x-www-form-urlencoded'}
        }).success(function(data){
            location.reload();
        }).error(function(data){
            $scope.error = data.reason || 'error';
            $scope.working = false;
        });
    }
});

homepage.controller("RegisterCtrl", function RegisterCtrl($scope, $http){
    $scope.error = null;
    $scope.working = false;

    $scope.register = function(){
        $scope.error = null;
        $scope.working = true;
        $http({
            method: 'POST',
            url: "/api/v1/user/register/",
            data: $.param({
                username: $scope.username,
                password: $scope.password,
                confirm: $scope.confirm,
                email: $scope.email}),
            headers: {'Content-Type': 'application/x-www-form-urlencoded'}
        }).success(function(data){
            location.reload();
        }).error(function(data){
            $scope.error = data.reason || 'error';
            $scope.working = false;
        });
    }
})

homepage.controller("RequestCtrl", function RequestCtrl($scope, $http){
    $scope.tweet = true;
    $scope.username = "";
    $scope.request = function(){
        $scope.error = null;
        $scope.working = true;
        $http({
            method: 'POST',
            url: "/api/v1/request/create/",
            data: $.param({
                username: $scope.username}),
            headers: {'Content-Type': 'application/x-www-form-urlencoded'}
        }).success(function(data){
            location.reload();
        }).error(function(data){
            $scope.error = data.reason || 'error';
            $scope.working = false;
        });
    }
})

homepage.controller("PasswordCtrl", function RequestCtrl($scope, $http){
    $scope.current = "";
    $scope.new1 = "";
    $scope.new2 = "";
    $scope.working = false;
    $scope.error = null;
    $scope.change = function(){
        $scope.error = null;
        if($scope.new1 != $scope.new2){
            $scope.error = "no_match"
        }else{
            $scope.working = true;
            $http({
                method: 'POST',
                url: '/api/v1/user/change_password/',
                data: $.param({
                    current: $scope.current,
                    new: $scope.new1
                }),
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            }).success(function(data){
                location.reload();
            }).error(function(data){
                $scope.error = data.reason || 'error';
                $scope.working = false;
            });
        }
    }
})

homepage.directive('fileRead', function () {
    return {
        require: '?ngModel',
        link: function (scope, el, attrs, ngModel) {
            if(!ngModel) return;
            ngModel.$render = function () {
                alert(el[0].files[0].name)
                ngModel.$setViewValue(el[0].files[0]);
            };

            el.bind('change', function (e) {
                var file = (e.srcElement || e.target).files[0];
                scope.$apply(ngModel.$render);
            });
        }
    };
});
