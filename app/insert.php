<?php
// Enable error reporting
ini_set('display_errors', 1);
error_reporting(E_ALL);

// Read incoming JSON
$data = json_decode(file_get_contents("php://input"), true);

// Extract values safely
$timestamp = $data['timestamp'] ?? null;
$ph = $data['ph_value'] ?? null;
$tds = $data['tds_ppm'] ?? null;
$water_temp = $data['water_temp_c'] ?? null;
$air_temp = $data['air_temp_c'] ?? null;
$humidity = $data['humidity_percent'] ?? null;
$pressure = $data['air_pressure_hpa'] ?? null;

// Validate timestamp
if ($timestamp === null) {
    echo json_encode(["status" => "error", "message" => "Missing timestamp"]);
    exit;
}

// Connect to DB
$host = 'localhost';
$dbname = 'db1113357-hydro';
$user = 'db1113357-hydro';
$pass = 'jEZkF}<(MJ{<<LJQmz(A';

try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname;charset=utf8mb4", $user, $pass);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    $stmt = $pdo->prepare("
        INSERT INTO sensor_data
        (timestamp, ph_value, tds_ppm, water_temp_c, air_temp_c, humidity_percent, air_pressure_hpa)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ");

    $stmt->execute([
        $timestamp, $ph, $tds, $water_temp, $air_temp, $humidity, $pressure
    ]);

    echo json_encode(["status" => "success"]);
} catch (PDOException $e) {
    echo json_encode(["status" => "error", "message" => $e->getMessage()]);
}
?>