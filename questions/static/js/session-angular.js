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

	$scope.vote = function(question, val){
		$scope.apply(function(){
			if(question.vote == val){
				question.vote = 0;
			}else{
				question.vote = val;
			}
			$http({
				method: 'POST',
				url: question.resource_uri+"vote/",
				data: $.param({vote:question.vote}),
				headers: {'Content-Type': 'application/x-www-form-urlencoded'}
			});
		})
	}
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
