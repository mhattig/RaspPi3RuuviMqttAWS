'''
  Config file for running program that listens for Ruuvi tag 
  beacons/advertisments, then sends the JSON content to the cloud.
'''
# Turn on/off logging
logging=True

# Mac addresses of ruuvi sensors
ruuvi_sensors = {
    'F7:E3:69:3A:DC:5B':'sensor1',
    'FC:ED:B9:D8:51:78':'sensor2',
    'E6:DD:4F:70:29:90':'sensor3',
    'DE:C1:45:A2:2E:99':'sensor4'}

GET_TIME = 30 # Seconds to get advertisments before sending
STILL_ALIVE_COUNT_DOWN = 10 # Count down to save still alive str

# TLS connection cert related files
cafile_filename='./RootCA.pem'
cert_filename='./thingA_cert.pem'
key_filename='./thingA_private_key.pem'

# AWS Iot end-point
client_id='thingA'
endpoint='XXXXXX-ats.iot.us-west-2.amazonaws.com'

# Output file where JSON is stored from Ruuvi sensors
outfile='/home/pi/Gateway/RuuviSensors.json'
