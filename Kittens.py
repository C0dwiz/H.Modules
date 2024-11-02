# Proprietary License Agreement

# Copyright (c) 2024-29 CodWiz

# Permission is hereby granted to any person obtaining a copy of this software and associated documentation files (the "Software"), to use the Software for personal and non-commercial purposes, subject to the following conditions:

# 1. The Software may not be modified, altered, or otherwise changed in any way without the explicit written permission of the author.

# 2. Redistribution of the Software, in original or modified form, is strictly prohibited without the explicit written permission of the author.

# 3. The Software is provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and non-infringement. In no event shall the author or copyright holder be liable for any claim, damages, or other liability, whether in an action of contract, tort, or otherwise, arising from, out of, or in connection with the Software or the use or other dealings in the Software.

# 4. Any use of the Software must include the above copyright notice and this permission notice in all copies or substantial portions of the Software.

# 5. By using the Software, you agree to be bound by the terms and conditions of this license.

# For any inquiries or requests for permissions, please contact codwiz@yandex.ru.

# Name: Kittens
# Description: Module for search cutie kitties from @catslovemeow
# Author: @nervousmods
# Commands:
# .kit
# ---------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------
# meta developer: @nervousmods, @hikka_mods
# scope: hikka_only
# scope: hikka_min 1.4.2
# -----------------------------------------------------------------------------------

import datetime
import random
import time

from telethon import functions

from .. import loader

__version__ = (1, 0, 0)


@loader.tds
class Kittens(loader.Module):
    """Module for search cutie kitties from @catslovemeow"""

    strings = {
        "name": "Kittens",
        "search": "<emoji document_id=5328311576736833844>🔴</emoji> Search cutie kitties..",
    }

    strings = {
        "name": "Kittens",
        "search": "<emoji document_id=5328311576736833844>🔴</emoji> Ищем милых котят..",
    }

    @loader.command(
        ru_doc="Чтобы завести милую кошечку",
        en_doc="To get a cute kitty",
    )
    async def kit(self, message):
        await message.edit(self.strings("search"))
        time.sleep(1)
        chat = "kanalskotami"
        result = await message.client(
            functions.messages.GetHistoryRequest(
                peer=chat,
                offset_id=0,
                offset_date=datetime.datetime.now(),
                add_offset=random.choice(range(1, 101, 2)),
                limit=1,
                max_id=0,
                min_id=0,
                hash=0,
            ),
        )
        await message.delete()
        await message.client.send_file(message.to_id, result.messages[0].media)
