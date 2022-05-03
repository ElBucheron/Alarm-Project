#!/usr/bin/env python3
from pydub import AudioSegment
from pydub.playback import play
from datetime import datetime, timedelta
from slowlight import startSlowLight
import signal
import random
import time

sounds = ["minions_i_swear.mp3", "minions.mp3", "minion_toy.mp3", "minions (1).mp3", "minions_3_talentshow.mp3", "minion_firefighter.mp3", "minions_banana.mp3"]

alarm_time = '07:00'
alarm_time_led = (datetime.strptime(alarm_time, '%H:%M') - timedelta(hours=0, minutes=10)).strftime('%H:%M')

def terminateProcess(signalNumber, frame):
    exit(0)

if(__name__ == '__main__'):
    signal.signal(signal.SIGTERM, terminateProcess)

    try:
        print('[+] Alarm set for ' + alarm_time)
        while True:
            now = datetime.now()
            
            current_time = now.strftime('%H:%M')

            if(current_time == alarm_time_led):
                startSlowLight()
            elif(current_time == alarm_time):
                print("Wake Up !")
                randSound = random.choice(sounds)
                # Input an existing mp3 filename
                mp3File = '/root/Alarm-Project/sounds/' + randSound
                # load the file into pydub
                music = AudioSegment.from_mp3(mp3File)
                print("Playing mp3 file...")
                # play the file
                play(music)
                break
            time.sleep(1)
    except KeyboardInterrupt:
        terminateProcess(0,0)
