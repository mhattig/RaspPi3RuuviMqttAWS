rm -r RuuviSensors.json RuuviSensors.log
cp ruuvi_observer.service /etc/systemd/system/ruuvi_observer.service 
cp ruuvi_watchdog.service /etc/systemd/system/ruuvi_watchdog.service 
systemctl enable ruuvi_observer.service 
systemctl start ruuvi_observer.service 
systemctl enable ruuvi_watchdog.service 
systemctl start ruuvi_watchdog.service 
#systemctl status ruuvi_observer.service 
#systemctl status ruuvi_watchdog.service 
