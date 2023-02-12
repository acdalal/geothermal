
$(function () {
    var disabledRanges = [];
    for (var i = 0; i < outageList.length; i++) {
        disabledRanges.push({ start: '{{ range.startDate }}', end: '{{ range.endDate }}' });
    }

    $('#id_dateRange').daterangepicker({
        isInvalidDate: function (date) {
            for (var i = 0; i < disabledRanges.length; i++) {
                if (date >= moment(disabledRanges[i].start) && date <= moment(disabledRanges[i].end)) {
                    return true;
                }
            }
            return false;
        },
        minDate: "{{ dataStartDate }}",
        maxDate: "{{ dataEndDate }}",
        ranges: {
            'Last 7 Available Days': [moment("{{ dataEndDate }}").subtract(6, 'days'), moment()],
            'Last 30 Available Days': [moment("{{ dataEndDate }}").subtract(29, 'days'), moment()],
            'Last 3 Available Months': [moment("{{ dataEndDate }}").subtract(3, 'months'), moment()],
            'Last Available Year': [moment("{{ dataEndDate }}").subtract(1, 'years'), moment()]
        },

    });
});

$('#id_timeSelector').daterangepicker({
    timePicker: true,
    singleDatePicker: true,
    timePickerIncrement: 1,
    timePickerSeconds: false,
    locale: {
        format: 'hh:mm A'
    }
}).on('show.daterangepicker', function (ev, picker) {
    picker.container.find(".calendar-table").hide();
});
$(document).ready(function () {
    $("button").click(function () {
        $(document).scrollTop($(document).height());
    });
});
