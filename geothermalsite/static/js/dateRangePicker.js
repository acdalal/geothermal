function invalidDate(date) {
    for (var i = 0; i < disabledRanges.length; i++) {
        if (date >= moment(disabledRanges[i].start) && date <= moment(disabledRanges[i].end)) {
            return true;
        }
    }
    return false;
}


function setUpDatePicker(id, disabledRanges) {
    $(id).daterangepicker({
        isInvalidDate: invalidDate,
        minDate: dataStartDate,
        maxDate: dataEndDate,
        ranges: {
            'Last 7 Available Days': [moment(dataEndDate).subtract(6, 'days'), moment()],
            'Last 30 Available Days': [moment(dataEndDate).subtract(29, 'days'), moment()],
            'Last 3 Available Months': [moment(dataEndDate).subtract(3, 'months'), moment()],
            'Last Available Year': [moment(dataEndDate).subtract(1, 'years'), moment()]
        },
    })
}


var disabledRanges = [];
outageList.forEach(range => {
    disabledRanges.push({start: range['startDate'], end: range['endDate']});
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
})


$('#id_tempVsDepthTimestamp').daterangepicker({
    singleDatePicker: true,
    minDate: dataStartDate,
    maxDate: dataEndDate,
    isInvalidDate: invalidDate
})

var ids = ['#id_tempVsTimeDateRange', '#id_temperatureProfileDateRange'];
ids.forEach(id => {
    setUpDatePicker(id, disabledRanges);
    $(id).value = moment(dataEndDate).subtract(30, "days").format("MM/DD/YYYY") + " - " + moment(dataEndDate).format("MM/DD/YYYY")
})


$('#id_temperatureProfileTimeSelector').value = "12:00 AM"
$('#id_tempVsDepthTimestamp').value = dataEndDate
