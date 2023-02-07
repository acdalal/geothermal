
const $chart = document.getElementById('ctx')

const drawHorizontalLine = {
    id: 'verticalLiner',
    afterInit: (chart, args, opts) => {
      chart.horizontalLiner = {}
    },
    afterEvent: (chart, args, options) => {
        const {inChartArea} = args
        chart.horizontalLiner = {draw: inChartArea}
    },
    beforeTooltipDraw: (chart, args, options) => {
        const {draw} = chart.horizontalLiner

        if (!draw) return false

        const {ctx} = chart
        const {top, bottom, left, right} = chart.chartArea
        const {tooltip} = args
        const y = tooltip?.caretY
        if (!y) return false

        ctx.save()

        ctx.beginPath()
        ctx.moveTo(left, y)
        ctx.lineTo(right, y)
        ctx.stroke()

        ctx.restore()
        return false
    }
}

const fillChart = {
    id: 'customCanvasBackgroundColor',
    beforeDraw: (chart, args, options) => {
      const {ctx} = chart;
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

// const colors = ["rgb(108, 113, 15)", "rgb(242, 137, 219)", "rgb(22, 110, 109)", "rgb(175, 217, 203)",
//                 "rgb(71, 29, 242)", "rgb(20, 199, 97)", "rgb(223, 106, 138)", "rgb(241, 206, 178)",
//                 "rgb(241, 0, 35)", "rgb(6, 56, 41)", "rgb(250, 100, 91)", "rgb(187, 118, 30)",
//                 "rgb(51, 77, 161)", "rgb(168, 98, 94)", "rgb(102, 60, 151)", "rgb(43, 239, 57)",
//                 "rgb(254, 108, 176)", "rgb(239, 186, 217)", "rgb(194, 48, 145)", "rgb(216, 247, 136)",
//                 "rgb(145, 195, 247)", "rgb(185, 82, 187)", "rgb(156, 0, 132)", "rgb(186, 165, 35)"]

var blue = 200
var green = 50
var diff = 200 / (Object.keys(graphData).length)
Object.keys(graphData).forEach(group => {
    datasetIndicesForEachWeek[group] = []

    Object.keys(graphData[group]).forEach(line => {
        datasetIndicesForEachWeek[group].push(datasetIndex)
        datasetIndex += 1

        let label = group
        if (groups.includes(group)) {
            label += line
        }
        else {
            groups.push(group)
        }
        let lineData = {
            data: graphData[group][line],
            label: label,
            axis: 'y',
            //borderColor: colors[groupNumber],
            borderColor: "rgb(10,"+green+","+blue+")",
            //backgroundColor: colors[groupNumber]
            backgroundColor: "rgb(10,"+green+","+blue+")"
        }
        datasets.push(lineData)
    })
    //console.log(group, colors[groupNumber])
    green += diff
    blue -=diff

    groupNumber += 1
})

const data = {
  datasets: datasets
}

var depth = "_depth_" + queryData[0]['depth_m'];
var startDate = "_startDate_" + queryData[0]['datetime_utc'].slice(0, 11) // Cut off the timestamp
var endDate = "_endDate" + queryData[queryData.length - 1]['datetime_utc'].slice(0, 11) // Cut off the timestamp
const graphImageName = "geothermal_data"  + startDate + endDate + ".png";

const options = {
    type: 'line',
    data: data,
    options: {
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'Temperature, C'
                }
            },
            y: {
                type: 'linear',
                title: {
                    display: true,
                    text: 'Depth below ground, ft.'
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
            mode: 'y',
            intersect: false,
        },
        plugins: {
            verticalLiner: {},
            legend: {
                display: true,
                labels: {
                    filter: function(legendItem, data) {
                        let group = legendItem.text
                        // console.log(group, groups)
                        if (groups.includes(group)) {
                            return true
                        }
                        else {
                            return false
                        }
                    }
                },
                onClick: function(event, legendItem, legend) {
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
            onComplete: function(){
                window.downloadGraphImage = function(){
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
    plugins: [drawHorizontalLine, fillChart]
}

var chart = new Chart($chart, options);
