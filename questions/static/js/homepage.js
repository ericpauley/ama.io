rotated = ['Justin', 'Eric', 'Jared', 'Max']

var homepage = angular.module('homepage', []);

homepage.controller("RotateCtrl", function RotateCtrl($scope){
	$scope.item = rotated.sort(function() {return 0.5 - Math.random()})[0];
})
