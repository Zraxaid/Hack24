from machine import Pin
from time import sleep

try:
    led = Pin('LED', Pin.OUT)
    while True:
        led.value(not led.value())
        sleep(0.5)
finally:
    led.value(0)