from nonebot.adapters.onebot.v11 import Bot
from nonebot import require, get_bot
from nonebot import logger

require("nonebot_plugin_apscheduler")

from nonebot_plugin_apscheduler import scheduler

import time, asyncio
from random import choice


# lz_list = ["绿头鸡", "鸡脖哥", "鸡脖王", "鸡脖哥哥"]
global autoname_gl
autoname_gl: list = []

@scheduler.scheduled_job("interval", minutes=1)
async def _():
    bot = get_bot()
    if len(autoname_gl) == 0:
        gl = [g["group_id"] for g in await bot.get_group_list()]
    if bot:
        timestr = time.strftime("%a %b %d %H:%M %Y CST", time.localtime())
        for g in gl:
            await bot.set_group_card(group_id=g, user_id=bot.self_id, card=f"大头 {timestr}")
            await asyncio.sleep(1)
        # await bot.set_group_card(group_id=774331907, user_id=1626303708, card=choice(lz_list)) 