function cacheInput(name, value) {
    localStorage.setItem(name, value)
}


function updateTempProfileForm() {
    // Update the temperature profile form

    let cachedValue = localStorage.getItem("tempProfileBoreholeNumber")
    if (cachedValue != null) {
        let borehole = document.getElementById("id_tempProfileBoreholeNumber")
        borehole.value = cachedValue;
    }

    cachedValue = localStorage.getItem("temperatureProfileDateRange")
    if (cachedValue != null) {
        let dateRange = document.getElementById("id_temperatureProfileDateRange")
        dateRange.value = cachedValue;
    }

    cachedValue = localStorage.getItem("temperatureProfileTimeSelector")
    if (cachedValue != null) {
        let time = document.getElementById("id_temperatureProfileTimeSelector")
        time.value = cachedValue;
    }

    cachedValue = localStorage.getItem("tempProfileUnits")
    if (cachedValue != null) {
        document.getElementById("id_tempProfileUnits_" + cachedValue).checked = true
    }

}

function updateTempVsTimeForm() {
    // Update the temperature vs time form

    let cachedValue = localStorage.getItem("tempVsTimeBoreholeNumber")
    if (cachedValue != null) {
        let borehole = document.getElementById("id_tempVsTimeBoreholeNumber")
        borehole.value = cachedValue;
    }

    cachedValue = localStorage.getItem("tempVsTimeDateRange")
    if (cachedValue != null) {
        let dateRange = document.getElementById("id_tempVsTimeDateRange")
        dateRange.value = cachedValue;
    }

    cachedValue = localStorage.getItem("tempVsTimeDepth")
    if (cachedValue != null) {
        let depth = document.getElementById("id_tempVsTimeDepth")
        depth.value = cachedValue;
    }

    cachedValue = localStorage.getItem("tempVsTimeUnits")
    if (cachedValue != null) {
        document.getElementById("id_tempVsTimeUnits_" + cachedValue).checked = true
    }

}

function updateTempVsDepthForm() {
    // Update the temperature vs depth form

    let cachedValue = localStorage.getItem("tempVsDepthBoreholeNumber")
    if (cachedValue != null) {
        let borehole = document.getElementById("id_tempVsDepthBoreholeNumber")
        borehole.value = cachedValue;
    }

    cachedValue = localStorage.getItem("tempVsDepthDateRange")
    if (cachedValue != null) {
        let dateRange = document.getElementById("id_tempVsDepthDateRange")
        dateRange.value = cachedValue;
    }

    cachedValue = localStorage.getItem("tempVsDepthTimeStamp")
    if (cachedValue != null) {
        let time = document.getElementById("id_tempVsDepthTimeStamp")
        time.value = cachedValue;
    }

    cachedValue = localStorage.getItem("tempVsDepthUnits")
    if (cachedValue != null) {
        document.getElementById("id_tempVsDepthUnits_" + cachedValue).checked = true
    }

}

window.onload = function () {
    updateTempProfileForm()
    updateTempVsDepthForm()
    updateTempVsTimeForm()
}

function clearCache() {
    localStorage.clear()
}
