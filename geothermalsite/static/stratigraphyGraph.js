
const $chart = document.getElementById('ctx')
const colors = ["#DFC397", "#F0E6E7","#E6E9EE","#839784","#3A473B"]
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
<<<<<<< HEAD
var lineData = {}
var count = 0
=======
var groups = []
var datasetIndex = 0
var groupNumber = 0
var datasetIndicesForEachWeek = {}

// 15 colors to dynamically assign to datasets, taken from https://sashamaps.net/docs/resources/20-colors/
// const colors = ['rgba(255, 230, 25, 75)', 'rgba(255, 60, 180, 75)', 'rgba(255, 0, 130, 200)', 'rgba(255, 245, 130, 48)', 'rgba(255, 145, 30, 180)', 'rgba(255, 70, 240, 240)', 'rgba(255, 240, 50, 230)', 'rgba(255, 210, 245, 60)', 'rgba(255, 220, 190, 255)', 'rgba(255, 170, 110, 40)', 'rgba(255, 128, 0, 0)', 'rgba(255, 128, 128, 0)', 'rgba(255, 255, 215, 180)', 'rgba(255, 0, 0, 128)', 'rgba(255, 0, 0, 0)']
const colors = ["rgba(255,0,0,1)", "rgba(0,255,0,1)", "rgba(0,0,255,1)", "rgba(255,128,0,1)", "rgba(255,0,128,1)", "rgba(0,255,128,1)", "rgba(128,255,0,1)", "rgba(0,128,255,1)", "rgba(128,0,255,1)", "rgba(255,0,255,1)", "rgba(255,255,0,1)", "rgba(0,255,255,1)", "rgba(255,128,128,1)", "rgba(128,255,128,1)", "rgba(128,128,255,1)", "rgba(0,0,128,1)", "rgba(128,0,0,1)", "rgba(0,128,0,1)", "rgba(192,192,192,1)", "rgba(128,128,128,1)", "rgba(64,64,64,1)", "rgba(255,165,0,1)", "rgba(173,255,47,1)", "rgba(255,20,147,1)"]

>>>>>>> d352d70332f628af15e0333a2e58dc11de15def8
Object.keys(graphData).forEach(group => {
    Object.keys(graphData[group]).forEach(line => {
        lineData = {
            data: graphData[group][line],
            label: group,
            axis: 'y',
            backgroundColor: colors[count%5],
            borderColor: colors[count%5]
        }
        count += 1
        datasets.push(lineData)
    })
<<<<<<< HEAD
=======
    // console.log(groupNumber, colors[groupNumber])

    groupNumber += 1
>>>>>>> d352d70332f628af15e0333a2e58dc11de15def8
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
        legend: {
            onClick: null
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
            verticalLiner: {}
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
            }
        },
        pointRadius: 0,
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 1,
    },
    plugins: [drawHorizontalLine, fillChart]
}

var chart = new Chart($chart, options);
