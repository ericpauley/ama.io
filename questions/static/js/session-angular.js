var sessionApp = angular.module('sessionApp', ['ngRoute', 'ngSanitize', 'homepage']);

sessionApp.controller('ProfileCtrl', function ProfileCtrl($scope, $http, $timeout, $rootScope, $sce) {
	$http.get("/api/v1/user/"+GLOBALS['user']+"/", {
		params: {full_pages: true}
	}).success(function(data) {
		$scope.user = data;
	});
	$scope.qfilter={"action_type":"question"}
	$scope.tab="questions"
});

sessionApp.controller('SessionCtrl', function SessionCtrl($scope, $http, $timeout, $rootScope, $sce){
	$scope.toApply = null;
	function repeat(){
		if(GLOBALS['owner'])
			$timeout(function(){
				repeat();
			}, 10000);
		else
			$timeout(function(){
				repeat();
			}, 30000);
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
	$scope.state.user = GLOBALS['user']
	$scope.state.edit = null;
	$scope.state.owner = GLOBALS['owner']
	$scope.state.question = ""
	$scope.state.drafts = {}

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

	$scope.ask = function(){
		$http({
			method: 'POST',
			url: $scope.session.resource_uri+"ask/",
			data: $.param({question:$scope.state.question}),
			headers: {'Content-Type': 'application/x-www-form-urlencoded'}
		}).
		success(function(data, status, headers, config) {
			$scope.session.questions.unshift(data.question);
			$scope.state.question = "";
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

	$scope.answer = function(question, value){
		$scope.state.edit = null;
		$scope.toApply = null;
		$scope.state.answerdraft = false;
		$scope.state.answering = false;
		question.answer = {
			response: value,
			created: Date()
		}
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
		$scope.state.answering = false
	})

	changeImage = function(){
		$("#image-edit").ajaxSubmit({
			success:function(data){
	            $scope.session.image = data.thumbnail;
	            $scope.$apply();
	        }
		})
	}
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
		if(! input){
			return undefined
		}
		return $sce.trustAsHtml(markdown.toHTML(input));
	};
}]);

sessionApp.filter('countdown', function(){
	return function(input){
		return moment(input).fromNow()
	};
});
