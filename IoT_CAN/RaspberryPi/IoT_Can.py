#!/usr/bin/python3


"""
MQTT topics must start with: EricssonONE/esignum/


Example: "EricssonONE/edallam/MQTT_Display/text"




"""

from urllib.request import urlopen
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
     client.publish(topic = "edallam/mmsi/boat/status", payload="Online", qos=0, retain=True) # TODO change to a publish that is with "auth"

def on_disconnect(client, userdata, rc):
     client.publish(topic = "edallam/MQTT_Display/text", payload = "This is a test Message")
     print("PUBLISH: Disconnected From Broker")
     client.publish(topic = "edallam/mmsi/boat/status", payload="Offline - Disconnected", qos=0, retain=True) # TODO change to a publish that is with "auth"
"""

Moved to personal.py
broker_address = "iot.eclipse.org"
broker_address = "129.192.70.56"
MQTT_auth = {'username':"edallam", 'password':"danielhackathon2019"}
broker_portno = 1883


# GET https://api.thingspeak.com/update?api_key=KEBDZO2LBQBJVV1Q&field1=0
ThingSpeak_Write_API_key = 'KEBDZO2LBQBJVV1Q'
ThingSpeak_Read_API_key ='5AYRZYT2BB16CBBW'
ThingSpeak_BaseURL = 'https://api.thingspeak.com/update?'
"""
"""
config = getConfig()

client = mqtt.Client()

#Assigning the object attribute to the Callback Function
client.will_set("EricssonONE/egarage/IoT_Can/status", payload="Offline - Will", qos=0, retain=True)
client.username_pw_set(username = "edallam", password = "danielhackathon2019")
client.on_connect = on_connect
client.on_disconnect = on_disconnect

client.connect(broker_address, broker_portno)

arduino1 = serial.Serial('/dev/ttyACM0',9600,timeout=100)
print("Listening to: " + arduino1.name)
#arduino2 = serial.Serial('/dev/ttyOP_arduino',9600,timeout=10)
#print("Listening to: " + arduino2.name)

# URL where we will send the data, Don't change it
baseURL = ThingSpeak_BaseURL + 'api_key=%s' % ThingSpeak_Write_API_key
"""
# States and Global variables
# BATTERY1
battery1_lastReportedValue = 0.0
# BATTERY2
battery2_lastReportedValue = 0.0
# SOLAR
solar_lastReportedValue    = 0.0
# DOOR
door_lastReportedValue     = 0
# WATER
water_lastReportedValue    = 0

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
    arduino2 = serial.Serial('/dev/ttyACM1',9600,timeout=100)
    arduino3 = serial.Serial('/dev/ttyACM2',9600,timeout=100)
    arduinoMain = [arduino1, arduino2, arduino3]

    #Assigning the object attribute to the Callback Function
    client.will_set("edallam/mmsi/boat/status", payload="Offline - Will", qos=0, retain=True)
    client.username_pw_set(username = config.MQTT_auth['username'], password = config.MQTT_auth['username'])
    client.on_connect = on_connect
    

    client.on_disconnect = on_disconnect

    client.connect(config.broker_address, config.broker_portno)



    while True:
        #try:
        for x in arduinoMain:
            line = x.readline().decode().replace('\r\n','')
            print(line)
            if startwith(line, 'edallam/BATTERY1'):
                data = decode_battery1(line)
                varning_battery1(data)
                publish_battery1(data)
                #signalk_battery1(data)
            if startwith(line, 'edallam/BATTERY2'):
                data = decode_battery1(line)
                varning_battery1(data)
                publish_battery1(data)
            if startwith(line, 'SOLAR'):
                data = decode_solar(line)
                publish_solar(data)
            if "ejacsve/Temp[0]" in line:
                data = decode_input(line)
                publish_display("Temperature", data)
            if "egebant/Distance" in line:
                data = decode_input(line)
                publish_display("Distance", data)
            if "erohsat/lock" in line:
                data = decode_input(line)
                publish_display("Lock", data)
            if startwith(line, 'edallam/DOOR'):
                data = decode_door(line)
                publish_door(data)
                
            else:
                print('No data received')
            send2ThingSpeak()      
            #sleep(1)
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


