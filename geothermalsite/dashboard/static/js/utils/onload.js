
window.onload = function () {
    updateTempProfileForm()
    // updateTempVsDepthForm()
    updateTempVsTimeForm()


    var fieldValue = $("#id_temperatureProfileDateRange")[0].value

    if (containsOutage(fieldValue)) {
        console.log("success")
        $("#temperatureProfile_warning")[0].style.display = "block"
    }
    else {
        $("#temperatureProfile_warning")[0].style.display = "none"
    }


    var fieldValue = $("#id_tempVsTimeDateRange")[0].value

    if (containsOutage(fieldValue)) {
        $("#tempVsTime_warning")[0].style.display = "block"
    }
    else {
        $("#tempVsTime_warning")[0].style.display = "none"
    }

    updateDisplayMode()
}
