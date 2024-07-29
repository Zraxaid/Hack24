from connections import connect_mqtt, connect_internet
from time import sleep
from machine import Pin


# from constants import ssid, mqtt_server, mqtt_user, mqtt_pass
# Input variables here:
mqtt_server = "ea703cf543054c5994a69a146070a15d.s1.eu.hivemq.cloud"
mqtt_user = "user1"
mqtt_pass = "Abcd1234"
ssid = "HAcK-Project-WiFi-2"
# Function to handle an incoming message

def cb(topic, msg):
#     print(f"Topic: {topic}, Message: {msg}")
    if topic == b"mytopic":
        print("Message from mytopic")

def testBlink():
    led = Pin('LED', Pin.OUT)
    x = 1
    while x < 6:
        x += 1
        led.value(not led.value())
        sleep(0.5)
    

def main():
    testBlink()
    try:
        connect_internet(ssid,password='UCLA.HAcK.2024.Summer') #Change none to the appropriate password.
        client = connect_mqtt(mqtt_server, mqtt_user, mqtt_pass)

        client.set_callback(cb)
        client.subscribe("mytopic")
        client.publish("mytopic", "message")
        while True:
            client.check_msg()
            sleep(1)
        

    except KeyboardInterrupt:
        print('keyboard interrupt')

        
        
if __name__ == "__main__":
    main()
