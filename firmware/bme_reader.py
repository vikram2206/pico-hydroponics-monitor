from machine import Pin, I2C
import bme280_float as bme280

# Setup I2C for BME280 (bus 1, GP2 = SDA, GP3 = SCL)
i2c = I2C(1, scl=Pin(3), sda=Pin(2), freq=400000)
bme = bme280.BME280(i2c=i2c, address=0x76)

def read_bme280():
    """BME280 UNits"""
    temperature_c, pressure_pa, humidity_perc = bme.read_compensated_data()
    pressure_hpa = pressure_pa / 100.0
    return {
        "air_temp_c" : round(temperature_c, 2),
        "humidity_percent" : round(humidity_perc, 2),
        "air_pressure_hpa" : round(pressure_hpa, 2)
    }


if __name__ == "__main__":
    import time
    while True:
        print(read_bme280())
        time.sleep(1)