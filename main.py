from machine import Pin
import utime
import random

import machine
machine.freq(240000000) #only recently discovered it runs on 160Mhz by default.


pins = [
    Pin(13, Pin.OUT),
    Pin(12, Pin.OUT),
    Pin(14, Pin.OUT),
    Pin(27, Pin.OUT),
]

full_step_sequence = [
    [1,0,0,1],
    [1,1,0,0],
    [0,1,1,0],
    [0,0,1,1],
]

half_step_sequence = [
    [1,0,0,1],
    [1,0,0,0],
    [1,1,0,0],
    [0,1,0,0],
    [0,1,1,0],
    [0,0,1,0],
    [0,0,1,1],
    [0,0,0,1],
]

step_sequence=half_step_sequence

cycle_time=10 # (seconds)
steps=8*64
sleep_time=round(cycle_time*1000000/(steps*len(step_sequence)))
next_sleep_time=sleep_time
noise=0

mod=1

pwm=1

sleep_on=round(sleep_time*pwm)
sleep_off=round(sleep_time* (1-pwm))

start_time=utime.ticks_ms()
clock_time=0

while True:
    for i in range(0,(steps) +1):
        for step in step_sequence:
            for i in range(len(pins)):
                pins[i].value(step[i])
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


    
    # last_check=utime.ticks_ms()/

            