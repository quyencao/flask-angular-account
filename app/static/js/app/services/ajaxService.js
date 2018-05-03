angular.module('app')
    .service('ajaxService', ['$http', function ($http) {
    this.ajaxGetWithData = function (data, url, successFn, errorFn) {
        $http({
            method: 'GET',
            url: url,
            params: data
        }).then(function (response, status, header, config) {
            successFn(response, status);
        }, function (response) {
            errorFn(response);
        });
    };

    this.ajaxPost = function (data, url, successFn, errorFn) {
        $http({
            method: 'POST',
            url: url,
            data: data
        }).then(function (response, status, header, config) {
            successFn(response, status);
        }, function (response) {
            errorFn(response);
        });
    };

    this.ajaxDelete = function (url, successFn, errorFn) {
        $http({
            method: 'DELETE',
            url: url
        }).then(function (response, status, header, config) {
            successFn(response, status);
        }, function (response) {
            errorFn(response);
        });
    };

    this.ajaxPost2 = function (data, url) {
        return $http({
            method: 'POST',
            url: url,
            data: data
        })
    };
}]);