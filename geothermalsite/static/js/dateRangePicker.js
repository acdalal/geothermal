function setUpDatePicker(id, disabledRanges) {

    var start = moment(dataEndDate).subtract(29, 'days')
    var end = moment(dataEndDate)

    function cb(start, end) {
        $(id).html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'));
    }

    $(id).daterangepicker({
        isInvalidDate: function(date) {
            for (var i = 0; i < disabledRanges.length; i++) {
                if (date >= moment(disabledRanges[i].start) && date <= moment(disabledRanges[i].end)) {
                    return true;
                }
            }
            return false;
        },
        minDate: dataStartDate,
        maxDate: dataEndDate,
        ranges: {
            'Last 7 Available Days': [moment(dataEndDate).subtract(6, 'days'), moment()],
            'Last 30 Available Days': [moment(dataEndDate).subtract(29, 'days'), moment()],
            'Last 3 Available Months': [moment(dataEndDate).subtract(3, 'months'), moment()],
            'Last Available Year': [moment(dataEndDate).subtract(1, 'years'), moment()]
        },

    }, cb);

    cb(start, end);
};

var ids = ['#id_tempVsTimeDateRange', '#id_tempVsDepthTimestamp', '#id_temperatureProfileDateRange', '#id_temperatureProfileTimeSelector'];

var disabledRanges = [];
outageList.forEach(range => {
    disabledRanges.push({start: range['startDate'], end: range['endDate']});
});



ids.forEach(id => {
    setUpDatePicker(id, disabledRanges);
})


$('#id_temperatureProfileTimeSelector').daterangepicker({
    timePicker: true,
    singleDatePicker: true,
    timePicker24Hour: false,
    timePickerIncrement: 1,
    timePickerSeconds: false,
    locale: {
        format: 'hh:mm A'
    }
}).on('show.daterangepicker', function (ev, picker) {
    picker.container.find('.calendar-table').hide();
});

$('#id_temperatureProfileTimeSelector').html("12:00 AM");
