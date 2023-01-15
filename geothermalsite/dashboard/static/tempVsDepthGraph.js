console.log(series1)
var options = {
    series: {
        lines: { show: true },
        points: { show: true },
        hoverable: true,
        clickable: true
    },
    xaxis: {
        show: true,
        inverted: false,
        timezone: "browser",
        gridLines: true,
    },
    yaxis: {
        show: true,
        inverted: false,
        timezone: "browser",
        gridLines: true,
    }
};
console.log($.plot("#graph", series1, options));
