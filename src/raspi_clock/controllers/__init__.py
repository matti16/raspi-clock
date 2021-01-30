import json
import time
import datetime
import pytz

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
            self.alarm = settings.get("alarm_time", "00:00")
            self.alarm_on = settings.get("alarm_on", False)
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
        if self.alarm.alarm_on:
            tz = datetime.datetime.now(tz=pytz.timezone(self.alarm.timezone)).tzinfo
            a = datetime.datetime.strptime(self.alarm.alarm, "%H:%M").replace(tzinfo=tz).astimezone(pytz.utc)
            a = a.strftime("%H:%M")
            print(f"Scheduling alarm at {self.alarm.alarm} {self.alarm.timezone} ({a} UTC)")
            schedule.every().day.at(a).do(self.start_alarm)
        else:
            print(f"Clearing Alarm")
            schedule.clear()


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
        
        while self.rotary_enc.read_button() == 0:
            time.sleep(0.1)
        selected_idx = 0
        while self.rotary_enc.read_button() != 0:
            rotation = self.rotary_enc.rotation
            selected_idx = rotation % len(MenuSettings.OPTIONS)
            self.display.show_menu(MenuSettings.OPTIONS, selected_idx)
        
        while self.rotary_enc.read_button() == 0:
            time.sleep(0.1)
        if selected_idx == 0:
            self.edit_alarm()
        elif selected_idx == 1:
            self.edit_timezone()

    def edit_alarm(self):
        hours, minutes = self.clock.alarm.alarm.split(":")
        hours, minutes = int(hours), int(minutes)
        alarm_on = self.clock.alarm.alarm_on

        # Editing Hours
        self.rotary_enc.reset_status(hours)
        self.display.show_set_alarm(hours, minutes, alarm_on, editing_idx=0)
        while self.rotary_enc.read_button() != 0:
            rotation = self.rotary_enc.rotation
            hours = rotation % AlarmSettings.HOURS
            self.display.show_set_alarm(hours, minutes, alarm_on, editing_idx=0)
        
        while self.rotary_enc.read_button() == 0:
            time.sleep(0.1)

        # Editing Minutes
        self.rotary_enc.reset_status(minutes)
        self.display.show_set_alarm(hours, minutes, alarm_on, editing_idx=1)
        while self.rotary_enc.read_button() != 0:
            rotation = self.rotary_enc.rotation
            minutes = rotation % AlarmSettings.MINUTES
            self.display.show_set_alarm(hours, minutes, alarm_on, editing_idx=1)
        
        while self.rotary_enc.read_button() == 0:
            time.sleep(0.1)



