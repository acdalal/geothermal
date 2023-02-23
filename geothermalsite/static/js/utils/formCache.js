function cacheInput(e) {
    localStorage.setItem(e.attributes["name"].value, e.value)
}

function fillFormWithCache(id) {
    let form = document.getElementById(id);

    let inputs = form.children;
    for (let i = 0; i < inputs.length; i++) {
        let el = inputs[i];
        let cachedVal = localStorage.getItem(el.attributes["name"].value)
        if (cachedVal != null) {
            el.value = cachedVal;
        }
    }
}

window.onload = function () {
    fillFormWithCache("tempprofileform")
    fillFormWithCache("tempvstimeform")
    fillFormWithCache("tempvsdepthform")
}

function clearCache() {
    localStorage.clear()
}
