from connections import connect_mqtt, connect_internet
from time import sleep
from hcsr04 import HCSR04
from dht import DHT11
from machine import Pin, PWM
from servo import Servo
import machine, neopixel
import math
import utime


# Define GPIO pins for Motors 1 and 2
IN11 = Pin(14, Pin.OUT)
IN12 = Pin(15, Pin.OUT)
IN21 = Pin(12, Pin.OUT)
IN22 = Pin(13, Pin.OUT)

# Define GPIO pins for Motors 3 and 4
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

# Define PWM pins for enabling the claw motor
EN_C = machine.PWM(machine.Pin(11))

# Set PWM frequency to 1000Hz
EN_C.freq(1000)

# Define GPIO pins for claw Motors
IN5 = machine.Pin(6, machine.Pin.OUT)
IN6 = machine.Pin(7, machine.Pin.OUT)

# Define PWM pins for enabling the claw motor
EN_C.duty_u16(0)

# Define GPIO pins for the ultrasonic sensor
ultrasonic_sensor = HCSR04(trigger_pin=9, echo_pin=10)

# Define GPIO pins for the temperature and humidity sensors
temp_humid_sensor = DHT11(Pin(8, Pin.IN, Pin.PULL_UP))

# Define GPIO pins for the servos
arm_servo_fb = Servo(pin_id=4)
arm_servo_ud = Servo(pin_id=5)

# Define GPIO pin for the LED ring
np = neopixel.NeoPixel(machine.Pin(2), 12)

# Usernames and passwords, could also import from constants.py
ssid = "?"
mqtt_server = "?"
mqtt_user = "?"
mqtt_pass = "?"

# Arm angles
angle_front = 0
angle_up = 150
angle_left = 0
pi = math.pi

# Motor speed
motor_speed = 30000

# Function to handle incoming messages
def cb(topic, msg):
    global angle_front, angle_up, angle_left, pi, motor_speed
    print(f"Topic: {topic}, Message: {msg}")

    # Reads motor speed
    if topic == b"speed":
        motor_speed = int(msg)

    # Reads direction
    if topic == b"direction":
        if msg == b"forward":
            move_forward(motor_speed)
        elif msg == b"backward":
            move_backward(motor_speed)
        elif msg == b"left":
            rotate_left(motor_speed)
        elif msg == b"right":
            rotate_right(motor_speed)
        elif msg == b"stop":
            motor_pair_a_stop()
            motor_pair_b_stop()

    # Arm messages  
    elif topic == b"arm":
        if msg == b"forward": 
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
        elif msg == b"arm-up": 
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

# Ultrasonic sensor, temperature and humidity sensor functions
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

# Wheel motor functions
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

# Claw motor functions
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
    

# Main function
def main():
    # Turn the Pico LED and LED ring on.
    led = Pin('LED', Pin.OUT)
    led.value(1)
    light(np)
    # Establish connection to the wireless network and the MQTT server.
    try:
        connect_internet(ssid,password="putNetworkPasswordHere")
        client = connect_mqtt(mqtt_server, mqtt_user, mqtt_pass)

        # Pico subscribing from the MQTT server.
        client.set_callback(cb)
        client.subscribe("direction")
        client.subscribe("arm")
        client.subscribe("pinch")
        client.subscribe("light")
        client.subscribe("speed")

        # cycles will prevent the temperature and humidity sensor from measuring too often, thus causing an error.
        client.publish("mytopic", "message")
        cycles = 0
        # Update loop
        while True:
            if cycles == 20:
                data = temp_humid(temp_humid_sensor)
                client.publish("temp", data[0])
                client.publish("humidity", data[1])
                cycles = 0
            client.publish("ultrasonic", ultrasonic(ultrasonic_sensor))
            client.check_msg()
            sleep(0.1)
            cycles+=1

    # When the Pico stops running the program.
    except KeyboardInterrupt:
        print('keyboard interrupt')
    finally: 
        # Turn off motors and LEDs.
        motor_pair_a_stop()
        motor_pair_b_stop()
        led.value(0)
        off(np)
        
        
if __name__ == "__main__":
    main()