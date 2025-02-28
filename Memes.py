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

from bs4 import BeautifulSoup
import aiohttp
import random

from .. import loader


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

    async def client_ready(self, client, db):
        self.hmodslib = await self.import_lib('https://raw.githubusercontent.com/C0dwiz/H.Modules/refs/heads/main-fix/HModsLibrary.py')

    @loader.command(
        ru_doc="",
        en_doc="",
    )
    async def memescmd(self, message):
        img = await self.hmodslib.get_random_image()
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
        img = await self.hmodslib.get_random_image()
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
