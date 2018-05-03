angular.module('app')
    .controller('accountInqueryController', ['$scope', '$uibModal', 'accountService',
    function ($scope, $uibModal, accountService) {

        $scope.initializeController = function () {

            $scope.isCollapsed = false;

            $scope.currentPageNumber = 1;
            $scope.pageSize = 5;
            $scope.accounts = [];

            $scope.accountNumber = undefined;
            $scope.firstName = '';
            $scope.lastName = '';
            $scope.address = '';
            $scope.email = '';
            $scope.gender = -1;
            $scope.balance = undefined;
            $scope.employer = '';
            $scope.city = '';
            $scope.state = '';

            $scope.sortDirection = 1;
            $scope.sortExpression = "balance";

            $scope.sortExpressionClient = "balance";
            $scope.sortReverseClient = false;

            $scope.getAccounts();

            // Account Modal
            $scope.animationsEnabled = true;
            $scope.selectedAccount = undefined;
            $scope.selectedAccountIndex = undefined;
        };
        
        $scope.getAccounts = function () {
            accountInquery = $scope.getAccountInquery();
            accountService.getAccounts(accountInquery, $scope.accountInquerySuccess, $scope.accountInqueryError);
        };

        $scope.accountInquerySuccess = function (response, status) {
            $scope.accounts = response.data.accounts;
            $scope.totalAccounts = response.data.pagination.total;
            $scope.totalPages = response.data.pagination.last_page;
            $scope.currentPageNumber = response.data.pagination.current_page;
            $scope.nextPageNumber = response.data.pagination.next_page;
            $scope.prevPageNumber = response.data.pagination.prev_page;
        };

        $scope.accountInqueryError = function (error) {

        };

        $scope.getAccountInquery = function () {
             var accountInquiry = new Object();
             accountInquiry.page = $scope.currentPageNumber;
             accountInquiry.per_page = $scope.pageSize;
             accountInquiry.sortDirection = $scope.sortDirection;
             accountInquiry.sortExpression = $scope.sortExpression;

             if($scope.accountNumber !== undefined) {
                 accountInquiry.accountNumber = $scope.accountNumber;
             }

             if($scope.firstName !== '') {
                 accountInquiry.firstName = $scope.firstName;
             }

             if($scope.lastName !== '') {
                 accountInquiry.lastName = $scope.lastName;
             }

             if($scope.email !== '') {
                 accountInquiry.email = $scope.email;
             }

             if($scope.gender == 'M' || $scope.gender == 'F') {
                 accountInquiry.gender = $scope.gender;
             }

             if($scope.balance !== undefined) {
                 accountInquiry.balance = $scope.balance;
             }

             if($scope.city !== '') {
                 accountInquiry.city = $scope.city;
             }

             if($scope.state !== '') {
                 accountInquiry.state = $scope.state;
             }

             if($scope.employer !== '') {
                 accountInquiry.employer = $scope.employer;
             }

             if($scope.address !== '') {
                 accountInquiry.address = $scope.address;
             }

             return accountInquiry;
        };
        
        $scope.pageChanged = function () {
            $scope.getAccounts();
        };

        $scope.searchAccount = function () {
            $scope.currentPageNumber = 1;
            $scope.getAccounts();
        };

        $scope.reset = function () {
            $scope.accountNumber = undefined;
            $scope.firstName = '';
            $scope.lastName = '';
            $scope.email = '';
            $scope.gender = -1;
            $scope.balance = undefined;
            $scope.city = '';
            $scope.state = '';
            $scope.address = '';
            $scope.getAccounts();
        };

        // Account Modal
        $scope.openModal = function(index) {
            if(index !== undefined) {
                $scope.selectedAccountIndex = index;
                $scope.selectedAccount = angular.copy($scope.accounts[index]);
            }
            $scope.open('lg');
        };

        $scope.open = function (size, parentSelector) {
            var parentElem = parentSelector ?
              angular.element($document[0].querySelector('.account-modal ' + parentSelector)) : undefined;
            var modalInstance = $uibModal.open({
              animation: $scope.animationsEnabled,
              ariaLabelledBy: 'modal-title',
              ariaDescribedBy: 'modal-body',
              templateUrl: '/static/js/app/partials/accountMaintainance.html',
              controller: 'accountMaintainanceController',
              size: size,
              appendTo: parentElem,
              resolve: {
                selectedAccount: function () {
                  if($scope.selectedAccount === undefined) {
                      return {};
                  }
                  return $scope.selectedAccount;
                },
                action: function () {
                    if($scope.selectedAccount === undefined) {
                        return true;
                    }
                    return false;
                }
              }
            });

            modalInstance.result.then(function (editItem) {
              if(editItem) {
                  $scope.accounts[$scope.selectedAccountIndex] = editItem;
              }
              $scope.resetModal();
            }, function () {
              $scope.resetModal();
            });
        };

        $scope.resetModal = function () {
            $scope.selectedAccount = undefined;
            $scope.selectedAccountIndex = undefined;
        };

        $scope.sortBy = function (exp) {
            $scope.sortReverseClient = ($scope.sortExpressionClient === exp) ? !$scope.sortReverseClient : false;
            $scope.sortExpressionClient = exp;
        };

        $scope.sort = function (exp) {
            if($scope.sortExpression === exp) {
                if($scope.sortDirection == 1) {
                    $scope.sortDirection = -1;
                } else {
                    $scope.sortDirection = 1;
                }
            }
            $scope.sortExpression = exp;
        };

        $scope.delete = function (index) {
            account = $scope.accounts[index];
            accountService.deleteAccount(account.account_number, $scope.accountInquerySuccess, $scope.accountInqueryError);
        };

        $scope.$watch('sortExpression', function (value) {
            $scope.getAccounts();
        });

        $scope.$watch('sortDirection', function (value) {
            $scope.getAccounts();
        });

        $scope.$watch('pageSize', function (value) {
            $scope.getAccounts();
        })
    }]);