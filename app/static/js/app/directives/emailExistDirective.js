angular.module('app')
    .directive('emailExist', ['$http', function ($http) {
        return {
            require: 'ngModel',
            link: function (scope, elem, attrs, ctrl) {
                ctrl.$parsers.push(function (value) {
                  if(typeof value !== "undefined" && value !== "") {
                    $http({
                       method: 'POST',
                       url: '/exist',
                       data: { email: value }
                    }).then(function (response) {
                       exist = response.data.exist;
                       ctrl.$setValidity("available", !exist);
                    }).catch(function (reason) {
                       ctrl.$setValidity("available", true);
                    })
                  }
                  return value;
                });
            }
        }
    }]);