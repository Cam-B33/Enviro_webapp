
<?php
// data_API.php


// Paths to the JSON and GeoJSON files
$jsonFilePath = '/home/cameron/Documents/gis-edna-app/data/serve_to_frontend/processed_data.json';
$geoJsonFilePath = '/home/cameron/Documents/gis-edna-app/data/shapefiles/Michigan_Dam_Inventory.geojson';

$response = array();

// Add JSON data to the response
if (file_exists($jsonFilePath)) {
    $jsonData = json_decode(file_get_contents($jsonFilePath), true);
    $response['jsonData'] = $jsonData;
} else {
    $response['jsonDataError'] = 'JSON file not found';
}

// Add GeoJSON data to the response
if (file_exists($geoJsonFilePath)) {
    $geoJsonData = json_decode(file_get_contents($geoJsonFilePath), true);
    $response['geoJsonData'] = $geoJsonData;
} else {
    $response['geoJsonDataError'] = 'GeoJSON file not found';
}

// Set header to indicate JSON content and output the combined response
header('Content-Type: application/json');
echo json_encode($response);
?>


