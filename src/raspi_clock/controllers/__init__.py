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
                self.display.display_string(time.strftime('    %H:%M:%S    '), 1)
                self.display.display_string(time.strftime('  %d %b %Y   '), 2)
            time.sleep(0.1)
    

    def start_alarm(self, lock):
        with lock:
            self.display.display_string("  SVEGLIA!!!!!  ", 2)
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


    def check_schedules(self):
        while True:
            schedule.run_pending()
            time.sleep(1)


    def schedule_loop(self):
        self.schedule_thread = threading.Thread(
            target=self.check_schedules
        )
        self.schedule_thread.start()



class JoystickController():

    def __init__(self, clock):
        self.clock = clock
        self.joystick = Joystick()
    
    def click_listener(self):
        while True:
            z_read = self.joystick.read_z()
            if z_read == 0:
                self.show_alarms()

    def show_alarms(self):
        with self.clock.lock:
            if len(self.clock.alarm.alarms):
                self.clock.alarm.display.display_string(" Current Alarms ", 1)
                self.clock.alarm.display.display_string(f"     {self.clock.alarm.alarms[0]}     ", 2)
            else:
                self.clock.alarm.display.display_string("No Alarms Set", 1)
            time.sleep(2)



class AlarmsChangedHandler(FileSystemEventHandler):
    def __init__(self, raspi_clock):
        self.raspi_clock = raspi_clock

    def on_modified(self, event):
        print(f'Alarms changed! Reloading...')
        self.raspi_clock.schedule_alarms()
