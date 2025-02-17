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
# Name: AutofarmCookies
# Description: Autofarm in the bot @cookies_game_bot
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# scope: AutofarmCookies
# scope: AutofarmCookies 0.0.1
# ---------------------------------------------------------------------------------

import random

from datetime import timedelta
from telethon import functions

from .. import loader, utils

__version__ = (1, 0, 0)


@loader.tds
class AutofarmCookiesMod(loader.Module):
    """Autofarm in the bot @cookies_game_bot"""

    strings = {
        "name": "AutofarmCookies",
        "farmon": (
            "<i>The deferred task has been created, autofarming has been started, everything will start in 10 minutes"
            " seconds...</i>"
        ),
        "farmon_already": "<i>It has already been launched :)</i>",
        "farmoff": "<i>The autopharm is stopped\nSelected:</i> <b>%coins% Cookies</b>",
        "farm": "<i>I typed:</i> <b>%coins% Cookies</b>",
    }

    strings_ru = {
        "farmon": (
            "<i>Отложенная задача создана, автофарминг запущен, всё начнётся через 10"
            " секунд...</i>"
        ),
        "farmon_already": "<i>Уже запущено :)</i>",
        "farmoff": "<i>Автофарм остановлен.\nНвброно:</i> <b>%coins% Cookies</b>",
        "farm": "<i>Я набрал:</i> <b>%coins% Cookies</b>",
    }

    def __init__(self):
        self.name = self.strings["name"]

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self.myid = (await client.get_me()).id
        self.cookies = "@cookies_game_bot"

    @loader.command(
        ru_doc="Запустить автофарминг",
        en_doc="Launch auto-farming",
    )
    async def cookon(self, message):
        status = self.db.get(self.name, "status", False)
        if status:
            return await message.edit(self.strings["farmon_already"])
        self.db.set(self.name, "status", True)
        await self.client.send_message(
            self.cookies, "/cookie", schedule=timedelta(seconds=10)
        )
        await message.edit(self.strings["farmon"])

    @loader.command(
        ru_doc="Остановить автофарминг",
        en_doc="Stop auto-farming",
    )
    async def cookoff(self, message):
        self.db.set(self.name, "status", False)
        coins = self.db.get(self.name, "coins", 0)
        if coins:
            self.db.set(self.name, "coins", 0)
        await message.edit(self.strings["farmoff"].replace("%coins%", str(coins)))

    @loader.command(
        ru_doc="Вывод кол-ва коинов, добытых этим модулем",
        en_doc="Output of the number of coins mined by this module",
    )
    async def cookies(self, message):
        coins = self.db.get(self.name, "coins", 0)
        await message.edit(self.strings["farm"].replace("%coins%", str(coins)))

    async def watcher(self, event):
        if not isinstance(event, Message):
            return
        chat = utils.get_chat_id(event)
        if chat != self.cookies:
            return
        status = self.db.get(self.name, "status", False)
        if not status:
            return
        if event.raw_text == "/cookie":
            return await self.client.send_message(
                self.cookies, "/cookie", schedule=timedelta(hours=2)
            )
        if event.sender_id != self.cookies:
            return
        if "🙅‍♂️!" in event.raw_text:
            args = [int(x) for x in event.raw_text.split() if x.isnumeric()]
            randelta = random.randint(20, 60)
            if len(args) == 4:
                delta = timedelta(
                    hours=args[1], minutes=args[2], seconds=args[3] + randelta
                )
            elif len(args) == 3:
                delta = timedelta(minutes=args[1], seconds=args[2] + randelta)
            elif len(args) == 2:
                delta = timedelta(seconds=args[1] + randelta)
            else:
                return
            sch = (
                await self.client(
                    functions.messages.GetScheduledHistoryRequest(self.cookies, 1488)
                )
            ).messages
            await self.client(
                functions.messages.DeleteScheduledMessagesRequest(
                    self.cookies, id=[x.id for x in sch]
                )
            )
            return await self.client.send_message(
                self.cookies, "/cookie", schedule=delta
            )
        if "✨" in event.raw_text:
            args = event.raw_text.split()
            for x in args:
                if x[0] == "+":
                    return self.db.set(
                        self.name,
                        "coins",
                        self.db.get(self.name, "coins", 0) + int(x[1:]),
                    )

    async def message_q(
        self,
        text: str,
        user_id: int,
        mark_read: bool = False,
        delete: bool = False,
    ):
        async with self.client.conversation(user_id) as conv:
            msg = await conv.send_message(text)
            response = await conv.get_response()
            if mark_read:
                await conv.mark_read()

            if delete:
                await msg.delete()
                await response.delete()

            return response

    @loader.command(
        ru_doc="Показывает ваш мешок",
        en_doc="Shows your bag",
    )
    async def me(self, message):
        bot = "@cookies_game_bot"
        bags = await self.message_q(
            "/me",
            bot,
            delete=True,
        )

        args = utils.get_args_raw(message)

        if not args:
            await utils.answer(message, bags.text)

    @loader.command(
        ru_doc="Помощь по модулю AutofarmCookies",
        en_doc="Help with the AutofarmCookies module",
    )
    async def ckies(self, message):
        chelp = """
            🍀| <b>Помощь по командам:</b>
            .cookon - Включает авто фарм.
            .cookoff - Выключает авто фарм.
            .farm - Показывает сколько вы нафармили.
            .me - Показывает ваш ммешок"""
        await utils.answer(message, chelp)
