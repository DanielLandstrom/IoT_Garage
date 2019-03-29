# Rename this file personal.py after entering your personal data
class config:
    def __init__(self):
        self.broker_address = "iot.eclipse.org"
        self.MQTT_auth = {'username':"MyMQTTusername", 'password':"MyMQTTpassword"}
        self.broker_portno = 1883
        
        #Example GET https://api.thingspeak.com/update?api_key=KEBDZOBJVV1Q&field1=0
        self.ThingSpeak_Write_API_key = 'KEBDZO2LBQBJVV1Q'
        self.ThingSpeak_Read_API_key ='5AY6CBBW'
        self.ThingSpeak_BaseURL = 'https://api.thingspeak.com/update?'

def getConfig():
    return config()


