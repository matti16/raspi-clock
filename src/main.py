from raspi_clock.controllers import Alarm, RaspiClock, AlarmsChangedHandler
from raspi_clock.setting import AlarmSettings

from watchdog.observers import Observer

class Main():

    def __init__(self):
        self.alarm_clock = RaspiClock()
    
    def start(self):
        self.alarm_clock.start_display_time_thread()
        self.alarm_clock.schedule_alarms()
        self.alarm_clock.schedule_loop()
    
    def reload_alarms(self):
        self.alarm_clock.schedule_alarms()
    
    def observe_alarms(self, filepath):
        event_handler = AlarmsChangedHandler(self.alarm_clock)
        observer = Observer()
        observer.schedule(event_handler, path=filepath, recursive=False)
        observer.start()
        


if __name__ == "__main__":
    main = Main()

    main.observe_alarms(AlarmSettings.alarms_path)

    main.start()