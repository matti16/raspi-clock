import schedule
import threading
import time

from raspi_clock.controllers import Alarm



def main():
    alarm_ctrl = Alarm()

    x = threading.Thread(target=alarm_ctrl.show_current_time)
    x.start()
    
    alarms = alarm_ctrl.read_alarms()

    for a in alarms:
        print(f"Scheduling alarm at {a}")
        schedule.every().day.at(a).do(alarm_ctrl.start_alarm)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()