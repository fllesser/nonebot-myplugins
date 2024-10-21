import nonebot
from nonebot import require
from pathlib import Path

require("nonebot_plugin_apscheduler")
require("nonebot_plugin_htmlrender")

IMG_PATH = Path() / "resources"/ "image"
FONT_PATH = Path() / "resources" / "font"
TMP_PATH = Path() / "resources" / "temp"
GL = [754044548, 208248400]

nonebot.load_plugins("myplugins/nonebot_plugin_fortnite")


