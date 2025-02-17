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
# Name: NumbersAPI
# Description: Many interesting facts about numbers.
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# scope: NumbersAPI
# scope: NumbersAPI 0.0.1
# ---------------------------------------------------------------------------------

import aiohttp
from datetime import datetime

from .. import loader, utils


async def get_fact_about_number(number, fact_type):
    url = f"http://numbersapi.com/{number}/{fact_type}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.text()
            else:
                return "Извините, не удалось получить факт."

async def get_fact_about_date(month, day):
    date_str = datetime.now().replace(month=month, day=day).strftime("%m/%d")
    url = f"http://numbersapi.com/{date_str}/date"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.text()
            else:
                return "Извините, не удалось получить факт."


@loader.tds
class NumbersAPI(loader.Module):
    """Many interesting facts about numbers."""

    strings = {"name": "NumbersAPI"}

    @loader.command(
        ru_doc="Дает интересный факт про число или дату\nНапример: .num 10 math или .num 01.01 date",
        en_doc="Gives an interesting fact about a number or date\nexample: .num 10 math or .num 01.01 date",
    )
    async def num(self, message):
        args = utils.get_args_raw(message).split()

        if len(args) < 2:
            await utils.answer(message, "Использование: .num <число или дата> <тип>")
            return

        num_or_date = args[0]
        fact_type = args[1]

        if "." in num_or_date:
        try:
                month, day = map(int, num_or_date.split("."))
                result = await get_fact_about_date(month, day)
            except ValueError:
                await utils.answer(message, "Ошибка: некорректный формат даты. Используйте: месяц.день")
                return
        else:
            try:
                number = int(num_or_date)
                result = await get_fact_about_number(number, fact_type)
            except ValueError:
                await utils.answer(message, "Ошибка: некорректный ввод числа.")
            return

        await utils.answer(message, result)