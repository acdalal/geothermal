function selectTab(formName) {
    var i, tablinks;

    tablinks = document.getElementsByClassName("form-container");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(
            " show active",
            ""
        );
    }

    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(formName).className += " show active";

    cacheInput("tab", formName);
}
