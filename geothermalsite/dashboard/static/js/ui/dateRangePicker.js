var disabledRanges = [];
outageList.forEach(range => {
    disabledRanges.push({start: range['startDate'], end: range['endDate']});
})

var premadeRanges = {
    'Last 7 Available Days': [moment(dataEndDate, 'MM/DD/YYYY').subtract(6, 'days'), moment()],
    'Last 30 Available Days': [moment(dataEndDate, 'MM/DD/YYYY').subtract(29, 'days'), moment()],
    'Last 3 Available Months': [moment(dataEndDate, 'MM/DD/YYYY').subtract(3, 'months'), moment()],
    'Last Available Year': [moment(dataEndDate, 'MM/DD/YYYY').subtract(1, 'years'), moment()]
}

var last30Days = moment(dataEndDate, 'MM/DD/YYYY').subtract(30, "days").format("MM/DD/YYYY") + " - " + moment(dataEndDate, 'MM/DD/YYYY').format("MM/DD/YYYY")

function invalidDate(date) {
    for (var i = 0; i < disabledRanges.length; i++) {
        if (date >= moment(disabledRanges[i].start) && date <= moment(disabledRanges[i].end)) {
            return true;
        }
    }
    return false;
}


function setUpDatePicker(id) {
    $(id).daterangepicker({
        isInvalidDate: invalidDate,
        minDate: dataStartDate,
        maxDate: dataEndDate,
        ranges: premadeRanges,
    }).on('apply.daterangepicker', function(ev, picker) {
        cacheInput(id.slice(4), $(id)[0].value)
      });
}


function containsOutage(range) {
    const [startStr, endStr] = range.split(' - ')
    const startDate = new Date(startStr)
    const endDate = new Date(endStr)

    for (const outage of outageList) {
        const outageStartDate = new Date(outage.startDate)
        const outageEndDate = new Date(outage.endDate)

        if (startDate <= outageEndDate && outageStartDate <= endDate) {
          return true
        }
      }

      return false
}



// set up the time selector to only display time
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
}).on('apply.daterangepicker', function(ev, picker) {
    cacheInput("temperatureProfileTimeSelector", $("#id_temperatureProfileTimeSelector")[0].value)

});



$("#id_tempVsTimeDateRange").daterangepicker({
    isInvalidDate: invalidDate,
    minDate: dataStartDate,
    maxDate: dataEndDate,
    ranges: premadeRanges,
}).on('apply.daterangepicker', function(ev, picker) {
    var fieldValue = $("#id_tempVsTimeDateRange")[0].value
    cacheInput("#id_tempVsTimeDateRange", fieldValue)

    if (containsOutage(fieldValue)) {
        $("#tempVsTime_warning")[0].style.display = "block"
    }
    else {
        $("#tempVsTime_warning")[0].style.display = "none"
    }
});
$("#id_tempVsTimeDateRange").value = last30Days



$("#id_temperatureProfileDateRange").daterangepicker({
    isInvalidDate: invalidDate,
    minDate: dataStartDate,
    maxDate: dataEndDate,
    ranges: premadeRanges,
}).on('apply.daterangepicker', function(ev, picker) {
    var fieldValue = $("#id_temperatureProfileDateRange")[0].value
    cacheInput("temperatureProfileDateRange", fieldValue)

    if (containsOutage(fieldValue)) {
        $("#temperatureProfile_warning")[0].style.display = "block"
    }
    else {
        $("#temperatureProfile_warning")[0].style.display = "none"
    }
});
$("#id_temperatureProfileDateRange").value = last30Days



$('#id_temperatureProfileTimeSelector').value = "12:00 AM";




// this is for temp vs depth, which was cut
// $('#id_tempVsDepthTimestamp').value = dataEndDate;
// $('#id_tempVsDepthTimestamp').daterangepicker({
//     singleDatePicker: true,
//     minDate: dataStartDate,
//     maxDate: dataEndDate,
//     isInvalidDate: invalidDate
// }).on('apply.daterangepicker', function(ev, picker) {
//     cacheInput("tempVsDepthTimestamp", $("#id_tempVsDepthTimestamp")[0].value)
//   });
