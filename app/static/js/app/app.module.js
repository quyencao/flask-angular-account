var app = angular.module('app', ['ui.bootstrap', 'ui.router', 'ngCookies'])

app.config(['$stateProvider', function ($stateProvider) {
    $stateProvider
        .state(
            'accounts', {
                url: '/accounts',
                controller: 'accountInqueryController',
                templateUrl: '/static/js/app/partials/accountInquery.html'
            }
        )
        .state('login', {
            url: '/login',
            controller: 'loginController',
            templateUrl: '/static/js/app/partials/login.html'
        })
        .state(
            'home', {
                url: '/home',
                controller: 'accountInqueryController',
                templateUrl: '/static/js/app/partials/account.html'
            }
        )
}]);

// app.run(['$rootScope', '$cookieStore', '$location', '$http',
//     function ($rootScope, $cookieStore, $location, $http) {
//     if($cookieStore.get('token')) {
//          $http.defaults.headers.common.Authorization = $cookieStore.get('token');
//     }
//
//     $rootScope.$on('$locationChangeStart', function (event, next, current) {
//         var publicPages = ['/login'];
//         var restrictedPage = publicPages.indexOf($location.path()) === -1;
//         if (restrictedPage && !$cookieStore.get('token')) {
//             $location.path('/login');
//         }
//     });
// }]);