import machine, onewire, ds18x20, time

# Connect DS18B20 data pin to GP15

data_pin = machine.Pin(15)
ds = ds18x20.DS18X20(onewire.OneWire(data_pin)) #using libraries
roms = ds.scan()

if not roms:
    print("Water sensor could not be found")

else:   #else statement
    print("Water sensor found: ", roms)   #water sensor's location

def read_water_temp():

    """Valuez from the water sensor""" #this statement would be visible
    if not roms:
        return None  # Sensor not found
    ds.convert_temp()
    time.sleep_ms(750)    #sleep time
    temp =  ds.read_temp(roms[0])
    return round(temp, 2)

if __name__ ==  "__main__":

    while True:  
        temp =   read_water_temp()
        sleeping_time_value=1  #defing the sleeping time
        print(f"  Temperature of the water: {temp} in Celcius") # printing the actual value
        time.sleep( sleeping_time_value ) #intervals for the data
