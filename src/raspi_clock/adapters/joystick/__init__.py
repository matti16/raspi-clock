import RPi.GPIO as GPIO

from raspi_clock.adapters.joystick.adc_device import ADCDevice, ADS7830
from raspi_clock.setting import JoystickSettings


class Joystick():
    def __init__(
        self, 
        z_pin=JoystickSettings.z_pin, 
        y_adc=JoystickSettings.y_adc, 
        x_adc=JoystickSettings.x_adc
        ):
        self.z_pin = z_pin
        self.y_adc = y_adc
        self.x_adc = x_adc
        self.adc = ADS7830()
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(z_pin, GPIO.IN, GPIO.PUD_UP)

    def read_z(self):
        return GPIO.input(self.z_pin)

    def read_y(self):
        return self.adc.analogRead(self.y_adc) 

    def read_x(self):
        return self.adc.analogRead(self.x_adc)

    def destroy(self):
        self.adc.close()
        GPIO.cleanup()
