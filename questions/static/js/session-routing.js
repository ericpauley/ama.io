sessionApp.controller("UnansweredCtrl", function UnansweredCtrl($scope, $rootScope) {
    $rootScope.$broadcast("tabChange", {
        "qfilter": {
            'answered': 'false'
        },
        "tab": "unanswered"
    })
    $scope.state = $rootScope
})

sessionApp.controller("AnsweredCtrl", function AnsweredCtrl($scope, $rootScope) {
    $rootScope.$broadcast("tabChange", {
        "qfilter": {
            'answered': 'true'
        },
        "tab": "answered"
    })
    $scope.state = $rootScope
})

sessionApp.controller("StarredCtrl", function StarredCtrl($scope, $rootScope) {
    $rootScope.$broadcast("tabChange", {
        "qfilter": {
            'starred': 'true'
        },
        "tab": "starred"
    })
    $scope.state = $rootScope
})

sessionApp.controller("QuestionCtrl", function QuestionCtrl($scope, $rootScope, $routeParams, $http) {
    $rootScope.$broadcast("tabChange", {
        "qfilter": {
            'id': $routeParams.questionId.toString()
        },
        "tab": "question"
    })
    $scope.state = $rootScope;
    $scope.state.comment = "";
    $scope.state.answering = false;
    $scope.state.drafts[$routeParams.questionId] = state.answerdraft;
    $http.get("/api/v1/comment/", {
        params: {
            question: $routeParams.questionId
        }
    }).success(function(data) {
        $scope.comments = data.objects;
    });
    $scope.postComment = function() {
        $http.post("/api/v1/comment/", {
            question: "/api/v1/question/" + $routeParams.questionId + "/",
            comment: $scope.state.comment
        }).success(function(data, status, headers) {
            $scope.state.comment = "";
            $http.get(headers("Location")).success(function(data) {
                $scope.comments.unshift(data);
            });
            if (!$scope.state.owner) {
                $scope.state.commentTimer = moment().add('minutes', 1).valueOf();
                $timeout(function() {
                    $scope.state['commentTimer'] = null;
                }, $scope.state.commentTimer - moment().unix());
            }
        }).error(function(data) {
            if (data.reason == 'too_soon') {
                $scope.state.commentTimer = Date.parse(data.soonest);
                $timeout(function() {
                    $scope.state['commentTimer'] = null;
                }, $scope.state.commentTimer - moment().valueOf());
            }
        })
    }
})

sessionApp.config(function($routeProvider, $locationProvider, $sceDelegateProvider) {
    $sceDelegateProvider.resourceUrlWhitelist([
        'self',
        'http://static.ama.io/**'
    ]);
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
        redirectTo: '/s/' + GLOBALS['session'] + '/unanswered'
    });
    $locationProvider.html5Mode(true);
});