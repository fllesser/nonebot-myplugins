from nonebot import get_bot
from nonebot.log import logger
from nonebot.plugin import on_command
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment

from nonebot_plugin_apscheduler import scheduler

from .data_source import update_daily_vb
from .. import IMG_PATH, GL

import asyncio

pve = on_command("vb图", aliases={"VB图", "V币图", "v币图"}, block=True)
@pve.handle()
async def _():
    await pve.finish(message=MessageSegment.image(IMG_PATH / "fn_stw.png"))

update_pve = on_command("更新vb图", block=True, permission=SUPERUSER)

@update_pve.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    img_name = await update_daily_vb()
    await update_pve.finish(message="手动更新 STW(PVE) vb图成功" + MessageSegment.image(IMG_PATH / img_name))

@scheduler.scheduled_job(
    "cron",
    hour=8,
    minute=10,
)
async def _():
    # msg = None
    while True:
        try:
            img_name = await update_daily_vb()
            msg = MessageSegment.image(IMG_PATH / img_name)
            break
        except Exception as e:
            logger.error(f"PVE vb图更新错误 {e}")
            # ssl错误, 重新更新vb图
            await asyncio.sleep(10)
            continue
    bot = get_bot()
    for g in GL:
        await bot.send_group_msg(group_id=g, message=msg)
        