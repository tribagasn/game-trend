document.addEventListener("DOMContentLoaded", function () {
  fetch("data/trend_game_data.csv")
    .then((response) => response.text())
    .then((csvData) => {
      const parsedData = parseCSV(csvData);
      renderChart(parsedData);
    })
    .catch((error) => console.error("Error loading the CSV file: ", error));
});

/*************  ✨ Windsurf Command ⭐  *************/
/**
 * Parse a CSV string containing trend data into an object.
 *
 * @param {string} csvData - The CSV string to be parsed.
 * @returns {Object} An object with the following properties:
 *  - dates: An array of dates for the trend data.
 *  - mobileLegends: An array of numbers representing the popularity trend of
 *    Mobile Legends.
 *  - pubgMobile: An array of numbers representing the popularity trend of
 *    PUBG Mobile.
 *  - residentEvil: An array of numbers representing the popularity trend of
 *    Resident Evil.
 */
/*******  4d5c12f1-6278-4de1-81dc-fa3854e908b5  *******/ function parseCSV(
  csvData
) {
  const lines = csvData.split("\n");
  const headers = lines[0].split(",");
  const dates = [];
  const mobileLegends = [];
  const pubgMobile = [];
  const residentEvil = [];

  for (let i = 1; i < lines.length; i++) {
    const row = lines[i].split(",");
    if (row.length === headers.length) {
      dates.push(row[0]);
      mobileLegends.push(row[1]);
      pubgMobile.push(row[2]);
      residentEvil.push(row[3]);
    }
  }

  return {
    dates,
    mobileLegends,
    pubgMobile,
    residentEvil,
  };
}

function renderChart(data) {
  const ctx = document.getElementById("trendChart").getContext("2d");
  const trendChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: data.dates,
      datasets: [
        {
          label: "Mobile Legends",
          data: data.mobileLegends,
          borderColor: "blue",
          fill: false,
        },
        {
          label: "PUBG Mobile",
          data: data.pubgMobile,
          borderColor: "green",
          fill: false,
        },
        {
          label: "Resident Evil Village",
          data: data.residentEvil,
          borderColor: "red",
          fill: false,
        },
      ],
    },
    options: {
      responsive: true,
      scales: {
        x: {
          ticks: {
            autoSkip: true,
            maxTicksLimit: 10,
          },
        },
        y: {
          beginAtZero: true,
        },
      },
    },
  });
}
