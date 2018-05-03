var app = angular.module('app', ['ui.bootstrap', 'ui.router', 'ngCookies'])

app.config(['$stateProvider', '$httpProvider', function ($stateProvider, $httpProvider) {
    $stateProvider
        .state('login', {
            url: '/login',
            controller: 'loginController',
            templateUrl: '/static/js/app/partials/login.html',
            data: { restrict: false }
        })
        .state(
            'accounts', {
                url: '/accounts',
                controller: 'accountInqueryController',
                templateUrl: '/static/js/app/partials/account.html',
                data: { restrict: true }
            }
        )

        $httpProvider.interceptors.push(['$cookieStore', '$state', function ($cookieStore, $state) {
            return {
                request: function (config) {
                    if($cookieStore.get('token')) {
                        config.headers.Authorization = $cookieStore.get('token');
                    }
                    return config;
                }
            }
        }])
}]);

app.run(['$rootScope', '$state', '$transitions', 'authService',
    function ($rootScope, $state, $transitions, authService) {
    $rootScope.isLoggedIn = false;

    $transitions.onStart({}, function (trans) {
        restrict = trans.$to().data.restrict;
        if (restrict && !authService.isLoggedIn()) {
            $state.go('login');
        }

        if (authService.isLoggedIn()) {
            $state.go('accounts');
        }

        $rootScope.isLoggedIn = authService.isLoggedIn();
    });
}]);