function toLightMode() {
    cacheInput('mode', 'light')
    document.documentElement.className = "light"
    document.getElementById("logo-blue").style = "display:block;"
    document.getElementById("logo-white").style = "display:none;"
}

function toDarkMode() {
    cacheInput('mode', 'dark')
    document.documentElement.className = "dark"
    document.getElementById("logo-white").style = "display:block;"
    document.getElementById("logo-blue").style = "display:none;"
}


$('#switch').change(function() {
    let checkbox = document.getElementById('switch')
    if (checkbox != null) {
        if (checkbox.checked) {
            toDarkMode()
        }
        else {
            toLightMode()
        }
    }
})


$('#switch-button').click(function() {
    console.log("hi")
    $('#switch').trigger('click')
})
