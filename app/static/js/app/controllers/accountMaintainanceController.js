angular.module('app')
    .controller('accountMaintainanceController', ['$scope', '$uibModalInstance', 'accountService',
                                'selectedAccount', 'action',
        function ($scope, $uibModalInstance, accountService, selectedAccount, action) {
        $scope.account = selectedAccount;
        $scope.action = action;
        $scope.title = action ? 'Create New Account' : 'Edit ' + selectedAccount.account_number;
        $scope.emailFormat = /^[a-z]+[a-z0-9._]+@[a-z]+\.[a-z.]{2,5}$/;

        $scope.save = function () {
            if($scope.account_form.$invalid) {
                return;
            }

            if(action) {
                // Create
                accountService.createAccount($scope.account, $scope.actionSuccessComplete, $scope.actionErrorComplete);
            } else {
                // Update
                accountService.updateAccount($scope.account, $scope.actionSuccessComplete, $scope.actionErrorComplete);
            }
        };

        $scope.actionSuccessComplete = function(response, status) {
            $uibModalInstance.close($scope.account)
        };

        $scope.actionErrorComplete = function() {

        };

        $scope.close = function () {
            $uibModalInstance.dismiss('cancel');
        };

    }]);