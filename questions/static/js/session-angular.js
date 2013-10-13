var sessionApp = angular.module('sessionApp', ['ngResource']);

sessionApp.controller('SessionCtrl', function SessionCtrl($scope, $http, $resource, $timeout, $rootScope){
	function repeat(){
		$timeout(function(){
			repeat();
		}, 10000);
		$http.get("/api/v1/session/"+GLOBALS['session']+"/").success(function(data) {
			$scope.session = data;
		});
	}
	repeat();
	$scope.owner = GLOBALS['owner']
	$scope.sessionId = GLOBALS['session']

	$scope.vote = function(question, val){
		var old = question.vote;
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
		question.score += question.vote - old;
	}

	$scope.star = function(question, val){
		question.starred = val;
		if(val){
			var data = 1;
		}else{
			var data = 0;
		}
		$http({
			method: 'POST',
			url: question.resource_uri+"star/",
			data: $.param({star:data}),
			headers: {'Content-Type': 'application/x-www-form-urlencoded'}
		});
	}

	$scope.ask = function(question){
		$http({
			method: 'POST',
			url: $scope.session.resource_uri+"ask/",
			data: $.param({question:question}),
			headers: {'Content-Type': 'application/x-www-form-urlencoded'}
		}).
		success(function(data, status, headers, config) {
			$scope.session.questions.unshift(data.question);
			$scope.question = null;
			$scope.apply()
		}).
		error(function(data, status, headers, config) {
			// called asynchronously if an error occurs
			// or server returns response with an error status.
		});
	}

	$rootScope.$on("tabChange", function(event, args){
		$.extend($scope, args)
	})
});

sessionApp.controller("UnansweredCtrl", function UnansweredCtrl($scope, $rootScope){
	$rootScope.$broadcast("tabChange", {"qfilter":{'answered':'false'}, "tab":"unanswered"})
})

sessionApp.controller("AnsweredCtrl", function AnsweredCtrl($scope, $rootScope){
	$rootScope.$broadcast("tabChange", {"qfilter":{'answered':'true'}, "tab":"answered"})
})

sessionApp.controller("StarredCtrl", function StarredCtrl($scope, $rootScope){
	$rootScope.$broadcast("tabChange", {"qfilter":{'starred':'true'}, "tab":"starred"})
})

sessionApp.controller("QuestionCtrl", function QuestionCtrl($scope, $rootScope, $routeParams){
	$rootScope.$broadcast("tabChange", {"qfilter":{'id':$routeParams.questionId.toString()}, "tab":"question"})
})

sessionApp.config(function($routeProvider, $locationProvider) {
	$routeProvider.when('/s/:sessionId/unanswered', {
		controller: 'UnansweredCtrl',
		templateUrl: GLOBALS['session_html']
	}).when('/s/:sessionId/answered', {
		controller: 'AnsweredCtrl',
		templateUrl: GLOBALS['session_html']
	}).when('/s/:sessionId/starred', {
		controller: 'StarredCtrl',
		templateUrl: GLOBALS['session_html']
	}).when('/q/:questionId', {
		controller: 'QuestionCtrl',
		templateUrl: GLOBALS['session_html']
	}).otherwise({
		redirectTo: '/s/'+GLOBALS['session']+'/unanswered'
	});
	$locationProvider.html5Mode(true);
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
