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
# Name: BirthdayTime
# Description: Counting down to your birthday
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# scope: BirthdayTime
# scope: Api BirthdayTime 0.0.1
# ---------------------------------------------------------------------------------

import random
import asyncio
import calendar
from datetime import datetime

from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.errors.rpcerrorlist import UserPrivacyRestrictedError

from .. import loader, utils

D_MSG = [
    "Ждешь его?",
    "Осталось немного)",
    "Дни пролетят, даже не заметишь",
    "Уже знаешь что хочешь получить в подарок?)",
    "Сколько исполняется?",
    "Жду не дождусь уже",
]


@loader.tds
class DaysToMyBirthday(loader.Module):
    """Counting down to your birthday"""

    strings = {
        "name": "BirthdayTime",
        "date_error": "<emoji document_id=5422840512681877946>❗️</emoji> <b>Your birthdate is not specified in the config, please correct this :)</b>",
        "msg": (
            "<emoji document_id=5377476217698001788>🎉</emoji> <b>"
            "There are {} days, {} hours, {} minutes, and {} seconds left until your birthday. \n<emoji document_id=5377442914521588226>"
            "💙</emoji> {}</b>"
        ),
        "conf": "<i>Open config...</i>",
        "name_changed": "<b>Name updated!</b>",
        "name_not_changed": "<b>Name was not updated.</b>",
        "name_privacy_error": "<b>Unable to change name due to privacy settings.</b>",
        "error": "<b>An error occurred. Please check the logs.</b>",
    }

    strings_ru = {
        "date_error": "<emoji document_id=5422840512681877946>❗️</emoji> <b>В конфиге не указан день вашего рождения, пожалуйста, исправь это :)</b>",
        "msg": (
            "<emoji document_id=5377476217698001788>🎉</emoji> <b>"
            "До вашего дня рождения осталось {} дней, {} часов, {} "
            "минут, {} секунд. \n<emoji document_id=5377442914521588226>"
            "💙</emoji> {}</b>"
        ),
        "conf": "<i>Открываю конфиг...</i>",
        "btname_yes": (
            "<b><emoji document_id=6327560044845991305>😶</emoji> Хорошо, теперь я "
            "буду изменять ваше имя в зависимости от количества дней до дня рождения</b>"
        ),
        "btname_no": "<emoji document_id=6325696222313055607>😶</emoji>Хорошо, я больше не буду изменять ваше имя",
        "name_changed": "<b>Имя обновлено!</b>",
        "name_not_changed": "<b>Имя не было обновлено.</b>",
        "name_privacy_error": "<b>Не удалось изменить имя из-за настроек приватности.</b>",
        "error": "<b>Произошла ошибка. Пожалуйста, проверьте логи.</b>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "birthday_date",
                None,
                lambda: "Дата вашего рождения. Указывать только день",
                validator=loader.validators.Integer(),
            ),
            loader.ConfigValue(
                "birthday_month",
                None,
                "Месяц вашего рождения",
                validator=loader.validators.Choice(
                    [
                        "January",
                        "February",
                        "March",
                        "April",
                        "May",
                        "June",
                        "July",
                        "August",
                        "September",
                        "October",
                        "November",
                        "December",
                    ]
                ),
            ),
        )
        self._task = None

    async def client_ready(self):
        if self._task:
            self._task.cancel()

        self._task = asyncio.create_task(self.checker())

    async def checker(self):
        while True:
            if not self.db.get(__name__, "change_name", False):
                await asyncio.sleep(60)
                continue
            try:
                now = datetime.now()
                day = self.config["birthday_date"]
                monthy = self.config["birthday_month"]
                month = list(calendar.month_name).index(monthy)
                birthday = datetime(now.year, month, day)

                if now.month > month or (now.month == month and now.day > day):
                    birthday = datetime(now.year + 1, month, day)

                time_to_birthday = abs(birthday - now)
                days = time_to_birthday.days

                user = await self.client(GetFullUserRequest(self.client.hikka_me.id))
                if not user or not user.users:
                    await asyncio.sleep(60)
                    continue

                name = user.users[0].last_name or ""

                ln = f'{self.db.get(__name__, "last_name", "")} • {days} d.'
                if name == ln:
                    await asyncio.sleep(60)
                    continue
                else:
                    await self.client(UpdateProfileRequest(last_name=ln))
                    self.db.set(__name__, "last_name", name)
            except UserPrivacyRestrictedError:
                self.db.set(__name__, "change_name", False)
                print("Error: Can't change name due to privacy settings.")
            except Exception as e:
                print(f"Error in checker: {e}")
            finally:
                await asyncio.sleep(60)

    @loader.command(
        ru_doc="Выставить таймер дней в ник (нестабильно)",
        en_doc="Set the timer of days in the nickname (unstable)",
    )
    async def btname(self, message):
        try:
            user = await self.client(GetFullUserRequest(self.client.hikka_me.id))
            name = user.users[0].last_name or ""
        except Exception as e:
            print(f"Error getting user info: {e}")
            await utils.answer(message, self.strings("error"))
            return

        self.db.set(__name__, "last_name", name)
        change_name = self.db.get(__name__, "change_name", False)

        if change_name:
            self.db.set(__name__, "change_name", False)
            await utils.answer(message, self.strings("btname_no"))
            try:
                await self.client(
                    UpdateProfileRequest(last_name=self.db.get(__name__, "last_name"))
                )
                await utils.answer(message, self.strings("name_not_changed"))
            except UserPrivacyRestrictedError:
                await utils.answer(message, self.strings("name_privacy_error"))
            except Exception as e:
                print(f"Error removing name: {e}")
                await utils.answer(message, self.strings("error"))

        else:
            self.db.set(__name__, "change_name", True)
            await utils.answer(message, self.strings("btname_yes"))

    @loader.command(
        ru_doc="Вывести таймер",
        en_doc="Display the timer",
    )
    async def bt(self, message):
        if (
            self.config["birthday_date"] is None
            or self.config["birthday_month"] is None
        ):
            await utils.answer(message, self.strings("date_error"))
            msg = await self.client.send_message(message.chat_id, self.strings("conf"))
            await self.allmodules.commands["config"](
                await utils.answer(msg, f"{self.get_prefix()}config BirthdayTime")
            )
            return

        try:
            now = datetime.now()
            day = self.config["birthday_date"]
            monthy = self.config["birthday_month"]
            month = list(calendar.month_name).index(monthy)
            birthday = datetime(now.year, month, day)

            if now.month > month or (now.month == month and now.day > day):
                birthday = datetime(now.year + 1, month, day)

            time_to_birthday = abs(birthday - now)

            await utils.answer(
                message,
                self.strings("msg").format(
                    time_to_birthday.days,
                    (time_to_birthday.seconds // 3600),
                    (time_to_birthday.seconds // 60 % 60),
                    (time_to_birthday.seconds % 60),
                    random.choice(D_MSG),
                ),
            )

        except Exception as e:
            print(f"Error in bt command: {e}")
            await utils.answer(message, self.strings("error"))
