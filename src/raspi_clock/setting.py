import os

class DispalySettings(object):
    num_chars = 16

class AudioSettings(object):
    file_path = "/home/pi/media/audio/thunderstruck_acdc.mp3"

class ClickerSettings(object):
    input_device = "/dev/input/event1"
    ev_val_pressed = 1
    ev_vaL_released = 0
    btn_code = 115

class AlarmSettings(object):
    alarms_path = "/home/pi/raspi-clock/alarms.json"
    max_values = [24, 60]

class JoystickSettings(object):
    z_pin = 12
    y_adc = 0
    x_adc = 1

    max_value = 254

    press_seconds = 1.5

