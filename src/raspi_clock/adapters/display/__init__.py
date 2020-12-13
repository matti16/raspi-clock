from i2c_driver import LCD

class DisplayLCD():

    def __init__(self):
        self.lcd = LCD()

    def display_string(self, string, line=1):
        self.lcd.lcd_display_string(string, line)

    def clear_display(self):
        self.display_string("", 1)
        self.display_string("", 2)
    