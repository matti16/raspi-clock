import time
import threading

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
        self.alarm_clock.schedule_loop()
        threading.Thread(target=self.joystick_controller.click_listener)
        
    
    def reload_alarms(self):
        self.alarm_clock.schedule_alarms()
    
    def observe_alarms(self, filepath):
        event_handler = AlarmsChangedHandler(self.alarm_clock)
        self.observer = Observer()
        self.observer.schedule(event_handler, path=filepath, recursive=False)
        self.observer.start()
    
    def stop(self):
        self.observer.stop()
        self.observer.join()


if __name__ == "__main__":
    main = Main()
    main.observe_alarms(AlarmSettings.alarms_path)
    main.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        main.stop()