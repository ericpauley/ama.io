rotated = ['Justin', 'Eric', 'Jared', 'Max']

var homepage = angular.module('homepage', []);

homepage.controller("RotateCtrl", function RotateCtrl($scope){
	$scope.item = rotated.sort(function() {return 0.5 - Math.random()})[0];
})

homepage.controller("CreateCtrl", function CreateCtrl($scope, $http){
	$scope.date = moment().format("YYYY-MM-DD");
	$scope.time = moment().format("HH:mm");
	$scope.duration = 1;
})

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
