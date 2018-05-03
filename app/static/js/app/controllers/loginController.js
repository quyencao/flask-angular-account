angular.module('app')
    .controller('loginController', ['$scope', '$state', 'authService',
    function ($scope, $state, authService) {
        $scope.username = '';
        $scope.password = '';


        $scope.login = function () {
            authService.login($scope.username, $scope.password)
                .then(function (result) {
                    if(result) {
                       $state.go('accounts');
                    } else {
                       $state.go('login');
                    }
                });
        };

        $scope.logout = function () {
            authService.logout();
            $state.go('login');
        };
    }]);