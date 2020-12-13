import json
import time

import threading
import schedule

from watchdog.events import FileSystemEventHandler

from raspi_clock.adapters.audio import SongPlayer
from raspi_clock.adapters.display import DisplayLCD
from raspi_clock.adapters.button import Clicker

from raspi_clock.setting import AlarmSettings

class Alarm():

    def __init__(self):
        self.player = SongPlayer()
        self.clicker = Clicker()
        self.display = DisplayLCD()


    def read_alarms(self):
        try:
            alarms = json.load(open(AlarmSettings.alarms_path))
            print(f"Loaded {alarms}")
        except Exception:
            alarms = []
            print(f"Alarms not found")
        return alarms


    def start_alarm(self):
        print("Staring alarm..")
        self.player.play()
        print("Waiting for click..")
        self.clicker.wait_for_click()
        self.player.stop()

    
    def show_current_time(self):
        while True:
            self.display.display_string(time.strftime('    %H:%M:%S    '), 1)
            self.display.display_string(time.strftime('  %d %b %Y   '), 2)


class RaspiClock():
    
    def __init__(self):
        self.alarm = Alarm()

    def start_display_time_thread(self):
        self.display_thread = threading.Thread(target=self.alarm.show_current_time)
        self.display_thread.start()


    def start_alarm(self):
        self.alarm.start_alarm()


    def schedule_alarms(self):
        alarms = self.alarm.read_alarms()
        schedule.clear()
        for a in alarms:
            print(f"Scheduling alarm at {a}")
            schedule.every().day.at(a).do(self.start_alarm)


    def schedule_loop(self):
        while True:
            schedule.run_pending()
            time.sleep(1)


class AlarmsChangedHandler(FileSystemEventHandler):
    def __init__(self, raspi_clock):
        self.raspi_clock = raspi_clock

    def on_modified(self, event):
        print(f'Alarms changed! Reloading...')
        self.raspi_clock.schedule_alarms()
