from datetime import datetime   #To set date and time
from playsound import playsound     #To play sound
import random
import time

sounds = ["minions_i_swear.mp3", "minions.mp3", "minion_toy.mp3", "minions (1).mp3", "minions_3_talentshow.mp3", "minion_firefighter.mp3", "minions_banana.mp3"]

alarm_hour = '07'
alarm_min = '10'
alarm_period = 'PM'

print('Starting alarm')

while True:
    now = datetime.now()

    current_hour = now.strftime("%I")
    current_min = now.strftime("%M")
    current_period = now.strftime("%p")

    #print(current_hour)
    #print(current_min)
    #print(current_period)

    if alarm_period == current_period:
        if alarm_hour == current_hour:
            if alarm_min == current_min:
                print("Wake Up !")
                randSound = random.choice(sounds)
                playsound('/root/Alarm-Project/sounds/' + randSound)
                break
    time.sleep(1)
