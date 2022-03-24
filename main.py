from machine import Pin
import utime
import random

import machine
#machine.freq(240000000) #only recently discovered it runs on 160Mhz by default.
machine.freq(160000000) #wemos d1 mini

step_pin=Pin(4, Pin.OUT)


cycle_time=10 # (seconds)
steps=(360/1.8)*32
steps=(360/1.8)*4
sleep_time=round(cycle_time*1000000/(steps))
next_sleep_time=sleep_time

start_time=utime.ticks_ms()
clock_time=0

while True:
    for i in range(0,(steps) +1):
     step_pin.value(1)
     step_pin.value(0)
     utime.sleep_us(next_sleep_time)



    clock_time=clock_time+(cycle_time*1000)
    actual_time=utime.ticks_ms()-start_time
    diff=clock_time-actual_time

    print("Clock     : {} mS".format(clock_time))
    print("Actual    : {} mS".format(actual_time))
    print("Difference: {} mS".format(diff))

    correction_factor=clock_time/actual_time
    print("Correction factor: {}".format(correction_factor))

    # adjust sleeptime to the correct value
    sleep_time=round(sleep_time*correction_factor)

    # in the next cycle try to make up for lost time
    next_sleep_time=round(sleep_time*((cycle_time*1000+diff)/(cycle_time*1000)))

    print("Sleep time     : {} uS".format(sleep_time))
    print("Next sleep time: {} uS".format(next_sleep_time))

            