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

import logging

from .. import loader, utils

logger = logging.getLogger(__name__)

@loader.tds
class SpamBanCheckMod(loader.Module):
    """Checks spam ban for your account."""

    strings = {
        "name": "CheckSpamBan",
    }

    @loader.command(
        ru_doc="Проверяет вашу учетную запись на спам-бан с помощью бота @SpamBot",
        en_doc="Checks your account for spam ban via @SpamBot bot",
    )
    async def spambot(self, message):
        async with self.client.conversation(178220800) as conv:
            user_message = await conv.send_message('/start')
            await user_message.delete()
            spam_message = await conv.get_response()
        await utils.answer(message, spam_message.text)
        await spam_message.delete()
