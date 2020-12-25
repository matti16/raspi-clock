from raspi_clock.adapters.display.i2c_driver import LCD
from raspi_clock.setting import DispalySettings

class DisplayLCD():

    def __init__(self):
        self.lcd = LCD()

    def display_string(self, string, line=1):
        spaces_left = int( (DispalySettings.num_chars - len(string)) / 2)
        display_string = " "*spaces_left + string
        display_string = display_string + " "*(DispalySettings.num_chars - len(display_string)) 
        self.lcd.lcd_display_string(display_string, line)

    def clear_display(self):
        self.display_string("", 1)
        self.display_string("", 2)
    