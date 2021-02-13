from evdev import InputDevice, ecodes
from select import select

from raspi_clock.setting import ClickerSettings


class Clicker:
    def __init__(self, input_device=ClickerSettings.INPUT_DEVICE):
        self.input_device = input_device

    def wait_for_click(self, display):
        i = 0
        try:
            clicker = InputDevice(self.input_device)
            print("Clicker present")
            r, _, _ = select([clicker.fd], [], [], 0.1)
            while not r:
                display.show_alarm_animation(i)
                r, _, _ = select([clicker.fd], [], [], 0.1)
                i = (i + 1) % 1e9
            print("Clicker pressed")
            clicker.close()
            return True

        except Exception as e:
            found = False
            print(e)
            print("Clicker not found. Waiting for clicker")
            while not found:
                try:
                    display.show_alarm_animation(i)
                    clicker = InputDevice(self.input_device)
                    print("Clicker found")
                    found = True
                except Exception:
                    i = (i + 1) % 1e9

        return True
