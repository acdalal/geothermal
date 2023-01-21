// var ctx = document.getElementById("ctx").getContext("2d");
// Chart.defaults.LineWithLine = Chart.defaults.line;
// Chart.controllers.LineWithLine = Chart.controllers.line.extend({
//    draw: function(ease) {
//       Chart.controllers.line.prototype.draw.call(this, ease);

//       if (this.chart.tooltip._active && this.chart.tooltip._active.length) {
//          var activePoint = this.chart.tooltip._active[0],
//              ctx = this.chart.ctx,
//              x = activePoint.tooltipPosition().x,
//              topY = this.chart.legend.bottom,
//              bottomY = this.chart.chartArea.bottom;

//          // draw line
//          ctx.save();
//          ctx.beginPath();
//          ctx.moveTo(x, topY);
//          ctx.lineTo(x, bottomY);
//          ctx.lineWidth = 2;
//          ctx.strokeStyle = '#07C';
//          ctx.stroke();
//          ctx.restore();
//       }
//    }
// });
// var myChart = new Chart(ctx, {
//   type: 'line',
//   options: {
//     scales: {
//       xAxes: [{
//         type: 'time',
//       }]
//     },
//     legend: {
//         onClick: null
//     }
//   },
//   data: {
//     labels: labels,
//     datasets: [{
//       label: 'Temperature vs Time',
//       data: data,
//       backgroundColor: 'rgba(255, 99, 132, 0.2)',
//       borderColor: 'rgba(255, 99, 132, 1)',
//       borderWidth: 1,
//       pointRadius: 0
//     }]
//   }
// });

const $chart = document.getElementById('ctx')

const plugin = {
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

const data = {
  labels: yData,
  datasets: [{
    data: xData
  }]
}

const options = {
  type: 'line',
  data,
  options: {
    interaction: {
      mode: 'index',
      intersect: false,
    },
    plugins: {
      verticalLiner: {}
    },
    pointRadius: 0,
    backgroundColor: 'rgba(255, 99, 132, 0.2)',
    borderColor: 'rgba(255, 99, 132, 1)',
    borderWidth: 1,
  },
  plugins: [plugin]
}

const chart = new Chart($chart, options)
