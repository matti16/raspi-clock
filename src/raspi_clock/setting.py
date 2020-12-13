import os

class AudioSettings(object):
    file_path = os.path.join("home/pi", "media/audio/lets_love-david_guetta+sia.mp3")

class ClickerSettings(object):
    input_device = "/dev/input/event1"
    ev_val_pressed = 1
    ev_vaL_released = 0
    btn_code = 115

class AlarmSettings(object):
    alarms_path = os.path.join("/home/pi/", "raspi-clock/alarms.json")

