var ctx = document.getElementById("tempvstimegraph").getContext("2d");

var myChart = new Chart(ctx, {
  type: 'line',
  options: {
    scales: {
      xAxes: [{
        type: 'time',
      }]
    },
    legend: {
        onClick: null
    }
  },
  data: {
    labels: labels,
    datasets: [{
      label: 'Temperature vs Time',
      data: data,
      backgroundColor: 'rgba(255, 99, 132, 0.2)',
      borderColor: 'rgba(255, 99, 132, 1)',
      borderWidth: 1,
      pointRadius: 0  // this will remove the circles on data points
    }]
  }
});
