import time, httpx

from bs4 import BeautifulSoup
from PIL import Image, ImageFont
from PIL.Image import Resampling
from io import BytesIO

from nonebot.log import logger

from .. import FONT_PATH, IMG_PATH
from .._build_image import BuildImage

vb_url = "https://freethevbucks.com/wp-content/uploads/cropped-v-bucks-3-32x32.png"

async def update_daily_vb() -> str:
    url = "https://freethevbucks.com/timed-missions/"
    async with httpx.AsyncClient() as client:
        free_resp = await client.get(url)
        ele_resp = await client.get("https://img.icons8.com/office/30/000000/lightning-bolt.png")
        vb_resp = await client.get(vb_url)
    soup = BeautifulSoup(free_resp.content, "lxml")
    # 电力图标
    ele_img = Image.open(BytesIO(ele_resp.content))
    ele_img = ele_img.resize((15, 15), Resampling.LANCZOS)

    # vb图标
    vb_icon = Image.open(BytesIO(vb_resp.content))
    vb_icon = vb_icon.resize((15, 15), Resampling.LANCZOS)
    # vb图
    img = BuildImage(width=256, height=220, font_size=15,
                    color=(36, 44, 68), font="gorga.otf")
    # 起始纵坐标
    Y = 30
    timestr = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    await img.text(pos=(0, 185), text=timestr, center_type="width", fill=(255, 255, 255))
    for item in soup.find_all("p"):
        if item.span is not None and item.span.b is not None:
            storm_src = item.img.get("src")  # 风暴图标链接
            async with httpx.AsyncClient() as client:
                resp = await client.get(storm_src)
            storm_img = Image.open(BytesIO(resp.content))
            await img.paste(image=storm_img, pos=(40, Y))  # 风暴图标
            # 电力
            await img.text(text=item.b.string, pos=(70, Y - 3), fill=(255, 255, 255))
            await img.paste(image=ele_img, pos=(88, Y + 2))  # 电力图标
            vb_num: str = item.span.text.split(",")[0]
            await img.paste(image=vb_icon, pos=(113, Y + 2)) 
            await img.text(pos=(130, Y - 3), text=vb_num, fill=(255, 255, 255))
            Y += 30
    if Y == 30:
        img.font = ImageFont.truetype(str(FONT_PATH / "HWXingKai.ttf"), 30)
        await img.text(pos=(0, 80), text="今天没有vb图捏", center_type="by_width", fill=(255, 255, 255))
    await img.save(IMG_PATH / "fn_stw.png")
    return "fn_stw.png"