angular.module('app')
    .service('accountService', ['ajaxService', function (ajaxService) {
        this.getAccounts = function (accountInquery, successFn, errorFn) {
            ajaxService.ajaxGetWithData(accountInquery, '/accounts', successFn, errorFn);
        };

        this.createAccount = function (account, successFn, errorFn) {
            ajaxService.ajaxPost(account, '/accounts', successFn, errorFn);
        };

        this.updateAccount = function (account, successFn, errorFn) {
            ajaxService.ajaxPost(account, '/account/' + account.account_number, successFn, errorFn);
        };

        this.deleteAccount = function (account_number, successFn, errorFn) {
            ajaxService.ajaxDelete('/account/' + account_number, successFn, errorFn);
        };
    }]);