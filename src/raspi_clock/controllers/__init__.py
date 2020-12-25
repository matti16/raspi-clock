import json
import time

import threading
import schedule

from watchdog.events import FileSystemEventHandler

from raspi_clock.adapters.audio import SongPlayer
from raspi_clock.adapters.display import DisplayLCD
from raspi_clock.adapters.button import Clicker
from raspi_clock.adapters.joystick import Joystick

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
        self.joystick = Joystick()
    
    def click_listener(self):
        while True:
            # Show alarms on press
            if self.joystick.read_z() == 0:  
                with self.clock.lock:
                    self.show_alarms()
                    # If still pressed, go in edit mode
                    if self.joystick.read_z() == 0:
                        self.edit_alarm()


    def show_alarms(self):
        if len(self.clock.alarm.alarms):
            self.clock.alarm.display.display_string("Current Alarm", 1)
            self.clock.alarm.display.display_string(self.clock.alarm.alarms[0], 2)
        else:
            self.clock.alarm.display.display_string("No Alarms Set", 1)
        time.sleep(JoystickSettings.press_seconds)


    def _process_move(self, value_read):
        if value_read > JoystickSettings.max_value * 0.7:
            return 1
        elif value_read < JoystickSettings.max_value * 0.3:
            return -1
        else:
            return 0


    def edit_alarm(self):
        current_alarm = self.clock.alarm.alarms[0] if len(self.clock.alarm.alarms) else "00:00"
        current_alarm_ints = [int(i) for i in current_alarm.split(":")]
        
        editing = 0
        prev_moved_x, prev_moved_y = 0, 0
        self.clock.alarm.display.display_string("Set Alarm", 1)
        self.clock.alarm.display.display_string(current_alarm, 2)
        while self.joystick.read_z() == 0:
            time.sleep(0.1)

        while self.joystick.read_z():
            current_alarm_str = f"->{current_alarm}  " if editing == 0 else f"  {current_alarm}<-"
            self.clock.alarm.display.display_string(current_alarm_str, 2)

            x_read = self.joystick.read_x()
            moved_x = self._process_move(x_read)
            if prev_moved_x != moved_x:
                editing = (editing + moved_x) % 2
                prev_moved_x = moved_x

            if moved_x == 0:
                y_read = self.joystick.read_y()
                moved_y = self._process_move(y_read)
                if prev_moved_y != moved_y:
                    prev_moved_y = moved_y
                    current_alarm_ints[editing] = (current_alarm_ints[editing] + moved_y) % AlarmSettings.max_values[editing]
                    current_alarm = f"{current_alarm_ints[0]:02d}:{current_alarm_ints[1]:02d}"

        json.dump([current_alarm], open(AlarmSettings.alarms_path, "w"))
        self.clock.schedule_alarms()