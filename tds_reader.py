from machine import ADC, Pin

#Set up ADC on GP26 (physical pin 31)
adc= ADC(Pin(26))

def read_tds_voltage():
    raws_Data= adc.read_u16()
    voltage= raws_Data * 3.3 / 65535
    return voltage

def read_tds_value():
    """Looping to change voltage to TDS"""
    voltage = read_tds_voltage()
    tds = (133.42* voltage**3 - 255.86* voltage**2 + 857.39* voltage)* 0.5
    return round(tds, 2)

# Optional standalone test
if __name__ == "__main__":
    import time
    while True:
        voltage = read_tds_voltage()
        sleep_time  =1
        tds = read_tds_value()
        print(f"voltage: {voltage:.3f} V | EC value got: {tds:.2f} ppm")
        time.sleep(sleep_time)

