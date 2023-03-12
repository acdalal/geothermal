$('#light-mode').change(function() {
    cacheInput('mode', 'light')
    document.documentElement.className = "light"
    document.getElementById("logo-blue").style = "display:block;"
    document.getElementById("logo-white").style = "display:none;"
});


$('#dark-mode').change(function() {
    cacheInput('mode', 'dark')
    document.documentElement.className = "dark"
    document.getElementById("logo-white").style = "display:block;"
    document.getElementById("logo-blue").style = "display:none;"
});
