from machine import Pin, PWM
from time import sleep

# Define GPIO pins for Motor Pair A (Motor A and Motor B)
IN11 = Pin(14, Pin.OUT)
IN12 = Pin(15, Pin.OUT)
IN21 = Pin(12, Pin.OUT)
IN22 = Pin(13, Pin.OUT)

# Define GPIO pins for Motor Pair B (Motor C and Motor D)
IN31 = Pin(27, Pin.OUT)
IN32 = Pin(28, Pin.OUT)
IN41 = Pin(20, Pin.OUT)
IN42 = Pin(21, Pin.OUT)

# Define PWM pins for enabling the motors
EN_A1 = PWM(Pin(16))  # for motor 1
EN_B1 = PWM(Pin(17))  # for motor 2
EN_A2 = PWM(Pin(19))  # for motor 3
EN_B2 = PWM(Pin(22))  # for motor 4

# Set PWM frequency to 1000Hz
EN_A1.freq(1000)
EN_B1.freq(1000)
EN_A2.freq(1000)
EN_B2.freq(1000)

# Initialize all pins to low state
IN11.value(0)
IN12.value(0)
IN21.value(0)
IN22.value(0)
IN31.value(0)
IN32.value(0)
IN41.value(0)
IN42.value(0)

EN_A1.duty_u16(0)
EN_B1.duty_u16(0)
EN_A2.duty_u16(0)
EN_B2.duty_u16(0)

# Motor control functions
def motor_pair_a_forward():
    IN11.value(1)
    IN12.value(0)
    IN21.value(1)
    IN22.value(0)
    EN_A1.duty_u16(65535)
    EN_B1.duty_u16(65535)

def motor_pair_a_backward():
    IN11.value(0)
    IN12.value(1)
    IN21.value(0)
    IN22.value(1)
    EN_A1.duty_u16(65535)
    EN_B1.duty_u16(65535)

def motor_pair_a_stop():
    IN11.value(0)
    IN12.value(0)
    IN21.value(0)
    IN22.value(0)
    EN_A1.duty_u16(0)
    EN_B1.duty_u16(0)

def motor_pair_b_forward():
    IN31.value(0)
    IN32.value(1)
    IN41.value(0)
    IN42.value(1)
    EN_A2.duty_u16(65535)
    EN_B2.duty_u16(65535)

def motor_pair_b_backward():
    IN31.value(1)
    IN32.value(0)
    IN41.value(1)
    IN42.value(0)
    EN_A2.duty_u16(65535)
    EN_B2.duty_u16(65535)
def motor_pair_b_stop():
    IN31.value(0)
    IN32.value(0)
    IN41.value(0)
    IN42.value(0)
    EN_A2.duty_u16(0)
    EN_B2.duty_u16(0)

def move_forward():
    motor_pair_a_forward()
    motor_pair_b_forward()

def move_backward():
    motor_pair_a_backward()
    motor_pair_b_backward()

def rotate_left():
    motor_pair_a_forward()
    motor_pair_b_backward()

def rotate_right():
    motor_pair_a_backward()
    motor_pair_b_forward()

def stop_all():
    motor_pair_a_stop()
    motor_pair_b_stop()
﻿
try:
    led = Pin('LED', Pin.OUT)
    while True:
        led.value(not led.value())
        sleep(0.5)
finally:
    led.value(0)

