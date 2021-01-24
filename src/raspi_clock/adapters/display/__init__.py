import time
import datetime

from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from luma.core.render import canvas

from raspi_clock.setting import DisplaySettings

class OLEDDisplay():

    def __init__(self):
        serial = i2c(port=1, address=0x3C)
        self.device = sh1106(serial)
        with canvas(self.device) as draw:
            draw.text((15, 35), "Loading...", font=DisplaySettings.MENU_OPTIONS_FONT, fill="white")

        
    def draw_moon(self, draw, cx, cy):
        draw.ellipse(
            (cx - DisplaySettings.MOON_RADIUS, cy - DisplaySettings.MOON_RADIUS, cx + DisplaySettings.MOON_RADIUS, cy + DisplaySettings.MOON_RADIUS),
            fill="white", outline="white"
        )
        draw.ellipse((
            cx - DisplaySettings.MOON_RADIUS - DisplaySettings.MOON_SHIFT, cy - DisplaySettings.MOON_RADIUS, cx + DisplaySettings.MOON_RADIUS - DisplaySettings.MOON_SHIFT, cy + DisplaySettings.MOON_RADIUS),
            fill="black", outline="black"
        )


    def draw_sun(self, draw, cx, cy):
        draw.ellipse(
            (cx - DisplaySettings.SUN_RADIUS, cy - DisplaySettings.SUN_RADIUS, cx + DisplaySettings.SUN_RADIUS, cy + DisplaySettings.SUN_RADIUS),
            fill="white", outline="white"
        )

        margin = DisplaySettings.SUN_RADIUS + DisplaySettings.RAY_SUN_MARGIN
        rays = [
            # 4 rays vertical and horizontal
            [(cx - DisplaySettings.RAY_WIDTH/2, cy - margin), (cx, cy - (margin + DisplaySettings.RAY_HEIGHT)), (cx + DisplaySettings.RAY_WIDTH/2, cy - margin)],
            [(cx - DisplaySettings.RAY_WIDTH/2, cy + margin), (cx, cy + (margin + DisplaySettings.RAY_HEIGHT)), (cx + DisplaySettings.RAY_WIDTH/2, cy + margin)],
            [(cx + margin, cy - DisplaySettings.RAY_WIDTH/2), (cx + (margin + DisplaySettings.RAY_HEIGHT), cy), (cx + margin, cy + DisplaySettings.RAY_WIDTH/2)],
            [(cx - margin, cy - DisplaySettings.RAY_WIDTH/2), (cx - (margin + DisplaySettings.RAY_HEIGHT), cy), (cx - margin, cy + DisplaySettings.RAY_WIDTH/2)],
        ]

        rays += [
            # 4 rays X
            [(cx + DisplaySettings.RAY_WIDTH/2, cy - margin), (cx + (margin + DisplaySettings.RAY_HEIGHT)*DisplaySettings.ANGLED_RAYS_SCALE, cy - (margin + DisplaySettings.RAY_HEIGHT)*DisplaySettings.ANGLED_RAYS_SCALE), (cx + margin, cy - DisplaySettings.RAY_WIDTH/2)],
            [(cx - DisplaySettings.RAY_WIDTH/2, cy - margin), (cx - (margin + DisplaySettings.RAY_HEIGHT)*DisplaySettings.ANGLED_RAYS_SCALE, cy - (margin + DisplaySettings.RAY_HEIGHT)*DisplaySettings.ANGLED_RAYS_SCALE), (cx - margin, cy - DisplaySettings.RAY_WIDTH/2)],
            [(cx - DisplaySettings.RAY_WIDTH/2, cy + margin), (cx - (margin + DisplaySettings.RAY_HEIGHT)*DisplaySettings.ANGLED_RAYS_SCALE, cy + (margin + DisplaySettings.RAY_HEIGHT)*DisplaySettings.ANGLED_RAYS_SCALE), (cx - margin, cy + DisplaySettings.RAY_WIDTH/2)],
            [(cx + DisplaySettings.RAY_WIDTH/2, cy + margin), (cx + (margin + DisplaySettings.RAY_HEIGHT)*DisplaySettings.ANGLED_RAYS_SCALE, cy + (margin + DisplaySettings.RAY_HEIGHT)*DisplaySettings.ANGLED_RAYS_SCALE), (cx + margin, cy + DisplaySettings.RAY_WIDTH/2)],
        ]

        for r in rays:
            draw.polygon(r, fill="white", outline="white")


    def get_y_from_x(self, x):
        x_max = self.device.bounding_box[2]
        return 10 + 0.01*(x - x_max/2)**2


    def get_sun_moon_x(self, hours, minutes):
        x_max = self.device.bounding_box[2]
        hours_minutes = hours + minutes/60
        sun_x_position = (hours_minutes - DisplaySettings.SUNRISE) / (DisplaySettings.SUNSET - DisplaySettings.SUNRISE) * x_max

        if hours_minutes > DisplaySettings.SUNRISE + 1:
            moon_x_position = (hours_minutes - DisplaySettings.SUNSET) / (DisplaySettings.SUNSET - DisplaySettings.SUNRISE) * x_max
        else:
            moon_x_position = (hours_minutes + 24 - DisplaySettings.SUNSET) / (DisplaySettings.SUNSET - DisplaySettings.SUNRISE) * x_max
        
        return sun_x_position, moon_x_position


    def show_sun_moon_clock(self):
        with canvas(self.device) as draw:
            now = datetime.datetime.now()
            today_date = now.strftime("%d - %m - %y")

            hours = now.hour
            minutes = now.minute

            sun_x, moon_x = self.get_sun_moon_x(hours, minutes)
            sun_y = self.get_y_from_x(sun_x)
            moon_y = self.get_y_from_x(moon_x)

            self.draw_sun(draw, sun_x, sun_y)
            self.draw_moon(draw, moon_x, moon_y)
            
            draw.text(DisplaySettings.HOURS_TEXT_POS, f"{hours:02d} : {minutes:02d}", font=DisplaySettings.HOURS_FONT, fill="white")
            draw.text(DisplaySettings.DATE_TEXT_POS, today_date, font=DisplaySettings.DATE_FONT, fill="white")
    

    def show_alarm(self):
        with canvas(self.device) as draw:
            draw.text((50, 25), "SVEGLIA!!!!!", fill="white")

    
    def show_menu(options, current):
        with canvas(self.device) as draw:
            draw.text((10, 5), "Settings", font=DisplaySettings.MENU_TITLE_FONT, fill="white")

            draw.text((15, 35), options[current], font=DisplaySettings.MENU_OPTIONS_FONT, fill="white")
            draw.polygon([(5, 25), (12, 30), (5, 35)], fill="white", outline="white")

            if current > 0:
                draw.text((15, 20), options[current-1], font=DisplaySettings.MENU_OPTIONS_FONT, fill="white")
            if current < len(options) - 1:
                draw.text((15, 50), options[current+1], font=DisplaySettings.MENU_OPTIONS_FONT, fill="white")