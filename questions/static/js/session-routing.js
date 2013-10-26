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

sessionApp.controller("QuestionCtrl", function QuestionCtrl($scope, $rootScope, $routeParams, $http){
	$rootScope.$broadcast("tabChange", {
		"qfilter":{'id':$routeParams.questionId.toString()},
		"tab":"question"
	})
	$scope.state = $rootScope;
	$scope.state.comment = "";
	$http.get("/api/v1/comment/", {
		params: {question:$routeParams.questionId}
	}).success(function(data){
		$scope.comments = data.objects;
	});
	$scope.postComment = function(){
		$http.post("/api/v1/comment/", {
			question:"/api/v1/question/"+$routeParams.questionId+"/",
			comment: $scope.state.comment
		}).success(function(data, status, headers){
			$scope.state.comment = "";
			$http.get(headers("Location")).success(function(data){
				$scope.comments.unshift(data);
			});
		}).error(function(data){

		})
	}
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
