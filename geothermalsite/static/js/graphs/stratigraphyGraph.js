const $chart = document.getElementById('ctx')


const fillChart = {
    id: 'customCanvasBackgroundColor',
    beforeDraw: (chart, args, options) => {
        const { ctx } = chart;
        ctx.save();
        ctx.globalCompositeOperation = 'destination-over';
        ctx.fillStyle = options.color || '#ffffff';
        ctx.fillRect(0, 0, chart.width, chart.height);
        ctx.restore();
    }
};


var datasets = []
var groups = []
var datasetIndex = 0
var groupNumber = 0
var datasetIndicesForEachWeek = {}

let numGroups = Object.keys(graphData).length
var red = 0
var blue = 256
var diff = 256 / numGroups

Object.keys(graphData).forEach(group => {
    datasetIndicesForEachWeek[group] = []

    Object.keys(graphData[group]).forEach(line => {
        datasetIndicesForEachWeek[group].push(datasetIndex)
        datasetIndex += 1

        let label = group
        if (groups.includes(group)) {
            label += " "
        }
        else {
            groups.push(group)
        }
        let lineData = {
            data: graphData[group][line],
            label: label,
            axis: 'y',
            borderColor: "rgb(" + red + ",50," + blue + ")",
            backgroundColor: "rgb(" + red + ",50," + blue + ")",
        }

        datasets.push(lineData)
    })
    blue -= diff
    red += diff
    groupNumber += 1
})

const data = {
    datasets: datasets
}

var depth = "_depth_" + queryData[0]['depth_m'];
var startDate = "_startDate_" + queryData[0]['datetime_utc'].slice(0, 11) // Cut off the timestamp
var endDate = "_endDate" + queryData[queryData.length - 1]['datetime_utc'].slice(0, 11) // Cut off the timestamp
const graphImageName = "geothermal_data" + startDate + endDate + ".png";

var xLabel = "Temperature"
var yLabel = "Depth Below Ground"

if (units == 0) {
    xLabel += ', °C'
    yLabel += ', m'
}
else {
    xLabel += ', F'
    yLabel += ', ft'
}

const options = {
    type: 'line',
    data: data,
    options: {
        scales: {
            x: {
                title: {
                    display: true,
                    text: xLabel
                }
            },
            y: {
                type: 'linear',
                title: {
                    display: true,
                    text: yLabel
                },
                reverse: true
            }
        },
        spanGaps: true,
        elements: {
            point: {
                radius: 0
            }
        },
        interaction: {
            mode: 'nearest',
            intersect: false,
        },
        plugins: {
            verticalLiner: {},
            legend: {
                display: true,
                labels: {
                    filter: function (legendItem, data) {
                        let group = legendItem.text

                        if (groups.includes(group)) {
                            return true
                        }
                        else {
                            return false
                        }
                    }
                },
                onClick: function (event, legendItem, legend) {
                    let group = legendItem.text
                    let chart = legend.chart
                    legendItem.hidden = true
                    datasetIndicesForEachWeek[group].forEach(index => {
                        let meta = chart.getDatasetMeta(index)
                        meta.hidden = meta.hidden === null ? !chart.data.datasets[index].hidden : null
                    })
                    chart.update()
                }
            }
        },
        indexAxis: 'y',
        animation: {
            onComplete: function () {
                window.downloadGraphImage = function () {
                    var image = chart.toBase64Image()
                    const a = document.createElement('a')
                    a.href = image
                    a.download = graphImageName
                    document.body.appendChild(a)
                    a.click()
                    document.body.removeChild(a)
                };
            },
            duration: 0
        },
        pointRadius: 0,
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 1,
    },
    plugins: [fillChart]
}

var chart = new Chart($chart, options);

document.getElementById("ctx").scrollIntoView();
