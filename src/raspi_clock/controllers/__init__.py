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


    def read_alarms(self):
        try:
            self.alarms = json.load(open(AlarmSettings.ALARMS_PATH))
            print(f"Loaded {self.alarms}")
        except Exception as e:
            self.alarms = []
            print(e)
        return self.alarms

    
    def show_current_time(self, lock):
        while True:
            with lock:
                self.display.show_sun_moon_clock()
            time.sleep(1)
    

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


    def schedule_alarms(self):
        alarms = self.alarm.read_alarms()
        schedule.clear()
        for a in alarms:
            print(f"Scheduling alarm at {a}")
            schedule.every().day.at(a).do(self.start_alarm)


class RotaryController():

    def __init__(self, clock):
        self.clock = clock
        self.display = clock.alarm.display
        self.rotary_enc = RotaryEncoder()
    
    def click_listener(self):
        while True:
            # Show alarms on press
            if self.rotary_enc.read_button() == 0:  
                with self.clock.lock:
                    self.edit_settings()
            time.sleep(0.1)


    def edit_settings(self):
        selected_idx = 0
        self.display.show_menu(MenuSettings.OPTIONS, selected_idx)

        while self.rotary_enc.read_button() != 0:
            clkState = GPIO.input(clk)
            dtState = GPIO.input(dt)

            if clkState == 1 and dtState == 0:
                selected_idx -= 1
            elif clkState == 0 and dtState == 1:
                selected_idx += 1
            
            self.display.show_menu(MenuSettings.OPTIONS, selected_idx)
