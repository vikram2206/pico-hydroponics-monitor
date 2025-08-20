machine import ADC, Pin
import time

adc = ADC(Pin(27))
# 🔧 Updated calibration constants
SLOPE =  4.08
INTERCEPT =  2.89

def read_ph_voltage( samples=10, delay=0.01):
    """ Read Values"""
    total = 0
    for _ in range(samples):
        total += adc.read_u16()
        time.sleep(delay)
    avg_raw = total / samples
    voltage = avg_raw * 3.3 / 65535  # Convert to voltage
    return voltage

def read_ph_value():
    """ Read PH values """
    voltage = read_ph_voltage()
    if voltage < 0.05 or voltage > 2.8:
        return None, voltage
    ph = SLOPE * voltage + INTERCEPT
    return round(ph, 2)

if __name__ == "__main__":
    while True :
        ph, voltage = read_ph_value()
        if ph is None:
            print(f"Value e: {voltage:.4f} V")
        else:
            print(f"In Volts: {voltage:.4f} V | pH after running through calibration: {ph:.2f}")
        time.sleep(1)


