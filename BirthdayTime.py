# ---------------------------------------------------------------------------------
# Name: BirthdayTime
# Description: Counting down to your birthday
# Author: @hikka_mods
# ---------------------------------------------------------------------------------

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# meta developer: @hikka_mods
# scope: BirthdayTime
# scope: Api BirthdayTime 0.0.1
# ---------------------------------------------------------------------------------

import random
import asyncio
from .. import loader, utils
from datetime import datetime
from datetime import timedelta
import calendar
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.account import UpdateProfileRequest

__version__ = (1, 0, 0)

d_msg = [
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
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "birthday_date",
                None,
                lambda: "Дата вашего рождения. Указывать только день",
            ),
            loader.ConfigValue(
                "birthday_month",
                None,
                "Месяц вашего рожденияbirthday_month",
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

    async def client_ready(self):
        asyncio.ensure_future(self.checker())

    async def checker(self):
        while True:
            if not self.db.get(__name__, "change_name"):
                return

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
            name = user.users[0].last_name

            ln = f'{self.db.get(__name__, "last_name")} • {days} d.'
            if name == ln:
                return
            else:
                await self.client(UpdateProfileRequest(last_name=ln))

            await asyncio.sleep(60)

    @loader.command(
        ru_doc="Выставить таймер дней в ник (нестабильно)",
        en_doc="Set the timer of days in the nickname (unstable)",
    )
    async def btname(self, message):
        user = await self.client(GetFullUserRequest(self.client.hikka_me.id))
        name = user.users[0].last_name
        if name is None:
            name = " "
        self.db.set(__name__, "last_name", name)
        if self.db.get(__name__, "change_name"):
            self.db.set(__name__, "change_name", False)
            await utils.answer(message, self.strings("btname_no"))
            await self.client(
                UpdateProfileRequest(last_name=self.db.get(__name__, "last_name"))
            )
            self.db.set(__name__, "last_name", None)
        else:
            self.db.set(__name__, "change_name", True)
            await utils.answer(message, self.strings("btname_yes"))

    @loader.command(
        ru_doc="Вывести таймер",
        en_doc="Display the timer",
    )
    async def bt(self, message):
        if self.config["birthday_date"] is None:
            await utils.answer(message, self.strings("date_error"))
            msg = await self.client.send_message(message.chat_id, self.strings("conf"))
            await self.allmodules.commands["config"](
                await utils.answer(msg, f"{self.get_prefix()}config BirthdayTime")
            )
            return

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
                random.choice(d_msg),
            ),
        )
