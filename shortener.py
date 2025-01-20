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
# Name: Shortener
# Description: shortening the link
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# scope: Shortener
# scope: Shortener 0.0.1
# requires: pyshorteners
# ---------------------------------------------------------------------------------

import pyshorteners

from .. import loader, utils


@loader.tds
class Shortener(loader.Module):
    """Module for working with the api bit.ly"""

    strings = {
        "name": "Shortener",
        "no_api": "<emoji document_id=5854929766146118183>❌</emoji> You have not specified an API token from the site <a href='https://app.bitly.com/settings/api/'>bit.ly</a>",
        "statclcmd": "<emoji document_id=5787384838411522455>📊</emoji> <b>Statistics on clicks for this link:</b> {c}",
        "shortencmd": "<emoji document_id=5854762571659218443>✅</emoji> <b>Your shortened link is ready:</b> <code>{c}</code>",
    }

    strings_ru = {
        "no_api": "<emoji document_id=5854929766146118183>❌</emoji> Вы не указали api токен с сайта <a href='https://app.bitly.com/settings/api/'>bit.ly</a>",
        "statclcmd": "<emoji document_id=5787384838411522455>📊</emoji> <b>Статистика о переходе по этой ссылке:</b> {c}",
        "shortencmd": "<emoji document_id=5854762571659218443>✅</emoji> <b>Ваша сокращённая ссылка готова:</b> <code>{c}</code>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "token",
                None,
                lambda: "Need a token with https://app.bitly.com/settings/api/",
                validator=loader.validators.Hidden(),
            )
        )

    @loader.command(
        ru_doc="Сократить ссылку через bit.ly",
        en_doc="Shorten the link via bit.ly",
    )
    async def shortencmd(self, message):
        if self.config["token"] is None:
            await utils.answer(message, self.strings("no_api"))
            return

        s = pyshorteners.Shortener(api_key=self.config["token"])
        args = utils.get_args_raw(message)
        await utils.answer(
            message, self.strings("shortencmd").format(c=s.bitly.short(args))
        )

    @loader.command(
        ru_doc="Посмотреть статистику ссылки через bit.ly",
        en_doc="View link statistics via bit.ly",
    )
    async def statclcmd(self, message):
        if self.config["token"] is None:
            await utils.answer(message, self.strings("no_api"))
            return

        s = pyshorteners.Shortener(api_key=self.config["token"])
        args = utils.get_args_raw(message)
        await utils.answer(
            message, self.strings("statclcmd").format(c=s.bitly.total_clicks(args))
        )
