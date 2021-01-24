import time
import datetime

from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from luma.core.render import canvas

from raspi_clock.setting import DispalySettings

class OLEDDisplay():

    def __init__(self):
        serial = i2c(port=1, address=0x3C)
        self.device = sh1106(serial)

        
    def draw_moon(self, draw, cx, cy):
        draw.ellipse(
            (cx - DispalySettings.MOON_RADIUS, cy - DispalySettings.MOON_RADIUS, cx + DispalySettings.MOON_RADIUS, cy + DispalySettings.MOON_RADIUS),
            fill="white", outline="white"
        )
        draw.ellipse((
            cx - DispalySettings.MOON_RADIUS - DispalySettings.MOON_SHIFT, cy - DispalySettings.MOON_RADIUS, cx + DispalySettings.MOON_RADIUS - DispalySettings.MOON_SHIFT, cy + DispalySettings.MOON_RADIUS),
            fill="black", outline="black"
        )


    def draw_sun(self, draw, cx, cy):
        draw.ellipse(
            (cx - DispalySettings.SUN_RADIUS, cy - DispalySettings.SUN_RADIUS, cx + DispalySettings.SUN_RADIUS, cy + DispalySettings.SUN_RADIUS),
            fill="white", outline="white"
        )

        margin = DispalySettings.SUN_RADIUS + DispalySettings.RAY_SUN_MARGIN
        rays = [
            # 4 rays vertical and horizontal
            [(cx - DispalySettings.RAY_WIDTH/2, cy - margin), (cx, cy - (margin + DispalySettings.RAY_HEIGHT)), (cx + DispalySettings.RAY_WIDTH/2, cy - margin)],
            [(cx - DispalySettings.RAY_WIDTH/2, cy + margin), (cx, cy + (margin + DispalySettings.RAY_HEIGHT)), (cx + DispalySettings.RAY_WIDTH/2, cy + margin)],
            [(cx + margin, cy - DispalySettings.RAY_WIDTH/2), (cx + (margin + DispalySettings.RAY_HEIGHT), cy), (cx + margin, cy + DispalySettings.RAY_WIDTH/2)],
            [(cx - margin, cy - DispalySettings.RAY_WIDTH/2), (cx - (margin + DispalySettings.RAY_HEIGHT), cy), (cx - margin, cy + DispalySettings.RAY_WIDTH/2)],
        ]

        rays += [
            # 4 rays X
            [(cx + DispalySettings.RAY_WIDTH/2, cy - margin), (cx + (margin + DispalySettings.RAY_HEIGHT)*DispalySettings.ANGLED_RAYS_SCALE, cy - (margin + DispalySettings.RAY_HEIGHT)*DispalySettings.ANGLED_RAYS_SCALE), (cx + margin, cy - DispalySettings.RAY_WIDTH/2)],
            [(cx - DispalySettings.RAY_WIDTH/2, cy - margin), (cx - (margin + DispalySettings.RAY_HEIGHT)*DispalySettings.ANGLED_RAYS_SCALE, cy - (margin + DispalySettings.RAY_HEIGHT)*DispalySettings.ANGLED_RAYS_SCALE), (cx - margin, cy - DispalySettings.RAY_WIDTH/2)],
            [(cx - DispalySettings.RAY_WIDTH/2, cy + margin), (cx - (margin + DispalySettings.RAY_HEIGHT)*DispalySettings.ANGLED_RAYS_SCALE, cy + (margin + DispalySettings.RAY_HEIGHT)*DispalySettings.ANGLED_RAYS_SCALE), (cx - margin, cy + DispalySettings.RAY_WIDTH/2)],
            [(cx + DispalySettings.RAY_WIDTH/2, cy + margin), (cx + (margin + DispalySettings.RAY_HEIGHT)*DispalySettings.ANGLED_RAYS_SCALE, cy + (margin + DispalySettings.RAY_HEIGHT)*DispalySettings.ANGLED_RAYS_SCALE), (cx + margin, cy + DispalySettings.RAY_WIDTH/2)],
        ]

        for r in rays:
            draw.polygon(r, fill="white", outline="white")


    def get_y_from_x(self, x):
        x_max = self.device.bounding_box[2]
        return 10 + 0.01*(x - x_max/2)**2


    def get_sun_moon_x(self, hours, minutes):
        x_max = self.device.bounding_box[2]
        hours_minutes = hours + minutes/60
        sun_x_position = (hours_minutes - DispalySettings.SUNRISE) / (DispalySettings.SUNSET - DispalySettings.SUNRISE) * x_max

        if hours_minutes > DispalySettings.SUNRISE + 1:
            moon_x_position = (hours_minutes - DispalySettings.SUNSET) / (DispalySettings.SUNSET - DispalySettings.SUNRISE) * x_max
        else:
            moon_x_position = (hours_minutes + 24 - DispalySettings.SUNSET) / (DispalySettings.SUNSET - DispalySettings.SUNRISE) * x_max
        
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
            
            draw.text(DispalySettings.HOURS_TEXT_POS, f"{hours:02d} : {minutes:02d}", font=DispalySettings.HOURS_FONT, fill="white")
            draw.text(DispalySettings.DATE_TEXT_POS, today_date, font=DispalySettings.DATE_FONT, fill="white")
    

    def show_alarm(self):
        with canvas(self.device) as draw:
            draw.text((50, 25), "SVEGLIA!!!!!", fill="white")

    
    def show_menu(options, current):
        with canvas(self.device) as draw:
            draw.text((10, 5), "Settings", font=DispalySettings.MENU_TITLE_FONT, fill="white")

            draw.text((15, 35), options[current], font=DispalySettings.MENU_OPTIONS_FONT, fill="white")
            draw.polygon([(5, 25), (12, 30), (5, 35)], fill="white", outline="white")

            if current > 0:
                draw.text((15, 20), options[current-1], font=DispalySettings.MENU_OPTIONS_FONT, fill="white")
            if current < len(options) - 1:
                draw.text((15, 50), options[current+1], font=DispalySettings.MENU_OPTIONS_FONT, fill="white")