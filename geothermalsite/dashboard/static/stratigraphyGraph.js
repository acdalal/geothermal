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

        if (!draw) return

        const {ctx} = chart
        const {top, bottom, left, right} = chart.chartArea
        const {tooltip} = args
        const y = tooltip?.caretY
        if (!y) return

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
var groupNumber = 0

// 15 colors to dynamically assign to datasets, taken from https://sashamaps.net/docs/resources/20-colors/
const colors = ['rgba(255, 230, 25, 75)', 'rgba(255, 60, 180, 75)', 'rgba(255, 0, 130, 200)', 'rgba(255, 245, 130, 48)', 'rgba(255, 145, 30, 180)', 'rgba(255, 70, 240, 240)', 'rgba(255, 240, 50, 230)', 'rgba(255, 210, 245, 60)', 'rgba(255, 220, 190, 255)', 'rgba(255, 170, 110, 40)', 'rgba(255, 128, 0, 0)', 'rgba(255, 128, 128, 0)', 'rgba(255, 255, 215, 180)', 'rgba(255, 0, 0, 128)', 'rgba(255, 0, 0, 0)']

Object.keys(graphData).forEach(group => {

    Object.keys(graphData[group]).forEach(line => {
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
            borderColor: colors[groupNumber]
        }
        datasets.push(lineData)
    })

    groupNumber += 1
})

const data = {
  datasets: datasets
}
console.log(data)

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
