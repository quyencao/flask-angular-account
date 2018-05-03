angular.module('app')
    .service('authService', ['$cookieStore', '$http', 'ajaxService',
        function ($cookieStore, $http, ajaxService) {

        var isLogin = false;

        this.login = function (username, password) {
            return ajaxService.ajaxPost2({
                username: username,
                password: password
            }, '/login').then(function (response, status) {
                if(response.data.token) {
                    $cookieStore.put('token', response.data.token);
                    $http.defaults.headers.common.Authorization = response.data.token;
                    isLogin = true;
                    return true;
                } else {
                    return false;
                }
            }).catch(function (reason) {
                return false;
            });
        };

        this.isLoggedIn = function () {
            return isLogin;
        };
        
        this.logout = function () {
            isLogin = false;
        };
    }]);