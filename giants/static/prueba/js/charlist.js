angular.module('charlist', ['ngMessages', 'ui.validate']).controller('CharListController', ['$scope', function($scope) {
	$scope.delete_item = function(idx) {
		$scope.list.splice(idx, 1);
	}

	$scope.add_item = function() {
		$scope.list.push({'value':""});
	};

	$scope.unwrap = function(list) {
		return list.map(function(v) {
			return v.value;
		});
	};

	$scope.wrap = function(list) {
		return list.map(function(v) {
			return {'value': v};
		});
	};
}]);
