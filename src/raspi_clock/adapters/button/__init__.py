from evdev import InputDevice, ecodes

from raspi_clock.setting import ClickerSettings

class Clicker():

    def __init__(self, input_device=ClickerSettings.input_device):
        self.input_device = input_device

    def wait_for_click(self):
        try:
            clicker = InputDevice(self.input_device)
            print("Clicker present")
            for event in clicker.read_loop():
                if event.type == ecodes.EV_KEY:
                    if event.value == ClickerSettings.ev_val_pressed:
                        if event.code == ClickerSettings.btn_code:
                            print("Clicker pressed")
                            clicker.close()
                            break
        except Exception as e:
            found = False
            print(e)
            print("Clicker not found. Waiting for clicker")
            while not found:
                try:
                    clicker = InputDevice(self.input_device)
                    print("Clicker found")
                    found = True
                except Exception:
                    pass
        return True