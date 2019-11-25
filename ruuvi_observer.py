"""
Act as a BLE observer to get BLE advertised data from Ruuvi sensors.
Ruuvi sensor data is converted to JSON. An MQTT connection to AWS IoT 
Core is made, then the JSON data is published.

Cases of no network, network disconnects, network reconnects, etc. 
are all handled. If no network, sensor data is stil recorded locally
in an output file.

"""

import datetime
import config  # all config parameters are in this file.
from rp3_mqtt import Rp3MQTTClient
from ruuvitag_sensor.ruuvi import RuuviTagSensor
from manage_file_size import manage_file_size

# Assign config variables to global variables in this file
ruuvi_sensors = config.ruuvi_sensors
logging = config.logging
outfile = config.outfile
GET_TIME = config.GET_TIME
STILL_ALIVE_COUNT_DOWN = config.STILL_ALIVE_COUNT_DOWN 

def main():

    ruuvi = RuuviTagSensor  # Ruuvi Sensor Object
    macs = list(ruuvi_sensors.keys())
    of = open (outfile, 'a')
    start_str = '----- start UTC: {} -----\r\n'.format(datetime.datetime.utcnow())
    if logging:
        print(start_str)
    of.write(start_str)
    of.close()

    manage_file_size(outfile)
    
    count_down = STILL_ALIVE_COUNT_DOWN 
    while (1):
        # Open and close the file inside the while(1)
        # just incase the file gets deleted instead of
        # copied. Otherwise data is not stored until
        # the next system reboot.

        of = open (outfile, 'a')
        if not count_down:
            # Record still_alive_str every (STILL_ALIVE_COUNT_DOWN * GET_TIME) secs
            count_down = STILL_ALIVE_COUNT_DOWN 
            still_alive_str='----- {} -----\r\n'.format(datetime.datetime.utcnow())
            if logging:
                print(still_alive_str)
            of.write(still_alive_str)
        count_down -= 1

        # Get dict: key=mac, values=ruuvi_sensor_data
        datas = ruuvi.get_data_for_sensors(macs, GET_TIME)
        for key, values in datas.items():
            # Change mac to upper case
            values.update({'mac':key})

            # Add Sensor Name
            values.update({'sensor_name':ruuvi_sensors[key]})

            # Add UTC time
            values.update({'UTC':str(datetime.datetime.utcnow())})

            # Remove unused field sent from ruuvi sensor
            if values.get('data_format', None):
                values.pop('data_format')

            # Network up/down processing
            try:
                # Previously connected, i.e. variable rp3 is assigned
                if rp3.connect_flag:
                    rp3.ruuvi_pub(values)
                else :
                    # MQTT disconnected for some reason, now try reconnect
                    if logging:
                        print('MQTT Disconnected')
                    rp3 = Rp3MQTTClient()   
            except:
                # First time connect, i.e. variable rp3 is not assigned yet
                rp3 = Rp3MQTTClient()   

            output_str = '{}\r\n'.format(str(values))
            of.write(output_str)
            of.flush()
            if logging:
                print('{}\r\n'.format(str(values)))
        of.close()

    rp3.disconnect()
    of.close()

if __name__ == "__main__":
    main()
