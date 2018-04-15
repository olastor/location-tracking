import android
import json
from time import sleep
from datetime import datetime

# time between capturing location
INTERVAL = 10
# directory where log file will be saved
LOGDIR = '/storage/emulated/0'

droid = android.Android()
droid.startLocating()


now = datetime.now()
print('--> Waiting ca. 25 seconds for location service to start')

# Make sure to wait until a nice time where the seconds are exact and modulo 5
secs_wait = 20 + (5 - (now.seconds % 5) - 1) + (1000000 - now.microsecond) / 1000000
sleep(secs_wait)

print('--> Starting to log')
try:
  while True:
    data = {}

    data['location'] = droid.readLocation().result
    # location data also contains timestamp, adding this one for redundancy
    data['timestamp'] = str(datetime.now())

    print(data)

    # Save to log file
    with open(LOGDIR + '/gps_' + data['timestamp'][:10] + '.txt', 'a') as f:
      f.write(json.dumps(data))

    if not data['location']:
      # Error notification
      droid.vibrate()
      droid.notify('Location Tracker', 'Failed to find location.')

    sleep(INTERVAL)
except:
  droid.stopLocating()
