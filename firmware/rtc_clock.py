from machine import Pin, I2C
import time

# I2C setup
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
addr = 0x68  # RTC I2C address

# BCD conversion helpers
def bcd2dec(b):
    return (b >> 4) * 10 + (b & 0x0F)

def dec2bcd(n):
    return ((n // 10) << 4) | (n % 10)

def read_real_time(  retries =5):
    for attempt in range(1, retries + 1):
        try:
            data = i2c.readfrom_mem(addr, 0x00, 7)  #Data from the read
            seconds = bcd2dec(data[0])  #seocnd converter	
            minutes = bcd2dec(data[1])  #minutes converter
            hours = bcd2dec(data[2])
            day = bcd2dec(data[4])
            month = bcd2dec(data[5] & 0x1F)
            year = bcd2dec(data[6]) + 2000
            return (year, month, day, hours, minutes, seconds, 0, 0)
        except Exception as e:
            print(f"Try{attempt} Crashed: {e}")
            time.sleep(0.5)
    raise OSError("Real-Time clock failed after multiple attempts")

# Write time to RTC
def set_rtc_time(year, month, day, hour, minute, second):
    try:
        data = bytes([
            dec2bcd(second),
            dec2bcd(minute),
            dec2bcd(hour),
            0,  
            dec2bcd( day),
            dec2bcd(month ),
            dec2bcd(year - 2000)
        ])
        i2c.writeto_mem(addr, 0x00, data)  #wrting the value
        print("Real_time setted correctly")
    except Exception as e:
        print("Could not set RTC time", e)

def seconds_since_2000()  :
    try:
        rtc_time =  read_rtc_time_struct()
        t_current =  time.mktime(rtc_time)
        t_base_2000  = time.mktime((2000, 1, 1, 0, 0, 0, 0, 0))
        return int(t_current  - t_base_2000)
    except Exception as e:
        print("Failed to get RTC time:", e)
        return 0  # Fallback value

# Haupt Testing Block
if __name__ == "__main__":
    print("Time Right Now", read_real_time())
    print("Seconds that have passed since year 2000", seconds_since_2000())





