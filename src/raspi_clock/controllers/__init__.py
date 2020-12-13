import json
import time

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

