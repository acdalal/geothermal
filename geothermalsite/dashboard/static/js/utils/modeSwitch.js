$('#light-mode').change(function() {
});


$('#dark-mode').change(function() {
});


$('#switch').change(function() {
    let checkbox = document.getElementById('switch')
    if (checkbox != null) {
        if (checkbox.checked) {
            cacheInput('mode', 'dark')
            document.documentElement.className = "dark"
            document.getElementById("logo-white").style = "display:block;"
            document.getElementById("logo-blue").style = "display:none;"
        }
        else {
            cacheInput('mode', 'light')
            document.documentElement.className = "light"
            document.getElementById("logo-blue").style = "display:block;"
            document.getElementById("logo-white").style = "display:none;"
        }
    }
})
