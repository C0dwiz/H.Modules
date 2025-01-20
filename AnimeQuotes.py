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
# Name: AnimeQuotes
# Description: A module for sending random quotes from anime
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# scope: AnimeQuotes
# scope: AnimeQuotes 0.0.1
# requires: requests
# ---------------------------------------------------------------------------------

import logging
import requests

from .. import loader, utils


@loader.tds
class AnimeQuotesMod(loader.Module):
    """A module for sending random quotes from anime"""

    strings = {
        "name": "AnimeQuotes",
        "quote_template": (
            '<b>Quote:</b> "{quote}"\n\n'
            "<b>Character:</b> {character}\n"
            "<b>Anime:</b> {anime}"
        ),
        "error": "<b>Couldn't get a quote. Try again later!</b>",
    }

    strings_ru = {
        "quote_template": (
            '<b>Цитата:</b> "{quote}"\n\n'
            "<b>Персонаж:</b> {character}\n"
            "<b>Аниме:</b> {anime}"
        ),
        "error": "<b>Не удалось получить цитату. Попробуйте позже!</b>",
    }

    @loader.command(
        ru_doc="Получить случайную цитату из аниме",
        en_doc="Get a random quote from the anime",
    )
    async def quote(self, message):
        url = "https://animechan.io/api/v1/quotes/random"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response.raise_for_status()
                    data = await response.json()

                    quote_content = data["data"]["content"]
                    character_name = data["data"]["character"]["name"]
                    anime_name = data["data"]["anime"]["name"]

                    quote = self.strings["quote_template"].format(
                        quote=quote_content, character=character_name, anime=anime_name
                    )
                    await utils.answer(message, quote)

        except aiohttp.ClientError as e:
            await utils.answer(message, self.strings["error"])