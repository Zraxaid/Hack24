from connections import connect_mqtt, connect_internet
from time import sleep
from hcsr04 import HCSR04
from dht import DHT11
from machine import Pin, PWM
from servo import Servo
import machine, neopixel
import math
import utime


# Define GPIO pins for Motor Pair A (Motor A and Motor B)
IN1 = machine.Pin(20, machine.Pin.OUT)
IN2 = machine.Pin(21, machine.Pin.OUT)

# Define GPIO pins for Motor Pair B (Motor C and Motor D)
IN3 = machine.Pin(27, machine.Pin.OUT)
IN4 = machine.Pin(28, machine.Pin.OUT)

# Define PWM pins for enabling the motors
EN_A = machine.PWM(machine.Pin(16))
EN_B = machine.PWM(machine.Pin(19))

# Set PWM frequency to 1000Hz
EN_A.freq(1000)
EN_B.freq(1000)

# Initialize all pins to low state
IN1.value(0)
IN2.value(0)
IN3.value(0)
IN4.value(0)

EN_A.duty_u16(0)
EN_B.duty_u16(0)


#Define GPIO pins for claw Motors
IN5 = machine.Pin(6, machine.Pin.OUT)
IN6 = machine.Pin(7, machine.Pin.OUT)

# Define PWM pins for enabling the mtors
EN_C = machine.PWM(machine.Pin(16))

#sensors
ultrasonic_sensor = HCSR04(trigger_pin=16, echo_pin=15, echo_timeout_us=10000)
temp_humid_sensor = DHT11(Pin(14, Pin.IN, Pin.PULL_UP))
arm_servo_fb = Servo(pin_id=13)
arm_servo_ud = Servo(pin_id=12)
arm_servo_rotate = Servo(pin_id=11)

#LED
np = neopixel.NeoPixel(machine.Pin(6), 12)

# from constants import ssid, mqtt_server, mqtt_user, mqtt_pass
ssid = "HAcK-Project-WiFi-2"
mqtt_server = "4abe997c2384415d9ce4cebbac507374.s1.eu.hivemq.cloud"
mqtt_user = "user1"
mqtt_pass = "Abcd1234"

#angles
angle_front = 0
angle_up = 150
angle_left = 0
pi = math.pi

#speed
motor_speed = 20000
# Function to handle an incoming message
def cb(topic, msg):
    global angle_front, angle_up, angle_left, pi, motor_speed
    print(f"Topic: {topic}, Message: {msg}")

    if topic == b"speed":
        motor_speed = int(msg)

    if topic == b"direction":
        if msg == b"forward":
            motor_pair_a_forward(motor_speed)
            motor_pair_b_forward(motor_speed)
        elif msg == b"backward":
            motor_pair_a_backward(motor_speed)
            motor_pair_b_backward(motor_speed)
        elif msg == b"left":
            motor_pair_a_forward(motor_speed)
            motor_pair_b_backward(motor_speed)
        elif msg == b"right":
            motor_pair_a_backward(motor_speed)
            motor_pair_b_forward(motor_speed)
        elif msg == b"stop":
            motor_pair_a_stop()
            motor_pair_b_stop()

            
    elif topic == b"arm":
        if msg == b"forward": #assume arm angle starts at 0 (_/) -> something like this (/ -> arm)
            if angle_front > 160:
                pass
            elif angle_front <= 160 and angle_front >= 0:
                angle_front += 10
                arm_servo_fb.write(angle_front)
        elif msg == b"backward":
            if angle_front < 0:
                pass
            elif angle_front >= 0 and angle_front <= 160:
                angle_front -= 10
                arm_servo_fb.write(angle_front)
        elif msg == b"left-rotate": #assume arm angle starts at 0 (/) ->something like this in bird's eye view
            if angle_left < 0:
                pass
            elif angle_left >=0 and angle_left <= 160:
                angle_left += 10
                arm_servo_rotate.write(angle_left)
        elif msg == b"right-rotate": 
            if angle_left > 160:
                pass
            elif angle_left <= 160 and angle_left >= 0:
                angle_left -= 10
                arm_servo_rotate.write(angle_left)
        elif msg == b"arm-up": #assume arm angle starts at 160 (/|) -> something liek this (/ -> arm)
            if angle_up > 160:
                pass
            elif angle_up <= 160 and angle_up >= 0:
                angle_up -= 10
                arm_servo_ud.write(angle_up)
        elif msg == b"arm-down":
            if angle_up < 0:
                pass
            elif angle_up >= 0 and angle_up<=160:
                angle_up += 10
                arm_servo_ud.write(angle_up)

    elif topic == b"pinch":
        if msg == b"grab":
            motor_grab()
        elif msg == b"release":
            motor_release()
    
    elif topic == b"light":
        if msg == b"on":
            light(np)
        elif msg == b"off":
            off(np)


