import RPi.GPIO as GPIO

from raspi_clock.setting import RotaryEncoderSettings


class RotaryEncoder():
    def __init__(self, button_pin=RotaryEncoderSettings.BUTTON_PIN):
        self.button_pin = button_pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def read_button(self):
        return GPIO.input(self.button_pin)
