# Proprietary License Agreement

# Copyright (c) 2024-29 CodWiz

# Permission is hereby granted to any person obtaining a copy of this software and associated documentation files (the "Software"), to use the Software for personal and non-commercial purposes, subject to the following conditions:

# 1. The Software may not be modified, altered, or otherwise changed in any way without the explicit written permission of the author.

# 2. Redistribution of the Software, in original or modified form, is strictly prohibited without the explicit written permission of the author.

# 3. The Software is provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and non-infringement. In no event shall the author or copyright holder be liable for any claim, damages, or other liability, whether in an action of contract, tort, or otherwise, arising from, out of, or in connection with the Software or the use or other dealings in the Software.

# 4. Any use of the Software must include the above copyright notice and this permission notice in all copies or substantial portions of the Software.

# 5. By using the Software, you agree to be bound by the terms and conditions of this license.

# For any inquiries or requests for permissions, please contact codwiz@yandex.ru.

# ---------------------------------------------------------------------------------
# Name: Meme
# Description: Random memes
# Author: @hikka_mods
# Commands:
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# scope: Meme
# scope: Meme 0.0.1
# ---------------------------------------------------------------------------------

import asyncio
from urllib.parse import quote_plus
from datetime import datetime
from bs4 import BeautifulSoup
import aiohttp
import random
import urllib.request
import json

from .. import loader, utils


async def get_random_image():
    random_site = random.randint(1, 3389)
    url = f"https://www.memify.ru/memes/{random_site}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            content = await response.text()
            soup = BeautifulSoup(content, "html.parser")
            items = soup.find_all("div", {"class": "infinite-item card"})
            random_item = random.choice(items)
            second_a = random_item.find_all("a")[1]
            img = second_a.get("href")

    return img


@loader.tds
class MemesMod(loader.Module):
    """Random memes"""

    strings = {
        "name": "Memes",
        "done": "☄️ Catch the meme",
        "still": "🔄 Update",
        "dell": "❌ Close",
    }

    strings_ru = {
        "done": "☄️ Лови мем",
        "still": "🔄 Обновить",
        "dell": "❌ Закрыть",
    }

    @loader.command(
        ru_doc="",
        en_doc="",
    )
    async def memescmd(self, message):
        img = await get_random_image()
        await self.inline.form(
            text=self.strings("done"),
            photo=img,
            message=message,
            reply_markup=[
                [
                    {
                        "text": self.strings("still"),
                        "callback": self.ladno,
                    }
                ],
                [
                    {
                        "text": self.strings("dell"),
                        "callback": self.dell,
                    }
                ],
            ],
            silent=True,
        )

    async def ladno(self, call):
        img = await get_random_image()
        await call.edit(
            text=self.strings("done"),
            photo=img,
            reply_markup=[
                [
                    {
                        "text": self.strings("still"),
                        "callback": self.ladno,
                    }
                ],
                [
                    {
                        "text": self.strings("dell"),
                        "callback": self.dell,
                    }
                ],
            ],
        )

    async def dell(self, call):
        """Callback button"""
        await call.delete()
