// 
// Initialize the map
var defaultLatitude = 46.5; // Set a default latitude
var defaultLongitude = -84.2; // Set a default longitude
var defaultZoom = 7; // Set a default zoom level

var map = L.map('map').setView([defaultLatitude, defaultLongitude], defaultZoom);

// Add OpenStreetMap tiles
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap contributors'
}).addTo(map);
// Determine the color based on cumulative strength

function getColorForStrength(strength) {
    if (strength <= 2) return '#00ff00'; // Light green for very low strength
    if (strength <= 4) return '#40ff00'; // Slightly stronger green
    if (strength <= 6) return '#80ff00'; // Moderate green
    if (strength <= 8) return '#c0ff00'; // Darker green
    if (strength <= 10) return '#ffff00'; // Yellow for medium strength
    if (strength <= 12) return '#ffc000'; // Orange-yellow
    if (strength <= 14) return '#ff8000'; // Light orange
    if (strength <= 16) return '#ff4000'; // Darker orange
    return '#ff0000'; // Red for high strength
}
// Fetch and display data from data_api.php
fetch('data_API.php')
    .then(response => response.json())
    .then(data => {
        // Process your regular JSON data
                if (data.jsonData) {
                    data.jsonData.forEach(item => {
                        if (item.station_lat && item.station_long) {
                            var strength = (Number(item.Sample_1) + Number(item.Sample_2) + Number(item.Sample_3));
                            var color = getColorForStrength(strength); // Store the color

                            var marker = L.circleMarker([item.station_lat, item.station_long], {
                                color: color, // Use the color for the marker
                                radius: 8 // You can adjust marker size as well
                            }).addTo(map);
                            marker.bindPopup(`Sampling Station: ${item.sampling_station}, Strength: ${strength}`);
                        }
                    });
                }

                // Add the GeoJSON layer to the map
                if (data.geoJsonData) {
                    var damLayer = L.geoJSON(data.geoJsonData, {
                        
                            // Define styles for point features (dams)
                            style: function (feature) {
                                return {
                                    radius: 2,
                                    fillColor: "#800080", // Purple color
                                    color: "#D107D1", // Border color
                                    weight: 1,
                                    opacity: 1,
                                    fillOpacity: 0.8
                                };
                            },
                        
                            pointToLayer: function (feature, latlng) {
                                // Use L.circleMarker to apply the defined style
                                return L.circleMarkerMarker(latlng);
                            },
                        
                            onEachFeature: function (feature, layer) {
                                if (feature.properties && feature.properties.DamName) {
                                    layer.bindPopup("Dam Name: " + feature.properties.DamName);
                                }
                            }
                        }).addTo(map);
                }
            })
            .catch(error => console.error('Error:', error));

        document.getElementById('slider').addEventListener('input', function(e) {
            var seasonLabel = document.getElementById('slider-label');
            var season = '';
            switch (e.target.value) {
                case '0':
                    season = 'Summer';
                    break;
                case '1':
                    season = 'Fall';
                    break;
                case '2':
                    season = 'Winter';
                    break;
            }
            seasonLabel.textContent = season;
        });
        document.getElementById('slider').addEventListener('input', function(e) {
            var seasonCode = '';
            switch (e.target.value) {
                case '0':
                    seasonCode = 'S';
                    break;
                case '1':
                    seasonCode = 'F';
                    break;
                case '2':
                    seasonCode = 'W';
                    break;
            }
            updateMapData(seasonCode);
        });


        // Add the legend (outside the loop)
        var legend = L.control({ position: 'topright' });
        legend.onAdd = function (map) {
    var div = L.DomUtil.create('div', 'info legend'),
        grades = [0, 3, 6, 9, 12, 15, 18], // Adjust according to getColorForStrength
        labels = [];

    for (var i = 0; i < grades.length; i++) {
        labels.push(
            '<i style="background:' + getColorForStrength(grades[i]) + '"></i> ' +
            grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] : '+'));
    }

    div.innerHTML = labels.join('<br>');
    return div;
};
legend.addTo(map);

// Define your GeoJSON layers
var geoJsonLayers = {
    "Dams": damLayer, // Your GeoJSON layer
    // Add more GeoJSON layers here
};

// Create a new control for the legend
var legendControl = L.control({ position: 'bottomright' });

legendControl.onAdd = function (map) {
    var div = L.DomUtil.create('div', 'info legend');

    // Loop through each GeoJSON layer and add its name to the legend
    for (var layerName in geoJsonLayers) {
        div.innerHTML += '<div><b>' + layerName + '</b></div>';
    }

    return div;
};

// Add the legend to the map
legendControl.addTo(map);

