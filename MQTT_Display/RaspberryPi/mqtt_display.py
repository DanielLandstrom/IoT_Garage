#!/usr/bin/python3

# Learn more from:
# https://mntolia.com/mqtt-python-with-paho-mqtt-client/

# For MQTT
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
# For display
import time
import serial
# For GPIO
import time
import RPi.GPIO as GPIO

LedPin_red      = 12 # Also connected to output socket
LedPin_green    = 16 # Also connected to output socket
LedPin_blue     = 18 


def setup_serial():
    # Start the serial port
    ser = serial.Serial(
	port='/dev/ttyACM0',
	baudrate=57600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS
    )
    print("Serial port ready:")
    #print(ser)
    ser.isOpen()
    time.sleep(1)

    
def show_on_display(display_str):
    try:
        ans = ser.isOpen()
        print(ans)
        print("Serial port already open")
    except:
        #setup_serial()
        
        ser = serial.Serial(
            port='/dev/ttyACM0',
            baudrate=57600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )
        print("Serial port re-opened")
        #print(ser)
        ser.isOpen()
        time.sleep(1)
        
    print("Display: " + str(display_str).splitlines(False)[0])
    display_str = str(display_str).splitlines(False)[0][0:45] + '                        \r\n'
    display_str = display_str.encode(encoding='UTF-8',errors='strict')
    ser.write(display_str)
    
    
    

#the callback function
def on_connect(client, userdata, flags, rc):
     print("Connected With Result Code {}".format(rc))
     client.publish("EricssonONE/egarage/MQTT_Display/status",payload="Online", qos=0, retain=True) # TODO change to a publish that is with "auth"
     client.subscribe("EricssonONE/egarage/MQTT_Display/text")

def on_disconnect(client, userdata, rc):
    print("Disconnected From Broker")
    client.publish("EricssonONE/egarage/MQTT_Display/status",payload="Offline - Disconnected", qos=0, retain=True) # TODO change to a publish that is with "auth"

"""
def on_message(client, userdata, message):
    print(message.payload.decode())
    print(message.topic)
"""

def on_message_display(client, userdata, message):
    print("Received a new message for the Display")
    #print(message.topic)
    print(message.payload.decode())
    #show_on_display(message.topic +" : "+ message.payload.decode())
    show_on_display(message.payload.decode())

def setup_GPIO():
    #GPIO.cleanup()
    GPIO.setmode(GPIO.BOARD) # Numbers GPIOs by physical location
    GPIO.setwarnings(False)
    GPIO.setup(LedPin_red,      GPIO.OUT)
    GPIO.setup(LedPin_green,    GPIO.OUT)
    GPIO.setup(LedPin_blue,     GPIO.OUT)

def destroy_GPIO():
    GPIO.output(LedPin_red,     GPIO.LOW)
    GPIO.output(LedPin_green,   GPIO.LOW)
    GPIO.output(LedPin_blue,    GPIO.LOW)
    GPIO.cleanup()

def blink_led_red():
    GPIO.output(LedPin_red, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(LedPin_red, GPIO.LOW)
    time.sleep(3)
    GPIO.output(LedPin_red, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(LedPin_red, GPIO.LOW)
    time.sleep(3)

def blink_led_green():
    GPIO.output(LedPin_green, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(LedPin_green, GPIO.LOW)
    time.sleep(1)
    GPIO.output(LedPin_green, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(LedPin_green, GPIO.LOW)
    time.sleep(1)
    
def blink_led_blue():
    GPIO.output(LedPin_blue, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(LedPin_blue, GPIO.LOW)
    time.sleep(1)
    GPIO.output(LedPin_blue, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(LedPin_blue, GPIO.LOW)
    time.sleep(1)

def on_message_led(client, userdata, message):
    print("Received a new message for the GPIO LED")
    #print(message.topic)
    mess = message.payload.decode()
    print(mess)
    if (mess == 'Red'):
        blink_led_red()
    if (mess == 'Green'):
        blink_led_green()
    if (mess == 'Blue'):
        blink_led_blue()

broker_address = "129.192.70.56"
MQTT_auth = {'username':"edallam", 'password':"danielhackathon2019"}
broker_portno = 1883
client = mqtt.Client()
print("MQTT client created")

#Assigning the object attribute to the Callback Function
client.on_connect = on_connect
client.on_disconnect = on_disconnect 
client.will_set("EricssonONE/egarage/MQTT_Display/status", payload="Offline - Will", qos=0, retain=True)
client.username_pw_set(username = "edallam", password = "danielhackathon2019")

#client.on_message = on_message
client.message_callback_add("EricssonONE/egarage/MQTT_Display/text", on_message_display)
client.message_callback_add("EricssonONE/egarage/MQTT_Display/led", on_message_led)

client.connect(broker_address, broker_portno)
print("MQTT client connected")


# Start the serial port
ser = serial.Serial(
        port='/dev/ttyACM0',
        baudrate=57600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
        )
print("Serial port ready:")
#print(ser)
ser.isOpen()
time.sleep(5)


#setup_serial()
setup_GPIO()
#blink_led_blue()

client.loop_forever()


#subscribe.callback( on_message_display, "EricssonONE/egarage/MQTT_Display/text", hostname = broker_address, port = broker_portno, auth = MQTT_auth )
#subscribe.callback( on_message_display, "EricssonONE/egarage/#", hostname = broker_address, port = broker_portno, auth = MQTT_auth )
"""
subscribe.callback( on_message_display, \
                    "EricssonONE/egarage/MQTT_Display/text", \
                    qos = 0, \
                    userdata = None, \
                    hostname = broker_address, \
                    port = broker_portno, \
                    client_id = "", \
                    keepalive = 60, \
                    will = None, \
                    auth = MQTT_auth, \
                    tls = None, \
                    protocol = mqtt.MQTTv311 \
                   )
subscribe.callback( on_message_led, "EricssonONE/egarage/MQTT_Display/led", hostname = broker_address, port = broker_portno, auth = MQTT_auth )
"""

"""
if __name__ == '__main__':
    setup_GPIO()
    try:
        blink_led_blue()
    except KeyboardInterrupt: # When 'Cntr+C' is pressed, the child program destroy_GPIO() will be executed.
        destroy_GPIO()

"""
