import os
import logging, sys
import dotenv
from sysinfo import SysInfo
from gracefulshutdown import GracefulShutdown
from mqttclient import MqttClient

def main():  

    env_read_cpu_temp = False
    env_update_interval = 5
    env_mqtt_broker_url = ""
    env_mqtt_broker_port = 1883
    env_mqtt_user_name = ""
    env_mqtt_password = ""
    env_mqtt_client_id = "SysInfoClient"
    env_mqtt_topic = ""

    # for debugging and test purepose
    if os.path.exists(".env"):
        dotenv.load()


    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    try:
        env_mqtt_broker_url = os.environ['RSM_MQTT_BROKER_URL']
    except Exception as err:
         logging.error(f"Read Mqtt broker url - {err} - exiting")
         exit(-1)

    try:
        env_mqtt_user_name = os.environ['RSM_MQTT_BROKER_USER_NAME']
    except Exception as err:
         logging.error(f"Read Mqtt broker user name - {err} - exiting")
         exit(-1)

    try:
        env_mqtt_password = os.environ['RSM_MQTT_BROKER_PW']
    except Exception as err:
         logging.error(f"Read Mqtt broker password - {err} - exiting")
         exit(-1)

    try:
        env_mqtt_topic = os.environ['RSM_MQTT_TOPIC']
    except Exception as err:
         logging.error(f"Read Mqtt topic - {err} - exiting")
         exit(-1)

    try:
        env_mqtt_broker_port = os.environ['RSM_MQTT_BROKER_PORT']
        env_mqtt_broker_port = int(env_mqtt_broker_port)
    except Exception as err:
         logging.warning(f"Mqtt broker port not specified - {err} - using default: {env_mqtt_broker_port}")

    try:
        env_mqtt_client_id = os.environ['RSM_MQTT_CLIENT_ID']
    except Exception as err:
         logging.warning(f"Mqtt client id not specified - {err} - using : {env_mqtt_client_id}")

    try:
        env_read_cpu_temp = os.environ['RSM_READ_TEMPERATURE']
        logging.info(f"Read CPU Temp set to: {env_read_cpu_temp}")
    except Exception as err:
         logging.warning(f"Read CPU Temp not specified - {err} - using default: {env_read_cpu_temp}")

    
    try:
        env_update_interval = os.environ['RSM_UPDATE_INTERVAL_SEC']
        env_update_interval = int(env_update_interval)
    except Exception as err:
         logging.warning(f"Update interval not specified - {err} - using default: {env_update_interval} seconds")


    
    graceful_shutdown = GracefulShutdown()
    sysinfo = SysInfo(logging.getLogger())
    mqttClient = MqttClient(env_mqtt_user_name, env_mqtt_password, env_mqtt_client_id)
    mqttClient.start()
    mqttClient.connect(env_mqtt_broker_url, env_mqtt_broker_port)
    

    while not graceful_shutdown.exit_now.is_set():
        try:
            sysinfo.update(withCpuTemp=env_read_cpu_temp)
            logging.info(f"payload: {sysinfo.to_json()}")
            mqttClient.publish(env_mqtt_topic, sysinfo.to_json())
        except Exception as err:
            logging.error(f"Error reading system values - {err}")
        graceful_shutdown.exit_now.wait(env_update_interval)   

    mqttClient.disconnect()
    mqttClient.stop()
    logging.info("Shuting down application")

if __name__ == '__main__':
    main()

