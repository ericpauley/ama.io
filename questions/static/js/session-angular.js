var sessionApp = angular.module('sessionApp', ['ngResource']);

sessionApp.controller('SessionCtrl', function SessionCtrl($scope, $http, $resource, $timeout){
	function repeat(){
		$timeout(function(){
			repeat();
		}, 10000);
		$http.get("/api/v1/session/"+GLOBALS['session']+"/").success(function(data) {
			$scope.session = data;
		});
	}
	repeat();
	$scope.qfilter = "false"
	$scope.owner = GLOBALS['owner']
});

sessionApp.filter('markdown', function(){
	return function(input){
		if(input == undefined){
			return undefined;
		}else{
			return markdown.toHTML(input);
		}
	};
});

sessionApp.filter('countdown', function(){
	return function(input){
		if(input == undefined){
			return undefined;
		}else{
			return moment(input).fromNow()
		}
	};
});
