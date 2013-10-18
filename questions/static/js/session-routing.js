sessionApp.controller("UnansweredCtrl", function UnansweredCtrl($scope, $rootScope){
	$rootScope.$broadcast("tabChange", {"qfilter":{'answered':'false'}, "tab":"unanswered"})
	$scope.state = $rootScope
})

sessionApp.controller("AnsweredCtrl", function AnsweredCtrl($scope, $rootScope){
	$rootScope.$broadcast("tabChange", {"qfilter":{'answered':'true'}, "tab":"answered"})
	$scope.state = $rootScope
})

sessionApp.controller("StarredCtrl", function StarredCtrl($scope, $rootScope){
	$rootScope.$broadcast("tabChange", {"qfilter":{'starred':'true'}, "tab":"starred"})
	$scope.state = $rootScope
})

sessionApp.controller("QuestionCtrl", function QuestionCtrl($scope, $rootScope, $routeParams){
	$rootScope.$broadcast("tabChange", {"qfilter":{'id':$routeParams.questionId.toString()}, "tab":"question"})
	$scope.state = $rootScope
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
