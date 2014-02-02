sessionApp.controller("UnansweredCtrl", function UnansweredCtrl($scope, $rootScope, $routeParams, $http) {
    $scope.state = $rootScope
    $http.get("/api/v1/question/", {
        params: {
            session: $routeParams.sessionId,
            answer__isnull: true
        }
    }).success(function(data) {
        $scope.state.questions = data.objects
        $scope.state.next = data.meta.next
        if ($scope.state.newQuestion != null) {
            angular.forEach($scope.state.questions, function(value, key) {
                if (value.id == $scope.state.newQuestion.id) {
                    $scope.state.questions.splice(key, 1)
                }
            })
            $scope.state.questions.unshift($scope.state.newQuestion)
            $scope.state.newQuestion = null
        }
        $rootScope.$broadcast("tabChange", {
            "tab": "unanswered"
        })
    })
})

sessionApp.controller("AnsweredCtrl", function AnsweredCtrl($scope, $rootScope, $routeParams, $http) {
    $scope.state = $rootScope
    $http.get("/api/v1/question/", {
        params: {
            session: $routeParams.sessionId,
            answer__isnull: false
        }
    }).success(function(data) {
        $scope.state.questions = data.objects
        $scope.state.next = data.meta.next
        $rootScope.$broadcast("tabChange", {
            "tab": "answered"
        })
    })
})

sessionApp.controller("StarredCtrl", function StarredCtrl($scope, $rootScope, $routeParams, $http) {
    $scope.state = $rootScope
    $http.get("/api/v1/question/", {
        params: {
            session: $routeParams.sessionId,
            starred: true
        }
    }).success(function(data) {
        $scope.state.questions = data.objects
        $scope.state.next = data.meta.next
        $rootScope.$broadcast("tabChange", {
            "tab": "starred"
        })
    })
})

sessionApp.controller("QuestionCtrl", function QuestionCtrl($scope, $rootScope, $routeParams, $http) {
    $scope.state = $rootScope;
    $scope.state.comment = "";
    $scope.state.answering = false;
    $scope.state.drafts[$routeParams.questionId] = $scope.state.answerdraft;
    $http.get("/api/v1/question/" + $routeParams.questionId + "/").success(function(data) {
        $scope.state.questions = [data]
        $rootScope.$broadcast("tabChange", {
            "tab": "question"
        })
    })
    $scope.state.next = null
    $scope.comments = null
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
    if (GLOBALS['state'] == "before") {
        redirect = '/s/' + GLOBALS['session'] + '/unanswered'
    } else {
        redirect = '/s/' + GLOBALS['session'] + '/answered'
    }
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
        redirectTo: redirect
    });
    $locationProvider.html5Mode(true);
});