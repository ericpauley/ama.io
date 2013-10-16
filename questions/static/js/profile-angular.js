var profileApp = angular.module('profileApp', []);

profileApp.controller('ProfileCtrl', function ProfileCtrl($scope, $http, $timeout, $rootScope, $sce){
	$http.get("/api/v1/user/"+GLOBALS['user']+"/").success(function(data) {
		$scope.user = data;
	});

});
