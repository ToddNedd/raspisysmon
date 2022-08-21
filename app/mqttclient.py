import logging
from paho.mqtt import client as mqtt

class MqttClient:
    def __init__(self,  userName, password, clientId):
        self.isConnected = False
        self.isRunning = False
        self.client = self.create_client(userName, password, clientId)

    def create_client(self, userName, password, clientId):
         def on_connect(client, userdata, flags, rc):
            if rc == 0:
                logging.info("Mqtt client connected.")
                self.isConnected = True
            else:
                logging.error("Mqtt client connection failed.")
                self.isConnected = False

         def on_diconnect(client, userdata, rc):
            self.isConnected = False
            if rc == 0:
                logging.info("Mqtt client disconnected gracefully.")
            else:
                logging.error("Mqtt client discconnected unexpected.")

         client = mqtt.Client(clientId)
         client.enable_logger()
         client.username_pw_set(userName, password)
         client.on_connect = on_connect
         client.on_disconnect = on_diconnect

         return client    
                

    def connect(self, serverUrl, serverPort):
        if not self.isRunning:
            logging.error("Mqtt client not started - connect failed")
            return        
        self.client.connect(serverUrl, serverPort)

    def disconnect(self):    
        if not self.isConnected:
            logging.warning("Mqtt client already disconnected - disconnect ignored")
            return    
        self.client.disconnect()

    def publish(self, topic, payload):
        if not self.isConnected:
            logging.error("Mqtt client not connected - publishing failed")
            return
        self.client.publish(topic, payload)

    def start(self):
        self.client.loop_start()
        self.isRunning = True

    def stop(self):
        if not self.isRunning:
            logging.warning("Mqtt client not running - stop ignored")
            return
        self.client.loop_stop()
        self.isRunning = False
        logging.info("Mqtt client disconnected")



    
