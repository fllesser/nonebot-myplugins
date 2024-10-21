from nonebot import get_bot
from nonebot.log import logger
from nonebot.plugin import on_command
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import MessageSegment

from nonebot_plugin_apscheduler import scheduler

from .. import GL, IMG_PATH

import asyncio, httpx

@scheduler.scheduled_job(
    "cron",
    hour=8,
    minute=2,
)
async def shopupshop():
    while True:
        try:
            result = await update_dailyshop()
            break
        except Exception as e:
            logger.error(f"商城更新错误 {e}")
            await asyncio.sleep(10)
            continue
    bot = get_bot()
    for g in GL:
        await bot.send_group_msg(group_id=g, message=result) 


shopshop = on_command("商城", priority=5, block=True)    
@shopshop.handle()
async def _():
    await shopshop.finish(message=MessageSegment.image(IMG_PATH / "shop.png"))


updateshop = on_command("更新商城", priority=5, block=True, permission=SUPERUSER)
@updateshop.handle()
async def _():
    result = await update_dailyshop()
    await updateshop.finish(message="手动更新商城成功" + result)

async def update_dailyshop() -> MessageSegment:
    async with httpx.AsyncClient() as client:
        response = await client.get(url= "https://cdn.dingpanbao.cn/blzy/shop.png")
    with open(IMG_PATH / "shop.png", "wb") as f:
        f.write(response.content)
    return MessageSegment.image(IMG_PATH / "shop.png")
