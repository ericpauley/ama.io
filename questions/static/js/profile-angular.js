var profileApp = angular.module('profileApp', ['restangular', 'ngRoute', 'ngSanitize']);

profileApp.config(function(RestangularProvider){
	RestangularProvider.setRestangularFields({
		selfLink: 'resource_uri'
	});
	RestangularProvider.setRequestSuffix('/');
	RestangularProvider.setDefaultHttpFields({cache: true});
})

profileApp.controller('ProfileCtrl', function ProfileCtrl($scope, $http, $timeout, Restangular, $rootScope, $sce) {
	var User = Restangular.one("api").one("v1").one("user")
	$scope.user = User.one(GLOBALS['user']).get()
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

profileApp.filter('plain', function() {
	return function(text) {
		return String(text).replace(/<(?:.|\n)*?>/gm, '');
	}
});

profileApp.filter('countdown', function() {
	return function(input) {
		if (input == undefined) {
			return undefined;
		} else {
			return moment(input).fromNow()
		}
	};
});
