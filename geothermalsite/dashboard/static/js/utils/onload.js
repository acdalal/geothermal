
window.onload = function () {
    restoreTab()
    updateTempProfileForm()
    // updateTempVsDepthForm()
    updateTempVsTimeForm()

    // check for outages in user input
    var field = $("#id_temperatureProfileDateRange")[0]
    if (field != null) {
        var fieldValue = field.value

        if (containsOutage(fieldValue)) {
            $("#temperatureProfile_warning")[0].style.display = "block"
        }
        else {
            $("#temperatureProfile_warning")[0].style.display = "none"
        }

    }

    field = $("#id_tempVsTimeDateRange")[0]
    if (field != null) {
        var fieldValue = $("#id_tempVsTimeDateRange")[0].value

        if (containsOutage(fieldValue)) {
            $("#tempVsTime_warning")[0].style.display = "block"
        }
        else {
            $("#tempVsTime_warning")[0].style.display = "none"
        }
    }
    updateDisplayMode()
}
