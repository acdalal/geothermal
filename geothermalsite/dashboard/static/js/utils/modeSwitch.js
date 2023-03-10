$('#light-mode').change(function() {
    cacheInput('mode', 'light')
    document.documentElement.className = "light"
});


$('#dark-mode').change(function() {
    cacheInput('mode', 'dark')
    document.documentElement.className = "dark"
});
