import json
import time

import threading
import schedule

from raspi_clock.adapters.audio import SongPlayer
from raspi_clock.adapters.display import DisplayLCD
from raspi_clock.adapters.button import Clicker
from raspi_clock.adapters.joystick import Joystick
from raspi_clock.adapters.rotary_encoder import RotaryEncoder

from raspi_clock.setting import AlarmSettings
from raspi_clock.setting import JoystickSettings

class Alarm():

    def __init__(self):
        self.player = SongPlayer()
        self.clicker = Clicker()
        self.display = DisplayLCD()


    def read_alarms(self):
        try:
            self.alarms = json.load(open(AlarmSettings.alarms_path))
            print(f"Loaded {self.alarms}")
        except Exception as e:
            self.alarms = []
            print(e)
        return self.alarms

    
    def show_current_time(self, lock):
        while True:
            with lock:
                self.display.display_string(time.strftime('%H:%M:%S'), 1)
                self.display.display_string(time.strftime('%d %b %Y'), 2)
            time.sleep(0.1)
    

    def start_alarm(self, lock):
        with lock:
            self.display.display_string("SVEGLIA!!!!!", 2)
            print("Staring alarm..")
            self.player.play()
            print("Waiting for click..")
            self.clicker.wait_for_click()
            self.player.stop()


class RaspiClock():
    
    def __init__(self):
        self.alarm = Alarm()
        self.lock = threading.Lock()

    def start_display_time_thread(self):
        self.display_thread = threading.Thread(
            target=self.alarm.show_current_time, args=(self.lock, )
        )
        self.display_thread.start()


    def start_alarm(self):
        self.alarm.start_alarm(self.lock)


    def schedule_alarms(self):
        alarms = self.alarm.read_alarms()
        schedule.clear()
        for a in alarms:
            print(f"Scheduling alarm at {a}")
            schedule.every().day.at(a).do(self.start_alarm)


class JoystickController():

    def __init__(self, clock):
        self.clock = clock
        self.rotary_enc = RotaryEncoder()
    
    def click_listener(self):
        while True:
            # Show alarms on press
            if self.rotary_enc.read_button():  
                with self.clock.lock:
                    self.show_alarms()
                    # If still pressed, go in edit mode
                    if self.rotary_enc.read_button():
                        self.edit_alarm()
            time.sleep(0.1)


    def show_alarms(self):
        if len(self.clock.alarm.alarms):
            self.clock.alarm.display.display_string("Current Alarm", 1)
            self.clock.alarm.display.display_string(self.clock.alarm.alarms[0], 2)
        else:
            self.clock.alarm.display.display_string("No Alarms Set", 1)
        time.sleep(JoystickSettings.press_seconds)



    def edit_alarm(self):
        current_alarm = self.clock.alarm.alarms[0] if len(self.clock.alarm.alarms) else "00:00"
        current_alarm_ints = [int(i) for i in current_alarm.split(":")]
        
        self.clock.alarm.display.display_string("Set Alarm", 1)
        self.clock.alarm.display.display_string(current_alarm, 2)

        # Set Hours
        while self.rotary_enc.read_button():
            time.sleep(0.1)
        while self.rotary_enc.read_button() == 0:
            current_alarm_str = f"->{current_alarm}  "
            self.clock.alarm.display.display_string(current_alarm_str, 2)
            rotatation_perc = self.rotary_enc.read_rotation_perc()
            hours = int( rotatation_perc * AlarmSettings.max_values[0] )
            current_alarm_ints[0] = hours % AlarmSettings.max_values[0]
            current_alarm = f"{current_alarm_ints[0]:02d}:{current_alarm_ints[1]:02d}"

        # Set Minutes
        while self.rotary_enc.read_button():
            time.sleep(0.1)
        while self.rotary_enc.read_button() == 0:
            current_alarm_str = f"  {current_alarm}<-"
            self.clock.alarm.display.display_string(current_alarm_str, 2)
            rotatation_perc = self.rotary_enc.read_rotation_perc()
            minutes = int( rotatation_perc * AlarmSettings.max_values[1] )
            current_alarm_ints[1] = minutes % AlarmSettings.max_values[1]
            current_alarm = f"{current_alarm_ints[0]:02d}:{current_alarm_ints[1]:02d}"

        json.dump([current_alarm], open(AlarmSettings.alarms_path, "w"))
        self.clock.schedule_alarms()
        self.clock.show_alarms()