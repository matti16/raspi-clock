import schedule
import threading
import time

from raspi_clock.controllers import Alarm



class RaspiClock():
    
    def __init__(self):
        self.alarm = Alarm()
        self.alarms = self.alarm.read_alarms()


    def start_display_time_thread(self):
        self.display_thread = threading.Thread(target=self.alarm.show_current_time)
        self.display_thread.start()


    def start_alarm(self):
        self.alarm.start_alarm()


    def schedule_alarms(self):
        schedule.clear()
        for a in self.alarms:
            print(f"Scheduling alarm at {a}")
            schedule.every().day.at(a).do(self.start_alarm)


    def schedule_loop(self):
        while True:
            schedule.run_pending()
            time.sleep(1)



def main():
    main_alarm = RaspiClock()
    main_alarm.start_display_time_thread()
    main_alarm.schedule_alarms()
    main_alarm.schedule_loop()


if __name__ == "__main__":
    main()