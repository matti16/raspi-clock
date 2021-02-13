import time
import threading
import schedule

from raspi_clock.controllers import Alarm, RaspiClock, RotaryController
from raspi_clock.setting import AlarmSettings


class Main:
    def __init__(self):
        self.alarm_clock = RaspiClock()
        self.rotary_controller = RotaryController(self.alarm_clock)

    def start(self):
        self.alarm_clock.load_settings()
        self.alarm_clock.start_display_time_thread()
        threading.Thread(target=self.rotary_controller.click_listener).start()


if __name__ == "__main__":
    schedule.clear()
    main = Main()
    time.sleep(3)
    main.start()

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("Interrupted")
