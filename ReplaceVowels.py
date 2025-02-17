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
# Name: VowelReplacer
# Description: Replaces vowel letters with ё
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# scope: VowelReplacer
# scope: VowelReplacer 0.0.1
# ---------------------------------------------------------------------------------

from telethon.tl.types import Message

from .. import loader, utils


@loader.tds
class VowelReplacer(loader.Module):
    """Replaces vowel letters with ё"""

    strings = {
        "name": "Vowel Replacer",
        "on": "✅ Vowel substitution for ё has been successfully enabled.",
        "off": "🚫 Vowel substitution for ё is disabled.",
    }

    strings_ru = {
        "on": "✅ Замена гласных на ё успешно включена.",
        "off": "🚫 Замена гласных на ё отключена.",
    }

    async def client_ready(self, client, db):
        self.db = db
        self._client = client
        self.enabled = self.db.get("vowel_replacer", "enabled", False)

    @loader.command(
        ru_doc="Включить или отключить замену гласных на ё.",
        en_doc="Enable or disable vowel substitution for ё.",
    )
    async def vowelreplace(self, message):
        self.enabled = not self.enabled
        self.db.set("vowel_replacer", "enabled", self.enabled)

        if self.enabled:
            response = self.strings("on")
        else:
            response = self.strings("off")

        await utils.answer(message, response)

    async def watcher(self, message: Message):
        """Автоматическая замена гласных на ё при получении собственного сообщения."""
        if self.enabled and message.out:
            vowels = "аеёиоуыэюяАЕЁИОУЫЭЮЯ"
            message_text = message.text
            replaced_text = "".join(
                "ё" if char in vowels else char for char in message_text
            )

            await message.edit(replaced_text)
