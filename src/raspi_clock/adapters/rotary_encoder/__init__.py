import RPi.GPIO as GPIO

from raspi_clock.setting import RotaryEncoderSettings


class RotaryEncoder():
    def __init__(self):
        self.switch = RotaryEncoderSettings.SW_PIN
        self.clk = RotaryEncoderSettings.CLK_PIN
        self.dt = RotaryEncoderSettings.DT_PIN

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(RotaryEncoderSettings.CLK_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(RotaryEncoderSettings.DT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(RotaryEncoderSettings.SW_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def read_button(self):
        return GPIO.input(self.switch)

    def read_rotation(self):
        clkState = GPIO.input(self.clk)
        dtState = GPIO.input(self.dt)
        if clkState == 1 and dtState == 0:
            rotation = -1
        elif clkState == 0 and dtState == 1:
            rotation = 1
        else:
            rotation = 0
        return rotation
