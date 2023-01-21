var ctx = document.getElementById("tempvsdepthgraph").getContext("2d");

var myChart = new Chart(ctx, {
  type: 'line',
  options: {
    legend: {
        onClick: null
    }
  },
  data: {
    labels: labels,
    datasets: [{
      label: 'Temperature vs Depth down the borehole',
      data: data,
      backgroundColor: 'rgba(255, 99, 132, 0.2)',
      borderColor: 'rgba(255, 99, 132, 1)',
      borderWidth: 1,
      pointRadius: 0
    }]
  }
});
