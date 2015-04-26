angular.module('timeslotlist', ['checklist-model', 'ngMessages', 'ui.validate']).controller('TimeSlotListController', ['$scope', function($scope) {
	$scope.days = {
		1: 'Monday',
		2: 'Tuesday',
		3: 'Wednesday',
		4: 'Thursday',
		5: 'Friday',
		6: 'Saturday',
		7: 'Sunday'
	};

	$scope.edited_timeslot = null;

	$scope.init = function(initial) {
		$.each(initial, function(k, v) {
			v['days_of_week'] = v['days_of_week'].map(function(v) {
				return String(v);
			});
		});

		$scope.timeslots = initial;
	};

	$scope.add_timeslot = function() {
		$scope.edit_target_timeslot = 'new';
		$scope.edit_temp_timeslot = { days_of_week: [] };
	};

	$scope.edit_timeslot = function(ts) {
		$scope.edit_temp_timeslot = angular.copy(ts);
		$scope.edit_target_timeslot = ts;
	};

	$scope.delete_timeslot = function(ts) {
		$scope.timeslots = $($scope.timeslots).not([ts]).get();
	}

	$scope.confirm_timeslot = function(ts) {
		if (!$scope.edit_timeslot_form.$valid)
			return;

		if ($scope.edit_target_timeslot == 'new') {
			$scope.timeslots.push($scope.edit_temp_timeslot);
		} else {
			angular.copy(
				$scope.edit_temp_timeslot,
				$scope.edit_target_timeslot);
		}

		$scope.edit_target_timeslot = null;
	};

	$scope.cancel_edited_timeslot = function() {
		$scope.edit_target_timeslot = null;
		$scope.edit_temp_timeslot = { days_of_week: [] };
		$scope.edit_timeslot_form.$setPristine();
	};

	$scope.transform_readable_dow = function(dow_list) {
		dow_list_sorted = angular.copy(dow_list);
		dow_list_sorted.sort();

		dow_list_names = dow_list_sorted.map(function(v) {
			return $scope.days[v];
		});

		return dow_list_names.join(", ");
	};

	$scope.time_before = function(a, b) {
		var da = Date.parse('Thu, 01 Jan 1970 ' + a + ':00 GMT');
		var db = Date.parse('Thu, 01 Jan 1970 ' + b + ':00 GMT');

		return db > da;
	};
}]);
