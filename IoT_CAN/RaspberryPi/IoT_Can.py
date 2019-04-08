#!/usr/bin/python3

"""
MQTT topics must start with: EricssonONE/esignum/

Example: "EricssonONE/edallam/MQTT_Display/text"
"""

from urllib.request import urlopen  # Update to urllib2
import serial
import sys
from time import sleep
import json 
import datetime
# For MQTT
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from personal import *


#the callback function
def on_connect(client, userdata, flags, rc):
     print("PUBLISH: Connected With Result Code {}".format(rc))
     client.publish(topic = "EricssonONE/egarage/IoT_Can/status", payload="Online", qos=0, retain=True) # TODO change to a publish that is with "auth"

def on_disconnect(client, userdata, rc):
     client.publish(topic = "EricssonONE/egarage/MQTT_Display/text", payload = "IoT_Can disconnected")
     print("PUBLISH: Disconnected From Broker")
     client.publish(topic = "EricssonONE/egarage/IoT_Can/status", payload="Offline - Disconnected", qos=0, retain=True) # TODO change to a publish that is with "auth"

# States and Global variables
# Temperature
temp_lastReportedValue          = 0.0
# Distance
trashlevel_lastReportedValue    = 0.0
# LOCK
lock_lastReportedValue          = 0
# DOOR
door_lastReportedValue          = 0
# WATER
water_lastReportedValue         = 0
# Laser
laser_lastReportedValue         = 0.0
# BATTERY1
battery1_lastReportedValue      = 0.0
# BATTERY2
battery2_lastReportedValue      = 0.0
# SOLAR
solar_lastReportedValue         = 0.0


# ThingSpeak
ThingSpeak_reportingCounter = 1
ThingSpeak_unreportedChange = True
field1_str = ''
field2_str = ''
field3_str = ''
field4_str = ''
field5_str = ''
field6_str = ''
field7_str = ''
field8_str = ''


class serialList:
    def __init__(self):
        self.arduinoList = []


def startit():
    global ThingSpeak_reportingCounter

    global door_lastReportedValue

    client = mqtt.Client()

    config = getConfig()

    arduino1 = serial.Serial('/dev/ttyACM0',9600,timeout=100)
    #arduino2 = serial.Serial('/dev/ttyACM1',9600,timeout=100)
    #arduino3 = serial.Serial('/dev/ttyACM2',9600,timeout=100)
    arduinos = [arduino1] #, arduino2, arduino3]

    #Assigning the object attribute to the Callback Function
    client.will_set("EricssonONE/egarage/IoT_Can/status", payload="Offline - Will", qos=0, retain=True)
    client.username_pw_set(username = config.MQTT_auth['username'], password = config.MQTT_auth['username'])
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.connect(config.broker_address, config.broker_portno)

    while True:
        #try:
        for arduino in arduinos:
            line = arduino.readline().decode().replace('\r\n','')
            print(line)
            if "egebant/Distance" in line:
                data = decode_input(line)
                trashlevel = round(100-(data-14)/(80-14)*100,2)
                warning_trashlevel(trashlevel)
                #publish_trashlevel(data)
                publish_MQTT("IoT_Can/3/trashlevel", trashlevel)
            if "ejacsve/Temp" in line:
                data = decode_input(line)
                publish_temperature(data)
                publish_MQTT("IoT_Can/3/temp", data)
                #publish_display("Temperature" + (string)data)
                publish_display("Temperature: {}".format(data))
            if "erohsat/Lock" in line:
                data = decode_input(line)
                warning_lock(data)
                publish_lock(data)
                publish_MQTT("IoT_Can/3/3/1/toilet", data)
            if "edallam/DOOR" in line:
                data = decode_input(line)
                warning_door(data)
                publish_door(data)
                publish_MQTT("IoT_Can/3/door", data)
            if "edallam/laser" in line:
                data = decode_input(line)
                varning_laser(data)
                publish_laser(data)
            if "edallam/Water" in line:
                data = decode_input(line)
                varning_water(data)
                publish_water(data)
                #publish_MQTT("IoT_Can/3/water", data)
            if "edallam/BATTERY1" in line:
                data = decode_input(line)
                varning_battery1(data)
                publish_battery1(data)
                #publish_MQTT("IoT_Can/3/battery", data)
                #signalk_battery1(data)
            if "edallam/SOLAR" in line:
                data = decode_input(line)
                publish_solar(data)
                #publish_MQTT("IoT_Can/3/solar", data)
            else:
                print('No data received')
            send2ThingSpeak()      
            ThingSpeak_reportingCounter += 1
            """
        except:
            print('Something went wrong. Retrying!')
            try:
                arduino1 = serial.Serial('/dev/ttyOP_devboard',9600,timeout=10)
                print("Listening to: " + arduino1.name)
            except:
                print('Could not find arduino!')
                sleep(10)
            """    

##################################################################
# Functions below
##################################################################

##################################################################
# Trash level

def warning_trashlevel(trashlevel):
    if trashlevel > 90:
        publish_display("Trashcan is almost full!")

    
def publish_trashlevel(data):
    diff = 10
    global ThingSpeak_unreportedChange
    global trashlevel_lastReportedValue
    global field1_str
    if abs(data - trashlevel_lastReportedValue) >= diff: 
        ThingSpeak_unreportedChange = True
        trashlevel_lastReportedValue = data
        data = '%.2f' % data
        field1_str = '&field1=%s' % (data)
        
##################################################################
# Temperature

def warning_temperature(data):
    if data <= 0.0:
        publish_display("Warning: Freezing temp!")

    
