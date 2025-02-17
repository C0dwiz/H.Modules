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
# Name: PastebinAPI
# Description: fills in the code on pastebin
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# scope: PastebinAPI
# scope: PastebinAPI 0.0.1
# requires: aiohttp
# ---------------------------------------------------------------------------------

import aiohttp

from .. import loader, utils


@loader.tds
class PastebinAPIMod(loader.Module):
    """PastebinAPI"""

    strings = {
        "name": "PastebinAPI",
        "no_reply": (
            "<emoji document_id=5462882007451185227>🚫</emoji> You didn't specify the text"
        ),
        "no_key": "<emoji document_id=5843952899184398024>🚫</emoji> The key was not found",
        "done": "Your link with the code\n<emoji document_id=5985571061993837069>➡️</emoji> <code>{response_text}</code>",
    }

    strings_ru = {
        "no_reply": (
            "<emoji document_id=5462882007451185227>🚫</emoji> Вы не указали текст"
        ),
        "no_key": "<emoji document_id=5843952899184398024>🚫</emoji> Ключ не найден",
        "done": "Ваша ссылка с кодом\n<emoji document_id=5985571061993837069>➡️</emoji> <code>{response_text}</code>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "pastebin",
                None,
                lambda: "link to get api https://pastebin.com/doc_api#1",
                validator=loader.validators.Hidden(),
            )
        )

    @loader.command(
        ru_doc="Заливает код в Pastebin",
        en_doc="Uploads the code to Pastebin",
    )
    async def past(self, message):
        text = utils.get_args(message)

        if self.config["pastebin"] is None:
            await utils.answer(message, self.strings("no_key"))
            return

        if not text:
            await utils.answer(message, self.strings("no_reply"))
            return

        async with aiohttp.ClientSession() as Session:
            async with Session.post(
                url="https://pastebin.com/api/api_post.php",
                data={
                    "api_dev_key": self.config["pastebin"],
                    "api_paste_code": text,
                    "api_option": "paste",
                },
            ) as response:
                response_text = await response.text()

                await utils.answer(
                    message, self.strings("done").format(response_text=response_text)
                )
