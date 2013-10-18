var sessionApp = angular.module('sessionApp', ['ngRoute', 'ngSanitize']);

sessionApp.controller('ProfileCtrl', function ProfileCtrl($scope, $http, $timeout, $rootScope, $sce) {
	$http.get("/api/v1/user/"+GLOBALS['user']+"/").success(function(data) {
		$scope.user = data;
	});
	$scope.qfilter={"action_type":"question"}
	$scope.tab="questions"
});

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

	$scope.answer = function(question, index, value){
		$scope.state.edit = null;
		$scope.toApply = null;
		question.answerdraft = false;
		question.answer.created = Date();
		question.answered = (value != "")
		$http({
			method: 'POST',
			url: question.resource_uri+"answer/",
			data: $.param({answer: value}),
			headers: {'Content-Type': 'application/x-www-form-urlencoded'},
		})
	}

	$rootScope.$on("tabChange", function(event, args){
		angular.extend($scope, args)
	})
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

sessionApp.filter('plain', function() {
	return function(text) {
		return String(text).replace(/<(?:.|\n)*?>/gm, '');
	}
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