def publish_temperature(data):
    diff = 0.1
    global ThingSpeak_unreportedChange
    global temp_lastReportedValue
    global field2_str
    if abs(data - temp_lastReportedValue) >= diff: 
        ThingSpeak_unreportedChange = True
        temp_lastReportedValue = data
        data = '%.2f' % data
        field2_str = '&field2=%s' % (data)
        
##################################################################
# Lock

def warning_lock(data):
    diff = 0.1
    global lock_lastReportedValue
    if abs(data-door_lastReportedValue) >= diff: 
        if data == 1:
            publish_display("Toilet: Occupied!")
        else:
            publish_display("Toilet: Free!")


def publish_lock(data):
    diff = 0.1
    global ThingSpeak_unreportedChange
    global lock_lastReportedValue
    global field3_str
    if abs(data-lock_lastReportedValue) >= diff: 
        ThingSpeak_unreportedChange = True
        lock_lastReportedValue = data
        data = '%.2f' % data
        field3_str = '&field3=%s' % (data)

##################################################################
# Door

def warning_door(data):
    diff = 0.1
    global door_lastReportedValue
    if abs(data-door_lastReportedValue) >= diff: 
        publish_display("The Door on your boat just opened!")


def publish_door(data):
    diff = 0.1
    global ThingSpeak_unreportedChange
    global door_lastReportedValue
    global field4_str
    if abs(data-door_lastReportedValue) >= diff: 
        ThingSpeak_unreportedChange = True
        door_lastReportedValue = data
        data = '%.2f' % data
        field4_str = '&field4=%s' % (data)
        
##################################################################
# Water 
def warning_water(data):
    if data > 0: 
        publish_display("The trashcan is leaking!")
        #publish_display("Your boat is taking in water!")


def publish_water(data):
    diff = 0.1
    global ThingSpeak_unreportedChange
    global water_lastReportedValue
    global field5_str
    if abs(data-water_lastReportedValue) >= diff: 
        ThingSpeak_unreportedChange = True
        water_lastReportedValue = data
        data = '%.2f' % data
        field5_str = '&field5=%s' % (data)

##################################################################
# Laser Trip Wire
def warning_laser(data):
    if data > 0: 
        publish_display("Your boat is taking in water!")


def publish_laser(data):
    diff = 1
    global ThingSpeak_unreportedChange
    global laser_lastReportedValue
    global field6_str
    if abs(data-laser_lastReportedValue) >= diff: 
        ThingSpeak_unreportedChange = True
        laser_lastReportedValue = data
        data = '%.2f' % data
        field6_str = '&field6=%s' % (data)

##################################################################
# Main battery 

def varning_battery1(data):
    if isinstance(data, float):
        return data
    else:
        return float(0.0) // Error
 
   
def publish_battery1(data):
    diff = 0.1
    global ThingSpeak_unreportedChange
    global battery1_lastReportedValue
    global field7_str
    if abs(data-battery1_lastReportedValue) >= diff: 
        ThingSpeak_unreportedChange = True
        battery1_lastReportedValue = data
        data = '%.2f' % data
        field7_str = '&field7=%s' % (data)
        
##################################################################
# Solar panel

def publish_solar(data):
    diff = 0.1
    global ThingSpeak_unreportedChange
    global solar_lastReportedValue
    global field8_str
    if abs(data - solar_lastReportedValue) >= diff: 
        ThingSpeak_unreportedChange = True
        solar_lastReportedValue = data
        data = '%.2f' % data
        field8_str = '&field8=%s' % (data)

##################################################################
# Other functions
##################################################################
def decode_input(line):
    name, data = line.split(": ")
    data = float(data)
    if isinstance(data, float):
        return data
    else:
        return 2 // Error
  
        
def publish_MQTT(topic, payload):
    config = getConfig()
    egarageTopic = "EricssonONE/egarage/{}".format(topic)

    publish.single(\
    topic = egarageTopic, \
    payload = payload, \
    hostname = config.broker_address, \
    client_id ="", \
    keepalive = 60, \
    will = None, \
    auth = config.MQTT_auth, \
    tls = None, \
    protocol = mqtt.MQTTv311, \
    transport = "tcp")

    print("Publish topic: {} payload: {}".format(egarageTopic,payload))
    
    
def publish_display(name):
    topic = "MQTT_Display/text"
    publish_MQTT(topic, name);        


def send2ThingSpeak():
    global ThingSpeak_reportingCounter
    global ThingSpeak_unreportedChange
    global field1_str
    global field2_str
    global field3_str
    global field4_str
    global field5_str
    global field6_str
    global field7_str
    global field8_str
    global baseURL
    
    # Somethings has to be sent and we did not just send
    # or it was long since we sent something
    if (( ThingSpeak_unreportedChange and ThingSpeak_reportingCounter >= 100) or \
        (  ThingSpeak_reportingCounter >= 1*36)):
        # Sending the data to thingspeak
        field_str = field1_str + field2_str + \
                    field3_str + field4_str + \
                    field5_str + field6_str + \
                    field7_str + field8_str

        config = getConfig()

        # URL where we will send the data, Don't change it
        baseURL = config.ThingSpeak_BaseURL + 'api_key=%s' % config.ThingSpeak_Write_API_key

        print(baseURL + field_str )
        conn = urlopen(baseURL + field_str ) # change from str1 to str to publish all
        print('ThingSpeak publish entry: ' + str(conn.read().decode()))
        # Closing the connection
        conn.close()
        ThingSpeak_unreportedChange = False
        ThingSpeak_reportingCounter = 0
        
##################################################################
if __name__ == "__main__":
    startit()
