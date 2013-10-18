var sessionApp = angular.module('sessionApp', ['ngRoute']);

sessionApp.controller('SessionCtrl', function SessionCtrl($scope, $http, $timeout, $rootScope, $sce){
	$scope.toApply = null;
	function repeat(){
		$timeout(function(){
			repeat();
		}, 10000);
		$http.get("/api/v1/session/"+GLOBALS['session']+"/").success(function(data) {
			if($scope.state.edit == null){
				$scope.session = data;
			}else{
				$scope.toApply = data;
			}
		});
	}
	repeat();
	$scope.sessionId = GLOBALS['session']
	$scope.state = $rootScope
	$scope.state.edit = null;
	$scope.state.owner = GLOBALS['owner']

	$scope.$watch("state.edit", function(){
		if($scope.toApply != null){
			$scope.session = $scope.toApply;
			$scope.toApply = null;
		}
		if($scope.state.edit == "title"){
			$("#edit-title").focus();
		}
	})

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

	$scope.edit = function(field, value){
		$scope.state.edit = null;
		if($scope.toApply != null)
			$scope.toApply[field] = value;
		data = {}
		data[field] = value;
		$http({
			method: 'PATCH',
			url: $scope.session.resource_uri,
			data: data,
		})
	}

	$rootScope.$on("tabChange", function(event, args){
		angular.extend($scope, args)
	})
});

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

sessionApp.directive('focusOnShow', function($timeout) {
    return {
        link: function ( scope, element, attrs ) {
            scope.$watch( attrs.ngShow, function ( val ) {
                if ( angular.isDefined( val ) && val ) {
                    $timeout( function () { element[0].focus(); } );
                }
            }, true);

            element.bind('blur', function () {
                if ( angular.isDefined( attrs.ngFocusLost ) ) {
                    scope.$apply( attrs.ngFocusLost );

                }
            });
        }
    };
});

sessionApp.filter('markdown', ['$sce', function($sce){
	return function(input){
		return $sce.trustAsHtml(markdown.toHTML(input));
	};
}]);

sessionApp.filter('countdown', function(){
	return function(input){
		return moment(input).fromNow()
	};
});
