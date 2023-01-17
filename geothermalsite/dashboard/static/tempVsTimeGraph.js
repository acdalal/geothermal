var options = {
    series: {
        lines: { show: true },
        points: { show: true },
        hoverable: true,
        clickable: true
    },
    xaxis: {
        show: true,
        mode: "time",
        inverted: false,
        timezone: "browser",
        gridLines: true,
        timeformat: "%Y-%m-%d %H:%M:%S"
    },
    yaxis: {
        show: true,
        inverted: false,
        timezone: "browser",
        gridLines: true,
    }
};

plot = $.plot("#graph", series1, options);
console.log(plot);
var myCanvas = plot.getCanvas();
var image = myCanvas.toDataURL();
image = image.replace("image/png","image/octet-stream");
document.location.href=image;
