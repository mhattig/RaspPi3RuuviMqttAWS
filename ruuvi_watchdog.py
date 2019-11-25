"""
This is a stand alone service that monitors the health of the
ruuiv_observer.py by looking at the timedate stamp of the last
update to RuuviSensor.json. 

RuuviSensor.json should be updated at a minimum of 
(GET_TIME * STILL_ALIVE_COUNT_DOWN) seconds. 
Both GET_TIME and STILL_ALIVE_COUNT_DOWN are configuration value
in the config.py file.

More specifically, if RuuviSensor.json is not updated in 
2 * (GET_TIME * STILL_ALIVE_COUNT_DOWN) seconds, 
then the system is rebooted. 

Both ruuvi_observer and this program are services started by
by systemd upon reboot.

"""

import datetime 
import config
import time
import os

outfile = config.outfile
REBOOT_TIME = 2 * (config.GET_TIME * config.STILL_ALIVE_COUNT_DOWN)

def main():
    while(1):
        try: 
            modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(outfile))
            local_time_now = datetime.datetime.now()
            time_diff = int((local_time_now - modified_time).total_seconds())
        except:
            time_diff = 0
            pass

        if time_diff > REBOOT_TIME:
            touch_cmd = 'touch {}'.format(outfile)
            os.system(touch_cmd)
            os.system('sudo reboot')
        time.sleep(30)

if __name__ == '__main__':
    main()
