from time import ticks_ms, ticks_diff, ticks_add
from PiicoDev_TMP117 import PiicoDev_TMP117


MAX_TEMP_READINGS = 60
READ_DELAY = 5000
tempSensor = PiicoDev_TMP117()

location = "Not Set"
Temp_Readings = []
next_read_time = 0


def checkTempReads():
    global next_read_time
    now = ticks_ms()
    try:
        if ticks_diff(next_read_time, now) <= 0:

            next_read_time = ticks_add(now, READ_DELAY)
            readTemp()
    except Exception as err:
        print("error: %s, %s" % (str(err), str(type(err).__name__)))


def readTemp():
    global Temp_Readings
    temperature = tempSensor.readTempC()
    print("checking Temps: Current Temp: %s" % str(temperature))
    if len(Temp_Readings) == MAX_TEMP_READINGS:
        del Temp_Readings[0]
    Temp_Readings.append(temperature)


def calculateAverageTemp():
    global Temp_Readings
    temp_sum = sum(Temp_Readings)
    temp_count = len(Temp_Readings)
    if temp_count < 1:
        return 0
    return temp_sum / temp_count
