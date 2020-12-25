import time
import threading
import schedule

from raspi_clock.controllers import Alarm, RaspiClock, AlarmsChangedHandler, JoystickController
from raspi_clock.setting import AlarmSettings

from watchdog.observers import Observer

class Main():

    def __init__(self):
        self.alarm_clock = RaspiClock()
        self.joystick_controller = JoystickController(self.alarm_clock)
    
    def start(self):
        self.alarm_clock.start_display_time_thread()
        self.alarm_clock.schedule_alarms()
        threading.Thread(target=self.joystick_controller.click_listener).start()
    
    def reload_alarms(self):
        self.alarm_clock.schedule_alarms()


if __name__ == "__main__":
    main = Main()
    main.start()

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("Interrupted")