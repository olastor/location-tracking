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

print('--> Waiting 20 seconds for location service to start')
sleep(20)

print('--> Starting to log')
today = str(datetime.now())[:10]

try:
  while True:
    data = droid.readLocation().result
    data['timestamp'] = str(datetime.now())

    print(data)
    with open(LOGDIR + '/gps_' + today + '.txt', 'a') as f:
      f.write(json.dumps(data))

    if not data:
      # Error notification
      droid.vibrate()
      droid.notify('Location Tracker','Failed to locate.')

    sleep(INTERVAL)
except:
  droid.stopLocating()
