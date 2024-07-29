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

# Define PWM pins for enabling the motors
EN_A = machine.PWM(machine.Pin(16))
EN_B = machine.PWM(machine.Pin(19))
EN_C = machine.PWM(machine.Pin(11))

# Set PWM frequency to 1000Hz
EN_A.freq(1000)
EN_B.freq(1000)
EN_C.freq(1000)

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

EN_C.duty_u16(0)

#sensors
ultrasonic_sensor = HCSR04(trigger_pin=10, echo_pin=11)
temp_humid_sensor = DHT11(Pin(15, Pin.IN, Pin.PULL_UP))
arm_servo_fb = Servo(pin_id=4)
arm_servo_ud = Servo(pin_id=5)
arm_servo_rotate = Servo(pin_id=11)

#LED
np = neopixel.NeoPixel(machine.Pin(2), 12)

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
motor_speed = 30000
# Function to handle an incoming message
def cb(topic, msg):
    global angle_front, angle_up, angle_left, pi, motor_speed
    print(f"Topic: {topic}, Message: {msg}")

    if topic == b"speed":
        motor_speed = int(msg)

    if topic == b"direction":
        if msg == b"forward":
            # motor_pair_a_forward(motor_speed)
            # motor_pair_b_forward(motor_speed)
            move_forward(motor_speed)
        elif msg == b"backward":
            # motor_pair_a_backward(motor_speed)
            # motor_pair_b_backward(motor_speed)
            move_backward(motor_speed)
        elif msg == b"left":
            # motor_pair_a_forward(motor_speed)
            # motor_pair_b_backward(motor_speed)
            rotate_left(motor_speed)
        elif msg == b"right":
            # motor_pair_a_backward(motor_speed)
            # motor_pair_b_forward(motor_speed)
            rotate_right(motor_speed)
        elif msg == b"stop":
            motor_pair_a_stop()
            motor_pair_b_stop()

            
      elif topic == b"arm":
        if msg == b"forward": #assume arm angle starts at 0 (_/) -> something like this (/ -> arm)
            if angle_front < 0:
                pass
            elif angle_front >= 0 and angle_front <= 80:
                angle_front -= 5
                arm_servo_fb.write(angle_front)
        elif msg == b"backward":
            if angle_front > 80:
                pass
            elif angle_front <= 80 and angle_front >= 0:
                angle_front += 5
                arm_servo_fb.write(angle_front)
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
        elif topic == b"light":
            if msg == b"on":
                light(np)
            elif msg == b"off":
                off(np)
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

print()
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
    IN11.value(1)
    IN12.value(0)
    IN21.value(1)
    IN22.value(0)
    EN_A1.duty_u16(speed)
    EN_B1.duty_u16(speed)

def motor_pair_a_backward(speed):
    IN11.value(0)
    IN12.value(1)
    IN21.value(0)
    IN22.value(1)
    EN_A1.duty_u16(speed)
    EN_B1.duty_u16(speed)

def motor_pair_a_stop():
    IN11.value(0)
    IN12.value(0)
    IN21.value(0)
    IN22.value(0)
    EN_A1.duty_u16(0)
    EN_B1.duty_u16(0)

def motor_pair_b_forward(speed):
    IN31.value(0)
    IN32.value(1)
    IN41.value(0)
    IN42.value(1)
    EN_A2.duty_u16(speed)
    EN_B2.duty_u16(speed)

def motor_pair_b_backward(speed):
    IN31.value(1)
    IN32.value(0)
    IN41.value(1)
    IN42.value(0)
    EN_A2.duty_u16(speed)
    EN_B2.duty_u16(speed)
def motor_pair_b_stop():
    IN31.value(0)
    IN32.value(0)
    IN41.value(0)
    IN42.value(0)
    EN_A2.duty_u16(0)
    EN_B2.duty_u16(0)

def move_forward(speed):
    motor_pair_a_forward(speed)
    motor_pair_b_forward(speed)

def move_backward(speed):
    motor_pair_a_backward(speed)
    motor_pair_b_backward(speed)

def rotate_left(speed):
    motor_pair_a_forward(speed)
    motor_pair_b_backward(speed)

def rotate_right(speed):
    motor_pair_a_backward(speed)
    motor_pair_b_forward(speed)

def stop_all():
    motor_pair_a_stop()
    motor_pair_b_stop()

claw motor functions
def motor_grab():
    IN5.value(1)
    IN6.value(0)
    EN_C.duty_u16(30000)

def motor_release():
    IN5.value(0)
    IN6.value(1)
    EN_C.duty_u16(30000)

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
    led = Pin('LED', Pin.OUT)
    led.value(1)
    light(np)
    try:
        connect_internet(ssid,password="UCLA.HAcK.2024.Summer")
        client = connect_mqtt(mqtt_server, mqtt_user, mqtt_pass)

        client.set_callback(cb)
        client.subscribe("direction")
        client.subscribe("arm")
        client.subscribe("pinch")
        client.subscribe("light")
        client.subscribe("speed")


        #maybe put the publish in a loop so that the data gets updated
        client.publish("mytopic", "message")
        cycles = 0
        while True:
            if cycles == 20:
                data = temp_humid(temp_humid_sensor)
                client.publish("temp", data[0])
                client.publish("humidity", data[1])
                cycles = 0
            client.publish("ultrasonic", ultrasonic(ultrasonic_sensor))
            client.check_msg()
            sleep(0.1)
            # cycles+=1

    except KeyboardInterrupt:
        print('keyboard interrupt')
    finally: 
        motor_pair_a_stop()
        motor_pair_b_stop()
        led.value(0)
        off(np)
        
        
if __name__ == "__main__":
    main()