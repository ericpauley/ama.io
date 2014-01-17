var sessionApp = angular.module('sessionApp', ['ngRoute', 'ngSanitize', 'homepage', 'ngCookies']);

sessionApp.controller('ProfileCtrl', function ProfileCtrl($scope, $http, $timeout, $rootScope, $sce) {
    $http.get("/api/v1/user/" + GLOBALS['user'] + "/", {
        params: {
            full_pages: true
        }
    }).success(function(data) {
        $scope.user = data;
    });
    $scope.qfilter = {
        "action_type": "question"
    }
    $scope.tab = "questions"
});

sessionApp.controller('SessionCtrl', function SessionCtrl($scope, $http, $timeout, $rootScope, $sce, $cookieStore) {
    $scope.toApply = null;

    function repeat() {
        if (GLOBALS['owner'])
            $timeout(repeat, 10000);
        else
            $timeout(repeat, 30000);
        $http.get("/api/v1/session/" + GLOBALS['session'] + "/").success(function(data) {
            if ($scope.state.edit == null && !$scope.state.answering && $scope.refresh && $scope.state.questionEdit == 0) {
                $scope.session = data;
            } else {
                $scope.toApply = data;
            }
        });
    }
    repeat();
    $scope.sessionId = GLOBALS['session']
    $scope.staticRoot = GLOBALS.staticRoot;
    $scope.state = $rootScope
    $scope.state.user = GLOBALS['user']
    $scope.state.edit = null;
    $scope.state.questionEdit = 0;
    $scope.state.owner = GLOBALS['owner']
    $scope.state.question = ""
    $scope.state.drafts = {}
    $scope.refresh = true;
    $scope.state.question = $cookieStore.get("askDrafts." + GLOBALS['session']) || "";
    $cookieStore.remove("askDrafts." + GLOBALS['session']);

    function reapply() {
        $timeout(reapply, 1000);
    }
    reapply();

    $scope.$watch("state.edit", function() {
        if ($scope.toApply != null) {
            $scope.session = $scope.toApply;
            $scope.toApply = null;
        }
        if ($scope.state.edit == "title") {
            $("#edit-title").focus();
        }
    })

    $scope.facebook = function() {
        FB.ui({
                method: 'feed',
                name: $scope.session.title,
                link: $('<a href="/s/' + $scope.session.slug + '"></a>')[0].href,
                picture: $scope.session.image,
                caption: $scope.session.name,
                description: $scope.session.desc
            },
            function(response) {

            }
        );
    }

    $scope.editQuestion = function(question) {
        $http({
            method: "PATCH",
            url: question.resource_uri,
            data: {
                question: question.question
            }
        }).success(function() {

        }).error(function() {

        });
    }

    $scope.vote = function(question, val) {
        var old = question.vote;
        if (question.vote == val) {
            question.vote = 0;
        } else {
            question.vote = val;
        }
        $http({
            method: 'POST',
            url: question.resource_uri + "vote/",
            data: $.param({
                vote: question.vote
            }),
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        });
        question.score += question.vote - old;
    }

    $scope.delete = function(question, index) {
        $http({
            method: 'DELETE',
            url: question.resource_uri,
        }).success(function() {
            $scope.session.questions.splice($scope.session.questions.indexOf(question), 1);
        });
    }

    $scope.star = function(question, val) {
        question.starred = val;
        if (val) {
            var data = 1;
        } else {
            var data = 0;
        }
        $http({
            method: 'POST',
            url: question.resource_uri + "star/",
            data: $.param({
                star: data
            }),
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        });
    }

    $scope.ask = function() {
        $http({
            method: 'POST',
            url: $scope.session.resource_uri + "ask/",
            data: $.param({
                question: $scope.state.question
            }),
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        }).
        success(function(data, status, headers, config) {
            $scope.session.questions.unshift(data.question);
            $scope.state.question = "";
            if(!data.staff){
                $scope.state.askTimer = moment().add('minutes', 1).valueOf();
                $timeout(function() {
                    $scope.state['askTimer'] = null;
                }, $scope.state.askTimer - moment().valueOf());
            }
        }).
        error(function(data, status, headers, config) {
            $scope.state.askTimer = moment().add('minutes', 1).valueOf();
            $timeout(function() {
                $scope.state['askTimer'] = null;
            }, $scope.state.askTimer - moment().valueOf());
        });
    }

    $scope.doAsk = function() {
        if (GLOBALS['user']) {
            $scope.ask();
        } else {
            $cookieStore.put("askDrafts." + GLOBALS['session'], $scope.state.question);
            $("#btnc").click();
        }
    }

    $scope.edit = function(field, value) {
        $scope.state.edit = null;
        if ($scope.toApply != null)
            $scope.toApply[field] = value;
        data = {}
        data[field] = value;
        $http({
            method: 'PATCH',
            url: $scope.session.resource_uri,
            data: data,
        })
    }

    $scope.answer = function(question, value) {
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
            url: question.resource_uri + "answer/",
            data: $.param({
                answer: value
            }),
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
        })
    }

    $rootScope.$on("tabChange", function(event, args) {
        angular.extend($scope, args)
        $scope.state.answering = false
    })

    $scope.endSession = function() {
        $http({
            method: "PATCH",
            url: "/api/v1/session/" + GLOBALS['session'] + "/",
            data: {
                end_time: Date()
            }
        })
    }

    changeImage = function() {
        $("#image-edit").ajaxSubmit({
            success: function(data) {
                $scope.session.image = data.thumbnail;
                $scope.$apply();
            }
        })
    }

    $scope.twitter = function() {
        if ($scope.session) {
            if ($scope.owner) {
                return "I'm doing an AMA! Check it out! " + $('<a href="/s/' + $scope.session.slug + '"></a>')[0].href;
            } else {
                return $scope.session.name + " is doing an AMA! Check it out! " + $('<a href="/s/' + $scope.session.slug + '"></a>')[0].href;
            }

        } else
            return ""
    }

});

sessionApp.directive('focusOnShow', function($timeout) {
    return {
        link: function(scope, element, attrs) {
            scope.$watch(attrs.ngShow, function(val) {
                if (angular.isDefined(val) && val) {
                    $timeout(function() {
                        element[0].focus();
                    });
                }
            }, true);

            element.bind('blur', function() {
                if (angular.isDefined(attrs.ngFocusLost)) {
                    scope.$apply(attrs.ngFocusLost);

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

sessionApp.filter('linesplit', ['$sce',
    function($sce) {
        return function(input) {
            input = $.trim(input)
            input = "<p>" + input.replace(/(\&\#10;)/g, "<br/>") + "</p>"
            return $sce.trustAsHtml(input);
        };
    }
]);

sessionApp.filter('countdown', function() {
    return function(input, prefix) {
        return moment(input).fromNow(prefix);
    };
});

sessionApp.filter('escape', function() {
    return window.escape;
});