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
# Name: KBSwapper
# Description: KBSwapper is a module for changing the keyboard layout
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# scope: KBSwapper
# scope: KBSwapper 0.0.1
# ---------------------------------------------------------------------------------

from telethon.types import Message
from .. import loader, utils

EN_TO_RU = str.maketrans(
    "qwertyuiop[]asdfghjkl;'zxcvbnm,./" +
    "QWERTYUIOP{}ASDFGHJKL:\"ZXCVBNM<>?",
    "йцукенгшщзхъфывапролджэячсмитьбю." +
    "ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,"
)

RU_TO_EN = str.maketrans(
    "йцукенгшщзхъфывапролджэячсмитьбю." +
    "ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,",
    "qwertyuiop[]asdfghjkl;'zxcvbnm,./" +
    "QWERTYUIOP{}ASDFGHJKL:\"ZXCVBNM<>?"
)

@loader.tds
class KBSwapperMod(loader.Module):
    """KBSwapper is a module for changing the keyboard layout"""

    strings = {
        "name": "KBSwapper",
        "no_reply": "<emoji document_id=5774077015388852135>❌</emoji> <b>Пожалуйста, ответьте на сообщение.</b>",
        "original_message": "<emoji document_id=5260450573768990626>➡️</emoji> <b>Original message:</b> {original}",
        "fixed_message": "<emoji document_id=5774022692642492953>✅</emoji> <b>Fixed message:</b> {fixed}",
    }
    strings_ru = {
        "no_reply": "<emoji document_id=5774077015388852135>❌</emoji> <b>Пожалуйста, ответьте на сообщение.</b>",
        "original_message": "<emoji document_id=5260450573768990626>➡️</emoji> <b>Оригинальное сообщение:</b> {original}",
        "fixed_message": "<emoji document_id=5774022692642492953>✅</emoji> <b>Исправленное сообщение:</b> {fixed}",
    }

    @loader.command(
        ru_doc="При ответе на своё сообщение меняет раскладку путем редактирования, на чужое — в отдельном сообщении.",
        en_doc="Change keyboard layout for the replied message.",
    )
    async def swap(self, message: Message):
        reply = await message.get_reply_message()
        if not reply:
            await utils.answer(message, self.strings("no_reply"))
            return

        original_text = reply.text
        if not original_text:
            await utils.answer(message, self.strings("no_reply"))
            return

        en_count = sum(1 for c in original_text if c in "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM")
        ru_count = sum(1 for c in original_text if c in "йцукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ")

        if en_count > ru_count:
            fixed_text = original_text.translate(EN_TO_RU)
        else:
            fixed_text = original_text.translate(RU_TO_EN)

        
        if reply.from_id == message.from_id:
            await reply.edit(fixed_text)
        else:
            await utils.answer(
                message,
                "{}\n{}".format(
                    self.strings("original_message").format(original=original_text),
                    self.strings("fixed_message").format(fixed=fixed_text),
                ),
            )
