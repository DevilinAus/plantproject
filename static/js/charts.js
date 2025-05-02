var ctx = document.getElementById("chart").getContext("2d");
var chart = new Chart(ctx, {
  type: "line",
  data: {
    labels: ["2025-05-01 10:00", "2025-05-01 11:00", "2025-05-01 12:00"],
    datasets: [
      {
        label: "Moisture Reading",
        data: [30, 35, 28],
        fill: false,
        borderColor: "rgb(75, 192, 192)",
        // TODO - DEFINE A CUSTOM COLOUR WHEN NOT USING CDN

        tension: 0.1,
      },
    ],
  },
  options: {
    responsive: false,
  },
});

//Listen for button click || async allows me to use await in the function, so the code
// keeps running whilst it waits for a reply. (website doesn't freeze etc)
document
  .getElementById("btn-1day")
  .addEventListener("click", async function () {
    const chartData = await fetchData("1d");

    updateChart(chartData);
  });

document
  .getElementById("btn-1week")
  .addEventListener("click", async function () {
    const chartData = await fetchData("1w");

    updateChart(chartData);
  });

document
  .getElementById("btn-1month")
  .addEventListener("click", async function () {
    const chartData = await fetchData("1m");

    updateChart(chartData);
  });

async function fetchData(timeframe) {
  const response = await fetch(`/api/readings?timeframe=${timeframe}`, {
    method: "GET",
    // headers: {
    //     'Content-Type': 'application/json',
    // },
    // body: JSON.stringify({ "timeframe": timeframe })
  });

  // Error handling - check if the respone is good, if not exit function and write to console
  if (!response.ok) {
    console.error("Failed to fetch chart data.");
    throw new Error("Response not okay" + response.statusText);
  }

  // Set the response to ChartData when it arrives
  return await response.json();
}

function updateChart(chartData) {
  // update the chart with the fresh data
  chart.data.labels = chartData.labels;
  chart.data.datasets[0].data = chartData.values;
  chart.update();
}
