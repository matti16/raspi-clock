from evdev import InputDevice, ecodes

from raspi_clock.setting import ClickerSettings

class Clicker():

    def __init__(self, input_device=ClickerSettings.input_device):
        self.clicker = InputDevice(input_device)

    def wait_for_click(self):
        for event in self.clicker.read_loop():
            if event.type == ecodes.EV_KEY:
                if event.value == ClickerSettings.ev_val_pressed:
                    if event.code == ClickerSettings.btn_code:
                        print("Clicker pressed")
                        return True