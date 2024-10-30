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
# Name: CheckSpamBan
# Description: Check spam ban for your account.
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# scope: CheckSpamBan
# scope: CheckSpamBan 0.0.1
# ---------------------------------------------------------------------------------

from .. import loader, utils
from ..utils import answer
from telethon.tl.types import Message

__version__ = (1, 0, 0)


@loader.tds
class SpamBanCheckMod(loader.Module):
    """Check spam ban for your account."""

    strings = {
        "name": "CheckSpamBan",
        "svo": "Your account is free from any restrictions.",
        "good": "<b>Everything is fine!You don't have a spam ban.</b>",
        "spamban": "<b>Unfortunately, your account has received a spam ban...\n\n{kk}\n\n{ll}</b>",
    }

    strings_ru = {
        "svo": "Ваш аккаунт свободен от каких-либо ограничений.",
        "good": "<b>Все прекрасно!\nУ вас нет спам бана.</b>",
        "spamban": "<b>К сожалению ваш аккаунт получил спам-бан...\n\n{kk}\n\n{ll}</b>",
    }

    @loader.command(
        ru_doc="Проверяет вашу учетную запись на спам-бан с помощью бота @SpamBot",
        en_doc="Checks your account for spam ban via @SpamBot bot",
    )
    async def spambancmd(self, message: Message):
        try:
            response = self._client.conversation("@SpamBot")

            last_message = response.messages[0]

            if last_message.message.startswith("/start"):
                if last_message.message.endswith(self.strings("svo")):
                    reply_text = self.strings("good")
                else:
                    lines = last_message.message.split("\n")
                    ban_reason = lines[2]
                    ban_duration = lines[4]
                    reply_text = self.strings("spamban").format(
                        kk=ban_reason, ll=ban_duration
                    )
                    await answer(message, reply_text)
            else:
                await answer(message, self.strings("spam_bot_error"))
        except Exception as e:
            await answer(message, self.strings("spam_bot_error"))
