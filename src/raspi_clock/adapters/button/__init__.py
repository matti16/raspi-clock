from evdev import InputDevice, ecodes
from select import select

from raspi_clock.setting import ClickerSettings

class Clicker():

    def __init__(self, input_device=ClickerSettings.input_device):
        self.input_device = input_device

    async def wait_for_click(self):
        try:
            clicker = InputDevice(self.input_device)
            print("Clicker present")
            r,_,_ = select([clicker.fd], [], [], 0.1)
            while not r:
                r,_,_ = select([clicker.fd], [], [], 0.1)
            print("Clicker pressed")
            clicker.close()
            return True

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