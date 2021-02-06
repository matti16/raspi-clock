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

    BELL_ICON = os.path.join(RESOURCES_PATH, "icons", "bell.bmp")
    BELL_POS = (92, 21)

    MOON_RADIUS = 8
    MOON_SHIFT = 6

    SUNRISE = 6
    SUNSET = 18

    HOURS_TEXT_POS = (42, 21)
    HOURS_FONT = ImageFont.truetype(os.path.join(RESOURCES_PATH, "font", "LeagueGothic-Regular.otf"), 26)

    DATE_TEXT_POS = (45, 49)
    DATE_FONT = ImageFont.truetype(os.path.join(RESOURCES_PATH, "font", "LeagueGothic-Regular.otf"), 15)

    MENU_TITLE_FONT = ImageFont.truetype(os.path.join(RESOURCES_PATH, "font", "LeagueGothic-Regular.otf"), 20)
    MENU_OPTIONS_FONT = ImageFont.truetype(os.path.join(RESOURCES_PATH, "font", "LeagueGothic-Regular.otf"), 16)

    TIMEZONES_FONT = ImageFont.truetype(os.path.join(RESOURCES_PATH, "font", "Montserrat-Regular.otf"), 9)
    

class AudioSettings(object):
    FILE_PATH = os.path.join(RESOURCES_PATH, "media", "Queen-Dont_Stop_Me_Now.mp3")

class ClickerSettings(object):
    INPUT_DEVICE = "/dev/input/event1"
    EV_VAL_PRESSEC = 1
    EV_VALRELEASED = 0
    BTN_CODE = 115

class AlarmSettings(object):
    SETTINGS_PATH = os.path.join(BASE_PATH, "settings.json")
    HOURS = 24
    MINUTES = 60
    TIMEZONES = [
        "Africa/Algiers",
        "Africa/Cairo",
        "Africa/Casablanca",
        "Africa/Johannesburg",
        "Africa/Nairobi",
        "America/Sao_Paulo",
        "Asia/Baghdad",
        "Asia/Bahrain",
        "Asia/Bangkok",
        "Asia/Dubai",
        "Asia/Hong_Kong",
        "Asia/Shanghai",
        "Asia/Singapore",
        "Asia/Tokyo",
        "Australia/Adelaide",
        "Australia/Brisbane",
        "Australia/Darwin",
        "Australia/Eucla",
        "Australia/Perth",
        "Australia/Sydney",
        "Canada/Atlantic",
        "Canada/Central",
        "Canada/Eastern",
        "Canada/Mountain",
        "Canada/Pacific",
        "Europe/Amsterdam",
        "Europe/Berlin",
        "Europe/London",
        "Europe/Madrid",
        "Europe/Moscow",
        "Europe/Oslo",
        "Europe/Paris",
        "Europe/Rome",
        "GMT",
        "Indian/Maldives",
        "Indian/Mauritius",
        "US/Alaska",
        "US/Arizona",
        "US/Central",
        "US/Eastern",
        "US/Hawaii",
        "US/Mountain",
        "US/Pacific",
        "UTC"
    ]

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

