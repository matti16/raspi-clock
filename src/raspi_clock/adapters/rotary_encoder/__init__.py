import RPi.GPIO as GPIO

from raspi_clock.adapters.drivers.adc_device import ADS7830
from raspi_clock.setting import RotaryEncoderSettings


class RotaryEncoder():
    def __init__(self, button_pin=RotaryEncoderSettings.button_pin, rotary_adc=RotaryEncoderSettings.rotary_adc):
        self.button_pin = button_pin
        self.rotary_adc = rotary_adc
        self.adc = ADS7830()
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def read_button(self):
        return GPIO.input(self.button_pin)

    def read_rotation(self):
        return self.adc.analogRead(self.rotary_adc)
