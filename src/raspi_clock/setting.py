import os

from PIL import ImageFont

BASE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "..")
RESOURCES_PATH = os.path.join(BASE_PATH, "resources")

print("BASE PATH: ", BASE_PATH)

class DisplaySettings(object):
    PORT = 1
    ADDRESS = 0x3C

    SUN_RADIUS = 5
    RAY_SUN_MARGIN = 2
    RAY_WIDTH = 5
    RAY_HEIGHT = 5
    ANGLED_RAYS_SCALE = 0.7

    MOON_RADIUS = 8
    MOON_SHIFT = 6

    SUNRISE = 6
    SUNSET = 18

    HOURS_TEXT_POS = (46, 22)
    HOURS_FONT = ImageFont.truetype(os.path.join(RESOURCES_PATH, "font", "LeagueGothic-Regular.otf"), 25)

    DATE_TEXT_POS = (45, 49)
    DATE_FONT = ImageFont.truetype(os.path.join(RESOURCES_PATH, "font", "LeagueGothic-Regular.otf"), 15)

    MENU_TITLE_FONT = ImageFont.truetype(os.path.join(RESOURCES_PATH, "font", "LeagueGothic-Regular.otf"), 20)
    MENU_OPTIONS_FONT = ImageFont.truetype(os.path.join(RESOURCES_PATH, "font", "LeagueGothic-Regular.otf"), 16)

class AudioSettings(object):
    FILE_PATH = os.path.join(RESOURCES_PATH, "media", "Queen-Dont_Stop_Me_Now.mp3")

class ClickerSettings(object):
    INPUT_DEVICE = "/dev/input/event1"
    EV_VAL_PRESSEC = 1
    EV_VALRELEASED = 0
    BTN_CODE = 115

class AlarmSettings(object):
    ALARMS_PATH = os.path.join(BASE_PATH, "alarms.json")
    MAX_VALUES = [24, 60]

class RotaryEncoderSettings(object):
    CLK_PIN = 20
    DT_PIN = 12
    SW_PIN = 13
    PRESS_SECONDS = 1.5


class MenuSettings(object):
    OPTIONS = [
        "Alarm",
        "Timezone",
        "Exit",
    ]

