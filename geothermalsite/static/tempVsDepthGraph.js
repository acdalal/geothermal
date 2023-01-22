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
  datasets: [{
    data: graphData,
  }]
}

const options = {
  type: 'line',
  data,
  options: {
    label: "Temperature vs Depth Graph",
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
