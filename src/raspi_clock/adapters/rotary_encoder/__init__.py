import RPi.GPIO as GPIO

from raspi_clock.setting import RotaryEncoderSettings


class RotaryEncoder():
    def __init__(self):
        self.rotation = 0

        self.switch = RotaryEncoderSettings.SW_PIN
        self.clk = RotaryEncoderSettings.CLK_PIN
        self.dt = RotaryEncoderSettings.DT_PIN

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(RotaryEncoderSettings.CLK_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(RotaryEncoderSettings.DT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(RotaryEncoderSettings.SW_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def setup_interrupt(self):
        GPIO.add_event_detect(self.clk, GPIO.FALLING, callback=self.clk_clicked, bouncetime=50)
        GPIO.add_event_detect(self.dt, GPIO.FALLING, callback=self.dt_clicked, bouncetime=50)
    
    def dt_clicked(self, channel):
        clkState = GPIO.input(self.clk)
        dtState = GPIO.input(self.dt)
        if clkState == 1 and dtState == 0:
            self.rotation = self.rotation - 1
    
    def clk_clicked(self, channel):
        clkState = GPIO.input(self.clk)
        dtState = GPIO.input(self.dt)
        if clkState == 0 and dtState == 1:
            self.rotation = self.rotation + 1

    def read_button(self):
        return GPIO.input(self.switch)
    
    def reset_status(self, status=0):
        self.rotation = status
