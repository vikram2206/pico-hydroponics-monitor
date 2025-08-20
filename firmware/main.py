import network
import time
import urequests

from rtc_clock import seconds_since_2000
from bme_reader import read_bme280
from ph_reader import read_ph_value
from tds_reader import read_tds_value
from water_temp_reader import read_water_temp

# --- Wi-Fi Credentials ---
SSID = "HAW-WLAN"
PASSWORD = "VXAD-uk73-E3TL-u37g"

# --- Connect to Wi-Fi ---
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
print(f"🔌 Connecting to Wi-Fi network: {SSID}...")
wlan.connect(SSID, PASSWORD)

max_wait = 10
while max_wait > 0:
    if wlan.isconnected():
        break
    print(".", end="")
    time.sleep(1)
    max_wait -= 1

print("\n")
if wlan.isconnected():
    print("✅ Connected to Wi-Fi!")
    print("📡 IP address:", wlan.ifconfig()[0])
else:
    print("❌ Failed to connect to Wi-Fi.")
    raise SystemExit

# --- Remote Server URL ---
url = "https://vasist.rrhess.de/insert.php"

# --- Main Loop: Send Data Every 180 Seconds ---
while True:
    print("\n📡 Measuring and sending sensor data...")

    try:
        # Timestamp from RTC
        timestamp = seconds_since_2000()

        # Read all sensors
        ph = read_ph_value()
        tds = read_tds_value()
        water_temp = read_water_temp()
        bme_data = read_bme280()

        # Combine everything into one payload
        data = {
            "timestamp": int(timestamp),
            "ph_value": ph,
            "tds_ppm": int(tds),
            "water_temp_c": water_temp,
            "air_temp_c": bme_data["air_temp_c"],
            "humidity_percent": bme_data["humidity_percent"],
            #"air_pressure_hpa": bme_data["air_pressure_hpa"]
        }

        print("📦 Data to send:", data)

        # Send to server
        res = urequests.post(url, json=data)
        print("✅ Server responded:", res.text)

    except Exception as e:
        print("❌ Error:", e)

    print("⏳ Waiting 180 seconds...\n")
    time.sleep(120)