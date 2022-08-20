import os
import logging, sys
from sysinfo import SysInfo
from gracefulshutdown import GracefulShutdown


def main():  

    env_read_cpu_temp = False
    env_update_interval = 5

    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    try:
        env_read_cpu_temp = os.environ['RSM_READ_TEMPERATURE']
    except Exception as err:
         logging.warn(f"Read CPU Temp not specified - {err} - using False")
    
    try:
        env_update_interval = os.environ['RSM_UPDATE_INTERVAL_SEC']
    except Exception as err:
         logging.warn(f"Update interval not specified - {err} - using 5 seconds")

    
    graceful_shutdown = GracefulShutdown()
    sysinfo = SysInfo()

    while not graceful_shutdown.exit_now.is_set():
        try:
            sysinfo.update(withCpuTemp=env_read_cpu_temp)
            print(sysinfo.to_json())
        except Exception as err:
            logging.error(f"Error reading system values - {err}")
        graceful_shutdown.exit_now.wait(env_update_interval)   


if __name__ == '__main__':
    main()

