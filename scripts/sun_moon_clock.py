import math
import time
import datetime

from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from luma.core.render import canvas

from PIL import ImageFont

SUN_RADIUS = 5
RAY_SUN_MARGIN = 2
RAY_WIDTH = 5
RAY_HEIGHT = 5
ANGLED_RAYS_SCALE = 0.7

MOON_RADIUS = 8
MOON_SHIFT = 6

SUNRISE = 6
SUNSET = 18

HOURS_TEXT_POS = (47, 22)
HOURS_FONT = ImageFont.truetype("./LeagueGothic-Regular.otf", 25)

DATE_TEXT_POS = (45, 49)
DATE_FONT = ImageFont.truetype("./LeagueGothic-Regular.otf", 15)


def draw_moon(draw, cx, cy):
    draw.ellipse((cx - MOON_RADIUS, cy - MOON_RADIUS, cx + MOON_RADIUS, cy + MOON_RADIUS), fill="white", outline="white")
    draw.ellipse((cx - MOON_RADIUS - MOON_SHIFT, cy - MOON_RADIUS, cx + MOON_RADIUS - MOON_SHIFT, cy + MOON_RADIUS), fill="black", outline="black")


def draw_sun(draw, cx, cy):
    draw.ellipse((cx - SUN_RADIUS, cy - SUN_RADIUS, cx + SUN_RADIUS, cy + SUN_RADIUS), fill="white", outline="white")

    margin = SUN_RADIUS + RAY_SUN_MARGIN
    rays = [
        # 4 rays vertical and horizontal
        [(cx - RAY_WIDTH/2, cy - margin), (cx, cy - (margin + RAY_HEIGHT)), (cx + RAY_WIDTH/2, cy - margin)],
        [(cx - RAY_WIDTH/2, cy + margin), (cx, cy + (margin + RAY_HEIGHT)), (cx + RAY_WIDTH/2, cy + margin)],
        [(cx + margin, cy - RAY_WIDTH/2), (cx + (margin + RAY_HEIGHT), cy), (cx + margin, cy + RAY_WIDTH/2)],
        [(cx - margin, cy - RAY_WIDTH/2), (cx - (margin + RAY_HEIGHT), cy), (cx - margin, cy + RAY_WIDTH/2)],
    ]

    rays += [
        # 4 rays X
        [(cx + RAY_WIDTH/2, cy - margin), (cx + (margin + RAY_HEIGHT)*ANGLED_RAYS_SCALE, cy - (margin + RAY_HEIGHT)*ANGLED_RAYS_SCALE), (cx + margin, cy - RAY_WIDTH/2)],
        [(cx - RAY_WIDTH/2, cy - margin), (cx - (margin + RAY_HEIGHT)*ANGLED_RAYS_SCALE, cy - (margin + RAY_HEIGHT)*ANGLED_RAYS_SCALE), (cx - margin, cy - RAY_WIDTH/2)],
        [(cx - RAY_WIDTH/2, cy + margin), (cx - (margin + RAY_HEIGHT)*ANGLED_RAYS_SCALE, cy + (margin + RAY_HEIGHT)*ANGLED_RAYS_SCALE), (cx - margin, cy + RAY_WIDTH/2)],
        [(cx + RAY_WIDTH/2, cy + margin), (cx + (margin + RAY_HEIGHT)*ANGLED_RAYS_SCALE, cy + (margin + RAY_HEIGHT)*ANGLED_RAYS_SCALE), (cx + margin, cy + RAY_WIDTH/2)],
    ]

    for r in rays:
        draw.polygon(r, fill="white", outline="white")


def get_y_from_x(device, x):
    x_max = device.bounding_box[2]
    return 10 + 0.01*(x - x_max/2)**2


def get_sun_moon_x(device, hours, minutes):
    x_max = device.bounding_box[2]
    hours_minutes = hours + minutes/60
    sun_x_position = (hours_minutes - SUNRISE) / (SUNSET - SUNRISE) * x_max

    if hours_minutes > SUNRISE + 1:
        moon_x_position = (hours_minutes - SUNSET) / (SUNSET - SUNRISE) * x_max
    else:
        moon_x_position = (hours_minutes + 24 - SUNSET) / (SUNSET - SUNRISE) * x_max
    
    return sun_x_position, moon_x_position



def main():
    today_last_time = "Unknown"
    while True:
        now = datetime.datetime.now()
        today_date = now.strftime("%d %b %y")
        today_time = now.strftime("%H:%M:%S")
        
        if today_time != today_last_time:
            today_last_time = today_time
            with canvas(device) as draw:
                now = datetime.datetime.now()
                today_date = now.strftime("%d - %m - %y")

                hours = now.second%24
                minutes = now.minute

                sun_x, moon_x = get_sun_moon_x(device, hours, minutes)
                sun_y = get_y_from_x(device, sun_x)
                moon_y = get_y_from_x(device, moon_x)

                draw_sun(draw, sun_x, sun_y)
                draw_moon(draw, moon_x, moon_y)
                
                draw.text(HOURS_TEXT_POS, f"{hours:02d}:{minutes:02d}", font=HOURS_FONT, fill="white")
                draw.text(DATE_TEXT_POS, today_date, font=DATE_FONT, fill="white")

            
        time.sleep(0.1)


if __name__ == "__main__":
    try:
        serial = i2c(port=1, address=0x3C)
        device = sh1106(serial)
        main()
    except KeyboardInterrupt:
        pass
