#!/Users/TR3478/Projects/VoiceControl/VoiceControlEnv/bin/python3.12

import os
import sys
sys.path.append(os.path.join(os.getcwd(), 'tests'))
import rtmidi


def callback(collector, msg):
    print("%s: %s" % (collector.portName, msg))


collectors = rtmidi.CollectorBin()
collectors.start()
print('HIT ENTER TO EXIT')
try:
    sys.stdin.read(1)
except KeyboardInterrupt:
    pass
collectors.stop()
