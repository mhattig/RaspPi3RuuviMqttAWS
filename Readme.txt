The code in ths directory can be executed locally; however, it's meant to operate on a Raspberry Pi 3.

Prereqs:
- Precursor is to create an AWS thing with a cert, poicy, etc. 
- The certificate and endpoint are used by the MQTT client to connect to AWS IoT. 
- To create the thing look at my repository to create a thing.
- Copy the certificate files and endpoint from the Thing creation.
- Modify config.py with the correct cert, endpoint, etc. 

Local execution:
- rp3_mqtt.py is a mqtt client. This file can be run locally on your mac, linux, windows machine. The
  purpose of running this locally is to send commands to AWS IoT Core. It's a useful test tool.
- Modify the topic and the data as you see fit before using.

Raspberry Pi execution:
- The code running on the RP3 is two distinct services. Execute the following to deploy these services, 
  and reboot the system.
    > sh deploy_services.sh
    > sudo reboot
- Execute the following to shutdown the services:
    > sh shutdown_services.sh
- JSON data from the Ruuvi tags is stored locally in the output file identified in the config.py file.
- JSON data from the Ruuvi tags is sent to AWS cloud if network connectivity exists.
- RuuviSensors.log is a log file for all the ouput.
- shutdown_services.sh deletes RuuviSensors.json RuuviSensors.log, the default files.

Ruuvi Observer service:
- ruuvi_observer.py is the entry point the Ruuvi tag observer service. 
- ruuvi_obsever.py is a BLE observer that listens specifically for Ruuvi tag advertisments. 
  See https://ruuvi.com/.
- Once a Ruuvi advert is received then some pre-procoessing occurs before the data is sent to AWS IoT
  core via MQTT.
- JSON data from the Ruuvi tags is stored locally in the output file identified in the config.py file.
- JSON data from the Ruuvi tags is sent to AWS cloud if network connectivity exists.

Ruuvi Watchdog service:
- ruuvi_watchdod.py is the entry point to the Ruuvi watchdog service.
- The ruuvi watchdog service verifies that the Ruuvi Observer service is operational.
- If Ruuvi Observer is not operational, then ruuvi_watchdog reboots the the RP3.

Additional robustness:
- It is also recommended that a cron job be setup to reboot the system once per day.

SSH & Networkaccess:
- It is recommended to copy dhcpcd.conf into the /etc/dhcp directory.
- This configures the RP3 to have a static IP address.
- A static ip address makes SSHing into the RP3 much easier because of a known IP address.  
  However, make sure the static IP address is within the IP subnet used by the Wi-Fi router.
- Modify /etc/wpa_supplicant/wpa_supplicant.conf with the credentials of your Wi-Fi router
