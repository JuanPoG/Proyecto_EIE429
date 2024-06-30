document.addEventListener('DOMContentLoaded', function () {
    var ctx = document.getElementById('realtimeChart').getContext('2d');
    var realtimeChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [], // Timestamps
            datasets: [{
                label: ' Real Time Air quality over Time',
                borderColor: 'rgb(255, 99, 132)',
                data: []
            }]
        },
        options: {
            animation: false,
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'millisecond', // Change the unit to millisecond
                        tooltipFormat: 'HH:mm:ss.SSS', // Include milliseconds in the tooltip
                        displayFormats: {
                            millisecond: 'HH:mm:ss.SSS' // Display format for milliseconds
                        }
                    },
                    title: {
                        display: true,
                        text: 'Time'
                    }
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'CO2 [ppm]'
                    }
                }
            }
        }
    });

    var websocket = new WebSocket('ws://localhost:8765');
    websocket.onmessage = function (event) {
        var data = JSON.parse(event.data);
        var time = data.Tiempo;
        var ch1 = data.CH1;
      

        // Ensure all arrays are properly aligned and have data
        if (time && ch1  && time.length === ch1.length ) {
            for (let i = 0; i < ch1.length; i++) {
                if (realtimeChart.data.labels.length > 500) { // Limit data points for performance
                    realtimeChart.data.labels.shift();
                    realtimeChart.data.datasets[0].data.shift();
                    
                }

                // Add each data point to the chart
                realtimeChart.data.labels.push(time[i]);
                realtimeChart.data.datasets[0].data.push(ch1[i]);
                
            }
            realtimeChart.update(); // Update the chart after adding all new data points
        }
    };

    websocket.onerror = function (event) {
        console.error('WebSocket error:', event);
    };

    websocket.onclose = function (event) {
        console.log('WebSocket connection closed:', event);
    };
});