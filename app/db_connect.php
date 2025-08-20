<?php
// Enable full error reporting
ini_set('display_errors', 1);
error_reporting(E_ALL);

function load_data() {
    //echo "=== HostEurope MySQL Connection Test (PDO) ===\n";

    // Connection parameters
    $host = 'localhost'; 
    $port = 3306;
    $dbname = 'DB_Name';
    $user = 'DB_USER';
    $pass = 'DB_PASS';

    try {
        // Create PDO connection
        $dsn = "mysql:host=$host;port=$port;dbname=$dbname;charset=utf8mb4";
        $pdo = new PDO($dsn, $user, $pass, [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION
        ]);

        //echo "✓ Connected to MySQL successfully\n";

        // Test query - adjust table name if needed
        $query = "SELECT * FROM hydro_sensor2 LIMIT 1000";
        $stmt = $pdo->query($query);

        if (!$stmt) {
            throw new Exception("Query failed to execute");
        }

        $rows = $stmt->fetchAll(PDO::FETCH_ASSOC);

        //echo "✓ Query executed successfully. Rows returned: " . count($rows) . "\n";
        return $rows;

    } catch (PDOException $e) {
       // echo "✗ PDO Exception: " . $e->getMessage() . "\n";
        return [];
    } catch (Exception $e) {
        // echo "✗ General Exception: " . $e->getMessage() . "\n";
        return [];
    }
}

// Call the function for testing
//$data = load_data();
//print_r($data); // For development: show fetched data
?>
