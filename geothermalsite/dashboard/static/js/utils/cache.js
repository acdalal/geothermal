function cacheInput(name, value) {
    localStorage.setItem(name, value)
}


function updateTempProfileForm() {
    // Update the temperature profile form

    let cachedValue = localStorage.getItem("tempProfileBoreholeNumber")
    if (cachedValue != null) {
        let borehole = document.getElementById("id_tempProfileBoreholeNumber")
        if (borehole != null) {
            borehole.value = cachedValue;
        }

    }

    cachedValue = localStorage.getItem("temperatureProfileDateRange")
    if (cachedValue != null) {
        let dateRange = document.getElementById("id_temperatureProfileDateRange")
        if (dateRange != null) {
            dateRange.value = cachedValue;
        }
    }

    cachedValue = localStorage.getItem("temperatureProfileTimeSelector")
    if (cachedValue != null) {
        let time = document.getElementById("id_temperatureProfileTimeSelector")
        if (time != null) {
            time.value = cachedValue;
        }
    }

    cachedValue = localStorage.getItem("tempProfileUnits")
    if (cachedValue != null) {
        let units = document.getElementById("id_tempProfileUnits_" + cachedValue)
        if (units != null) {
            units.checked = true
        }
    }

}

function updateTempVsTimeForm() {
    // Update the temperature vs time form

    let cachedValue = localStorage.getItem("tempVsTimeBoreholeNumber")
    if (cachedValue != null) {
        let borehole = document.getElementById("id_tempVsTimeBoreholeNumber")
        if (borehole != null) {
            borehole.value = cachedValue;
        }
    }

    cachedValue = localStorage.getItem("tempVsTimeDateRange")
    if (cachedValue != null) {
        let dateRange = document.getElementById("id_tempVsTimeDateRange")
        if (dateRange != null) {
            dateRange.value = cachedValue;
        }
    }

    cachedValue = localStorage.getItem("tempVsTimeDepth")
    if (cachedValue != null) {
        let depth = document.getElementById("id_tempVsTimeDepth")
        if (depth != null) {
            depth.value = cachedValue;
        }
    }

    cachedValue = localStorage.getItem("tempVsTimeUnits")
    if (cachedValue != null) {
        let units = document.getElementById("id_tempProfileUnits_" + cachedValue)
        if (units != null) {
            units.checked = true
        }
    }

}

function updateDisplayMode() {
    // update light/dark mode settings
    var cachedValue = localStorage.getItem("mode")
    if (cachedValue == "light") {
        document.getElementById("light-mode").click()
    }
    else {
        document.getElementById("dark-mode").click()
    }
}

// function updateTempVsDepthForm() {
//     // Update the temperature vs depth form

//     let cachedValue = localStorage.getItem("tempVsDepthBoreholeNumber")
//     if (cachedValue != null) {
//         let borehole = document.getElementById("id_tempVsDepthBoreholeNumber")
//         borehole.value = cachedValue;
//     }

//     cachedValue = localStorage.getItem("tempVsDepthDateRange")
//     if (cachedValue != null) {
//         let dateRange = document.getElementById("id_tempVsDepthDateRange")
//         dateRange.value = cachedValue;
//     }

//     cachedValue = localStorage.getItem("tempVsDepthTimeStamp")
//     if (cachedValue != null) {
//         let time = document.getElementById("id_tempVsDepthTimeStamp")
//         time.value = cachedValue;
//     }

//     cachedValue = localStorage.getItem("tempVsDepthUnits")
//     if (cachedValue != null) {
//         document.getElementById("id_tempVsDepthUnits_" + cachedValue).checked = true
//     }

// }

function displayOutageWarnings() {

    var fieldValue = $("#id_temperatureProfileDateRange")[0].value

    if (containsOutage(fieldValue)) {
        $("#temperatureProfile_warning")[0].style.display = "block"
    }
    else {
        $("#temperatureProfile_warning")[0].style.display = "none"
    }


    fieldValue = $("#id_tempVsTimeDateRange")[0].value

    if (containsOutage(fieldValue)) {
        $("#tempVsTime_warning")[0].style.display = "block"
    }
    else {
        $("#tempVsTime_warning")[0].style.display = "none"
    }

}

function restoreTab() {
    var tab = localStorage.getItem("tab")
    if (tab == "tempvstime") {
        if (document.getElementById("tempvstime-button") != null){
            document.getElementById("tempvstime-button").click()
        }
    }
}


function clearCache() {
    localStorage.clear()
}
