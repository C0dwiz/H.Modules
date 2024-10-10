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
# Name: animals
# Description: Random cats and dogs
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# scope: Api animals
# scope: Api animals 0.0.1
# requires: requests
# ---------------------------------------------------------------------------------

from hikkatl.types import Message
import requests

from .. import loader, utils

__version__ = (1, 0, 0)


@loader.tds
class animals(loader.Module):
    """Random cats and dogs"""

    strings = {
        "name": "animals",
        "loading": "<b>Generation is underway</b>",
        "done": "<b>Here is your salute</b>",
    }

    strings_ru = {
        "loading": "<b>Генерация идет полным ходом</b>",
        "done": "<b>Вот ваш результат</b>",
    }

    @loader.command(
        ru_doc="Файлы случайных фотографий кошек",
        en_doc="Random photos of cats files",
    )
    async def fcatcmd(self, message: Message):
        await utils.answer(message, self.strings("loading"))
        response = requests.get("https://api.thecatapi.com/v1/images/search")
        cat_url = response.json()[0]["url"]
        await utils.answer_file(
            message, cat_url, self.strings("done"), force_document=True
        )

    @loader.command(
        ru_doc="Случайные фотографии собачьих файлов",
        en_doc="Random photos of dog files",
    )
    async def fdogcmd(self, message: Message):
        await utils.answer(message, self.strings("loading"))
        response = requests.get("https://api.thedogapi.com/v1/images/search")
        dog_url = response.json()[0]["url"]
        await utils.answer_file(
            message, dog_url, self.strings("done"), force_document=True
        )

    @loader.command(
        ru_doc="Случайные фотографии кошек",
        en_doc="Random photos of cats",
    )
    async def catcmd(self, message: Message):
        await utils.answer(message, self.strings("loading"))
        response = requests.get("https://api.thecatapi.com/v1/images/search")
        cat_url = response.json()[0]["url"]
        await utils.answer_file(
            message, cat_url, self.strings("done"), force_document=False
        )

    @loader.command(
        ru_doc="Случайные фотографии собаки",
        en_doc="Random photos of dog",
    )
    async def dogcmd(self, message: Message):
        await utils.answer(message, self.strings("loading"))
        response = requests.get("https://api.thedogapi.com/v1/images/search")
        dog_url = response.json()[0]["url"]
        await utils.answer_file(
            message, dog_url, self.strings("done"), force_document=False
        )
