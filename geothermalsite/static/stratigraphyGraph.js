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
        const x = tooltip?.caretX
        if (!x) return

        ctx.save()

        ctx.beginPath()
        ctx.moveTo(x, left)
        ctx.lineTo(x, right)
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
var lineData = {}
Object.keys(graphData).forEach(group => {
    console.log(group)
    Object.keys(graphData[group]).forEach(line => {
        lineData = {
            data: graphData[group][line],
            label: group + ' ' + line,
            axis: 'y'
        }
        datasets.push(lineData)
    })
})
console.log(datasets)
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
        interaction: {
            mode: 'index',
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
