rotated = ['Justin', 'Eric', 'Jared', 'Max']

var homepage = angular.module('homepage', []);

homepage.controller("RotateCtrl", function RotateCtrl($scope){
	$scope.item = rotated.sort(function() {return 0.5 - Math.random()})[0];
});

homepage.controller("CreateCtrl", function CreateCtrl($scope, $http){
	$scope.date = moment().format("YYYY-MM-DD");
	$scope.time = moment().format("HH:mm");
	$scope.duration = 1;
});

homepage.controller("SigninCtrl", function SigninCtrl($scope, $http){
    $scope.error = null;
    $scope.working = null;
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
            $scope.error = data.reason;
            $scope.working = false;
        });
    }
});

homepage.directive("fileread", [function () {
    return {
        scope: {
            fileread: "="
        },
        link: function (scope, element, attributes) {
            element.bind("change", function (changeEvent) {
                var reader = new FileReader();
                reader.onload = function (loadEvent) {
                    scope.$apply(function () {
                        scope.fileread = loadEvent.target.result;
                    });
                }
                reader.readAsDataURL(changeEvent.target.files[0]);
            });
        }
    }
}]);