def publishMqttDisplay(topic, payload):
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
    
##################################################################
# Main battery 
def decode_battery1(line):
    #print(line)
    data = float(line[10:])
    if isinstance(data, float):
        return data
    else:
        return float(0.0) // Error

def varning_battery1(data):
    if isinstance(data, float):
        return data
    else:
        return float(0.0) // Error
   
def publish_battery1(data):
    diff = 0.1
    global ThingSpeak_unreportedChange
    global battery1_lastReportedValue
    global field1_str
    if abs(data-battery1_lastReportedValue) >= diff: 
        ThingSpeak_unreportedChange = True
        battery1_lastReportedValue = data
        data = '%.2f' % data
        field1_str = '&field1=%s' % (data)


def signalk_battery1(data):
    diff = 0.1
    src_str = "115"
    pgn_str= "128267"
    path_str = "electrical.batteries.0.voltage"

    now = str(datetime.datetime.now())

    delta_message = json.loads(' { "updates":[ \
                    { \
                    "source": { \
                      "device": "/dev/arduino", \
                      "src": "'+ src_str +'", "pgn": "'+ pgn_str +'"}, \
                    "timestamp" : "'+ str(now[:10] +'-'+ now[11:]) +'", \
                    "values": [ \
                       { \
                       "path" : "'+ path_str +' ",  "value" : '+ str(data) +' \
                       } ] \
                    }  \
                    ] }')
    print(delta_message)
    


def publish_display(name, data):
    diff = 0.1
    global ThingSpeak_unreportedChange
    global solar_lastReportedValue
    global field4_str
    print("data: {} lastValue: {}".format(data, solar_lastReportedValue))
    if abs(data - solar_lastReportedValue) >= diff: 
        ThingSpeak_unreportedChange = True
        solar_lastReportedValue = data
        data = '%.2f' % data
        field4_str = '&field4=%s' % (data)
        topic = "Water"
        topic = "MQTT_Display/text"
        publishMqttDisplay(topic, name + ": " + data);        
        
##################################################################
# Solar panel
def decode_solar(line):
    data = float(line[7:])
    if isinstance(data, float):
        return data
    else:
        return float(0.0) // Error

def publish_solar(data):
    diff = 0.1
    global ThingSpeak_unreportedChange
    global solar_lastReportedValue
    global field4_str
    print("data: {} lastValue: {}".format(data, solar_lastReportedValue))
    if abs(data - solar_lastReportedValue) >= diff: 
        ThingSpeak_unreportedChange = True
        solar_lastReportedValue = data
        data = '%.2f' % data
        field4_str = '&field4=%s' % (data)
        topic = "Water"
        topic = "MQTT_Display/text"
        publishMqttDisplay(topic, "Solar" + data);




##################################################################
# Water 
def decode_water(line):
    data = int(line[18:])
    if isinstance(data, int):
        return data
    else:
        return 2 // Error

def decode_input(line):
    name, data = line.split(": ")
    data = float(data)
    if isinstance(data, float):
        return data
    else:
        return 2 // Error


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
# Door
def decode_door(line):
    data = int(line[6:])
    if isinstance(data, int):
        return data
    else:
        return 2 // Error

def publish_door(data):
    diff = 0.1
    global ThingSpeak_unreportedChange
    global door_lastReportedValue
    global field6_str
    if abs(data-door_lastReportedValue) >= diff: 
        ThingSpeak_unreportedChange = True
        door_lastReportedValue = data
        data = '%.2f' % data
        field6_str = '&field6=%s' % (data)
        publishMqttDisplay("The Door on your boat just opened!")

##################################################################
# Other functions
##################################################################

def startwith(line,tag):
    if tag in line[0:9]:
        return True
    else:
        return False

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
    """
    field1_str = ''
    field2_str = ''
    field3_str = ''
    field4_str = ''
    field5_str = ''
    field6_str = ''
    field7_str = ''
    field8_str = ''
    """
    
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
