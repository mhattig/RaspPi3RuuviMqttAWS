systemctl stop ruuvi_observer.service 
systemctl stop ruuvi_watchdog.service 
systemctl disable ruuvi_observer.service 
systemctl disable ruuvi_watchdog.service 
rm -f /etc/systemd/system/ruuvi_observer.service
rm -f /etc/systemd/system/ruuvi_watchdog.service
systemctl daemon-reload
rm -r RuuviSensors.json RuuviSensors.log
