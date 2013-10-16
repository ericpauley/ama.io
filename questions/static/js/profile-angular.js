var profileApp = angular.module('profileApp', []);

profileApp.controller('ProfileCtrl', function ProfileCtrl($scope, $http, $timeout, $rootScope, $sce) {
	$http.get("/api/v1/user/" + GLOBALS['user'] + "/").success(function(data) {
		$scope.user = data;
	});
	$scope.qfilter={"action_type":"question"}
	$scope.tab="questions"
});

profileApp.filter('markdown', ['$sce',
	function($sce) {
		return function(input) {
			if (input == undefined) {
				return undefined;
			} else {
				return $sce.trustAsHtml(markdown.toHTML(input));
			}
		};
	}
]);

profileApp.filter('plain',['$sce', function($sce) {
	return function(text) {
		return $sce.trustAsHtml(String(text).replace(/<(?:.|\n)*?>/gm, ''));
	}
}]);

profileApp.filter('countdown', function() {
	return function(input) {
		if (input == undefined) {
			return undefined;
		} else {
			return moment(input).fromNow()
		}
	};
});
