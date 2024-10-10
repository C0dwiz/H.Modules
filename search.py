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
# Name: Search
# Description: Search for your question on the Internet
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# scope: Api Search
# scope: Api Search 0.0.1
# ---------------------------------------------------------------------------------

from telethon.tl.types import Message  # type: ignore
from urllib.parse import quote

from .. import loader, utils
from ..inline.types import InlineCall, InlineQuery

__version__ = (1, 0, 0)


@loader.tds
class Search(loader.Module):
    """Поисковик"""

    strings = {
        "name": "Search",
        "search": "<emoji document_id=5188311512791393083>🌎</emoji><b> I searched for information for you</b> ",
        "isearch": "🔎<b> I searched for information for you</b> ",
        "link": "🗂️ Link to your request",
        "close": "❌ Close",
    }

    strings_ru = {
        "search": "<emoji document_id=5188311512791393083>🌎</emoji><b> Я поискал информацию за тебя</b> ",
        "isearch": "🔎<b> Я поискал информацию за тебя</b> ",
        "link": "🗂️ Ссылка на ваш запрос",
        "close": "❌ Закрыть",
    }

    @loader.command(
        ru_doc="Поискать в Google",
        en_doc="Search on Google",
    )
    async def google(self, message: Message):
        g = utils.get_args_raw(message)
        google = f"https://google.com/search?q={g}"
        await utils.answer(
            message, self.strings("search") + f'<a href="{google}">Ссылка</a>'
        )

    @loader.command(
        ru_doc="Поискать в Yandex",
        en_doc="Search on Yandex",
    )
    async def yandex(self, message: Message):
        y = utils.get_args_raw(message)
        yandex = f"https://yandex.ru/?q={y}"
        await utils.answer(
            message, self.strings("search") + f'<a href="{yandex}">Ссылка</a>'
        )

    @loader.command(
        ru_doc="Поискать в Duckduckgo",
        en_doc="Search on Duckduckgo",
    )
    async def duckduckgo(self, message: Message):
        d = utils.get_args_raw(message)
        duckduckgo = f"https://duckduckgo.com/?q={d}"
        await utils.answer(
            message, self.strings("search") + f'<a href="{duckduckgo}">Ссылка</a>'
        )

    @loader.command(
        ru_doc="Поискать в Bing",
        en_doc="Search on Bing",
    )
    async def bing(self, message: Message):
        b = utils.get_args_raw(message)
        bing = f"https://bing.com/?q={b}"
        await utils.answer(
            message, self.strings("search") + f'<a href="{bing}">Ссылка</a>'
        )

    @loader.command(
        ru_doc="Поискать в You",
        en_doc="Search on You",
    )
    async def you(self, message: Message):
        y = utils.get_args_raw(message)
        you = f"https://you.com/?q={y}"
        await utils.answer(
            message, self.strings("search") + f'<a href="{you}">Ссылка</a>'
        )

    @loader.command(
        ru_doc="Поискать в Google инлайн",
        en_doc="Search on Google inline",
    )
    async def igoogle(self, message: Message):
        g = utils.get_args_raw(message)
        google = f"https://google.com/search?q={g}"
        await self.inline.form(
            text=self.strings("isearch"),
            message=message,
            reply_markup=[
                [
                    {
                        "text": self.strings("link"),
                        "url": google,
                    }
                ],
                [{"text": self.strings("close"), "action": "close"}],
            ],
            silent=True,
        )

    @loader.command(
        ru_doc="Поискать в Yandex инлайн",
        en_doc="Search on Yandex inline",
    )
    async def iyandex(self, message: Message):
        y = utils.get_args_raw(message)
        yandex = f"https://yandex.ru/?q={y}"
        await self.inline.form(
            text=self.strings("isearch"),
            message=message,
            reply_markup=[
                [
                    {
                        "text": self.strings("link"),
                        "url": yandex,
                    }
                ],
                [{"text": self.strings("close"), "action": "close"}],
            ],
            silent=True,
        )

    @loader.command(
        ru_doc="Поискать в Duckduckgo инлайн",
        en_doc="Search on Duckduckgo inline",
    )
    async def iduckduckgo(self, message: Message):
        d = utils.get_args_raw(message)
        duckduckgo = f"https://duckduckgo.com/?q={d}"
        await self.inline.form(
            text=self.strings("isearch"),
            message=message,
            reply_markup=[
                [
                    {
                        "text": self.strings("link"),
                        "url": duckduckgo,
                    }
                ],
                [{"text": self.strings("close"), "action": "close"}],
            ],
            silent=True,
        )

    @loader.command(
        ru_doc="Поискать в Bing инлайн",
        en_doc="Search on Bing inline",
    )
    async def ibing(self, message: Message):
        b = utils.get_args_raw(message)
        bing = f"https://bing.com/?q={b}"
        await self.inline.form(
            text=self.strings("isearch"),
            message=message,
            reply_markup=[
                [
                    {
                        "text": self.strings("link"),
                        "url": bing,
                    }
                ],
                [{"text": self.strings("close"), "action": "close"}],
            ],
            silent=True,
        )

    @loader.command(
        ru_doc="Поискать в You инлайн",
        en_doc="Search on You inline",
    )
    async def iyou(self, message: Message):
        y = utils.get_args_raw(message)
        you = f"https://you.com/?q={y}"
        await self.inline.form(
            text=self.strings("isearch"),
            message=message,
            reply_markup=[
                [
                    {
                        "text": self.strings("link"),
                        "url": you,
                    }
                ],
                [{"text": self.strings("close"), "action": "close"}],
            ],
            silent=True,
        )

    async def close(self, call):
        """Callback button"""
        await call.delete()
