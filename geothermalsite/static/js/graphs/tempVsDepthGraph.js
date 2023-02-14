const $chart = document.getElementById('ctx')

const drawVerticalLine = {
    id: 'verticalLiner',
    afterInit: (chart, args, opts) => {
      chart.verticalLiner = {}
    },
    afterEvent: (chart, args, options) => {
        const {inChartArea} = args
        chart.verticalLiner = {draw: inChartArea}
    },
    beforeTooltipDraw: (chart, args, options) => {
        const {draw} = chart.verticalLiner
        if (!draw) return

        const {ctx} = chart
        const {top, bottom} = chart.chartArea
        const {tooltip} = args
        const x = tooltip?.caretX
        if (!x) return

        ctx.save()

        ctx.beginPath()
        ctx.moveTo(x, top)
        ctx.lineTo(x, bottom)
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

const data = {
  datasets: [{
    data: graphData,
    label: "Temperature vs Depth Graph"
}]
}

var depth = "_depth_" + queryData[0]['depth_m'];
var startDate = "_startDate_" + queryData[0]['datetime_utc'].slice(0, 11) // Cut off the timestamp
var endDate = "_endDate" + queryData[queryData.length - 1]['datetime_utc'].slice(0, 11) // Cut off the timestamp
const graphImageName = "geothermal_data"  + startDate + endDate + ".png";

const options = {
  type: 'line',
  data,
  options: {
    label: "Temperature vs Depth Graph",
    legend: {
        onClick: null
    },
    interaction: {
        mode: 'index',
        intersect: false,
    },
    plugins: {
        verticalLiner: {},
        legend: {
          display: true,
          onClick: function(event, legendItem, legend) {
            return
          }
        }
    },
    scales: {
      x: {
        type: 'linear',
        title: {
            display: true,
            text: 'Depth below ground, m'
        }
      },
      y: {
        title: {
            display: true,
            text: 'Temperature, C'
        }
      }
    },
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
plugins: [drawVerticalLine, fillChart]
}

const chart = new Chart($chart, options)