def ultrasonic(sensor):
    try:
        distance = sensor.distance_cm()
        return str(distance)
    except OSError as ex:
        print('ERROR getting distance:', ex)
        return "error"

def temp_humid(sensor):
    try:
        sensor.measure()
        temp = sensor.temperature()
        humid = sensor.humidity()

        return [str(temp), str(humid)]
    finally:
        pass

#motor functions
def motor_pair_a_forward(speed):
    print(('hi'))
    IN1.value(1)
    IN2.value(0)
    EN_A.duty_u16(speed)  

def motor_pair_a_backward(speed):
    IN1.value(0)
    IN2.value(1)
    EN_A.duty_u16(speed)  

def motor_pair_a_stop():
    IN1.value(0)
    IN2.value(0)
    EN_A.duty_u16(0)  # Motor off

def motor_pair_b_forward(speed):
    IN3.value(1)
    IN4.value(0)
    EN_B.duty_u16(speed)  

def motor_pair_b_backward(speed):
    IN3.value(0)
    IN4.value(1)
    EN_B.duty_u16(speed)  

def motor_pair_b_stop():
    IN3.value(0)
    IN4.value(0)
    EN_B.duty_u16(0)  # Motor off

#claw motor functions
def motor_grab():
    IN5.value(1)
    IN6.value(1)
    EN_C.duty(15000)

def motor_release():
    IN5.value(0)
    IN6.value(0)
    EN_C.duty(15000)

#LED functions
def light(np):
    n = np.n

    for i in range(n):
        np[i] = (255, 255, 255)
    
    np.write()

def off(np):
    n = np.n

    for i in range(n):
        np[i] = (0, 0, 0)
    
    np.write()
    

def main():
    print("Testing Motor Pair A forward")
    motor_pair_a_forward(65535)  # Use maximum duty cycle for testing
    utime.sleep(5)
    
    print("Stop motors")
    motor_pair_a_stop()
    utime.sleep(1)
    
    print("Testing Motor Pair A backward")
    motor_pair_a_backward(65535)  # Use maximum duty cycle for testing
    utime.sleep(5)
    
    print("Stop motors")
    motor_pair_a_stop()
    utime.sleep(1)
    try:
        connect_internet(ssid,password="UCLA.HAcK.2024.Summer")
        client = connect_mqtt(mqtt_server, mqtt_user, mqtt_pass)

        client.set_callback(cb)
        client.subscribe("direction")
        client.subscribe("arm")
        client.subscribe("pinch")
        client.subscribe("light")


        #maybe put the publish in a loop so that the data gets updated
        #client.publish("mytopic", "message")

        while True:
            #data = temp_humid(temp_humid_sensor)
            #client.publish("ultrasonic", ultrasonic(ultrasonic_sensor))
            #client.publish("temp", data[0])
            #client.publish("humidity", data[1])
            client.check_msg()
            sleep(1)

    except KeyboardInterrupt:
        print('keyboard interrupt')
        
        
if __name__ == "__main__":
    main()