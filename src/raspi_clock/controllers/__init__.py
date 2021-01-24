import json
import time

import threading
import schedule

from raspi_clock.adapters.audio import SongPlayer
from raspi_clock.adapters.display import OLEDDisplay
from raspi_clock.adapters.button import Clicker
from raspi_clock.adapters.rotary_encoder import RotaryEncoder

from raspi_clock.setting import AlarmSettings, RotaryEncoderSettings, MenuSettings

class Alarm():

    def __init__(self):
        self.display = OLEDDisplay()
        self.clicker = Clicker()
        self.player = SongPlayer()


    def read_settings(self):
        try:
            settings = json.load(open(AlarmSettings.SETTINGS_PATH))
            print(f"Loaded {settings}")
            self.alarm = settings.get("alarm", "")
            self.timezone = settings.get("timezone", "GMT")

        except Exception as e:
            self.alarm = ""
            self.timezone = "GMT"
            print(e)

    
    def show_current_time(self, lock):
        while True:
            with lock:
                self.display.show_sun_moon_clock(self.timezone)
            time.sleep(0.1)
    

    def start_alarm(self, lock):
        with lock:
            self.display.show_alarm()
            print("Staring alarm..")
            self.player.play()
            print("Waiting for click..")
            self.clicker.wait_for_click()
            self.player.stop()


class RaspiClock():
    
    def __init__(self):
        self.alarm = Alarm()
        self.alarm.read_settings()
        self.lock = threading.Lock()

    def start_display_time_thread(self):
        self.display_thread = threading.Thread(
            target=self.alarm.show_current_time, args=(self.lock, )
        )
        self.display_thread.start()


    def start_alarm(self):
        self.alarm.start_alarm(self.lock)


    def load_settings(self):
        self.alarm.read_settings()
        schedule.clear()
        if self.alarm.alarm:
            print(f"Scheduling alarm at {self.alarm.alarm} {self.alarm.timezone}")
            schedule.every().day.at(self.alarm.alarm).do(self.start_alarm)


class RotaryController():

    def __init__(self, clock):
        self.clock = clock
        self.display = clock.alarm.display
        self.rotary_enc = RotaryEncoder()
        self.rotary_enc.setup_interrupt()
 
    def click_listener(self):
        while True:
            # Show alarms on press
            if self.rotary_enc.read_button() == 0:
                with self.clock.lock:
                    self.edit_settings()
            time.sleep(0.1)

    def edit_settings(self):
        self.rotary_enc.reset_status()

        while self.rotary_enc.read_button() != 0:
            rotation = self.rotary_enc.rotation
            selected_idx = rotation % len(MenuSettings.OPTIONS)
            self.display.show_menu(MenuSettings.OPTIONS, selected_idx)
