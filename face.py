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
# Name: face
# Description: Random face
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# scope: Api face
# scope: Api face 0.0.1
# requires: requests
# ---------------------------------------------------------------------------------

from hikkatl.types import Message  # type: ignore
import requests

from .. import loader, utils

__version__ = (1, 0, 0)


@loader.tds
class face(loader.Module):
    """random face"""

    strings = {
        "name": "face",
        "loading": (
            "<emoji document_id=5348399448017871250>🔍</emoji> I'm looking for you kaomoji"
        ),
        "random_face": (
            "<emoji document_id=5208878706717636743>🗿</emoji> Here is your random one kaomoji\n<code>{}</code>"
        ),
    }

    strings_ru = {
        "loading": (
            "<emoji document_id=5348399448017871250>🔍</emoji> Ищю вам kaomoji"
        ),
        "random_face": (
            "<emoji document_id=5208878706717636743>🗿</emoji> Вот ваш рандомный kaomoji\n<code>{}</code>"
        ),
    }

    @loader.command(
        ru_doc="Рандом kaomoji",
        en_doc="Random kaomoji",
    )
    async def rfacecmd(self, message: Message):
        await utils.answer(message, self.strings("loading"))
        response = requests.get("https://vsecoder.dev/api/faces")
        random_face = response.json()["data"]
        await utils.answer(message, self.strings("random_face").format(random_face))
