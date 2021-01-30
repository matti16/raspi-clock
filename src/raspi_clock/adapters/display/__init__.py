import time
import datetime
import pytz

from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from luma.core.render import canvas

from raspi_clock.setting import DisplaySettings

class OLEDDisplay():

    def __init__(self):
        serial = i2c(port=1, address=0x3C)
        self.device = sh1106(serial)
        with canvas(self.device) as draw:
            draw.text((35, 20), "Loading...", font=DisplaySettings.MENU_TITLE_FONT, fill="white")

        
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


    def show_sun_moon_clock(self, timezone):
        with canvas(self.device) as draw:
            now = datetime.datetime.now(tz=pytz.timezone(timezone))
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

    
    def show_menu(self, options, current):
        with canvas(self.device) as draw:
            middle_y = self.device.height/2

            draw.text((0, middle_y-DisplaySettings.MENU_TITLE_FONT.size/2), "Settings", font=DisplaySettings.MENU_TITLE_FONT, fill="white")
            draw.polygon([(58, middle_y-5), (66, middle_y), (58, middle_y+5)], fill="white", outline="white")

            draw.text(
                (75, middle_y-DisplaySettings.MENU_OPTIONS_FONT.size/2), options[current], 
                font=DisplaySettings.MENU_OPTIONS_FONT, fill="white"
            )
            if current > 0:
                draw.text(
                    (75, 0), options[current-1], 
                    font=DisplaySettings.MENU_OPTIONS_FONT, fill="white"
                )
            if current < len(options) - 1:
                draw.text((75, 50), options[current+1], font=DisplaySettings.MENU_OPTIONS_FONT, fill="white")


    def show_set_alarm(self, hours, minutes, alarm_on, editing_idx):
        with canvas(self.device) as draw:
            middle_y = self.device.height/2
            draw.text(
                (15, middle_y-DisplaySettings.MENU_TITLE_FONT.size/2), 
                "Alarm", 
                font=DisplaySettings.MENU_TITLE_FONT, 
                fill="white"
            )

            draw.text(
                (65, 7), 
                f"{hours:02d} : {minutes:02d}", 
                font=DisplaySettings.HOURS_FONT, 
                fill="white"
            )
            
            draw.ellipse(
                (80, 48, 93, 60),
                fill="white" if alarm_on else "black", 
                outline="white"
            )
            draw.text(
                (100, 48), 
                "ON" if alarm_on else "OFF", 
                fill="white"
            )
            
            if editing_idx == 0:
                draw.polygon([(68, 40), (73, 35), (78, 40)], fill="white", outline="white")
            elif editing_idx == 1:
                draw.polygon([(97, 40), (102, 35), (107, 40)], fill="white", outline="white")
            elif editing_idx == 2:
                draw.polygon([(65, 50), (70, 53), (65, 56)], fill="white", outline="white")