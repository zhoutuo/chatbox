$(document).ready(function() {
	$('.date-picker').datepicker({
		autoclose: true,
		forceParse: true,
		endDate: new Date()
	});
});