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
# Name: AccountData
# Description: Find out the approximate date of registration of the telegram account
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# scope: Api AccountData
# scope: Api AccountData 0.0.1
# ---------------------------------------------------------------------------------

from .. import loader, utils

@loader.tds
class AccountData(loader.Module):
    """Find out the approximate date of registration of the telegram account"""

    strings = {
        "name": "AccountData",
        "date_text": "<emoji document_id=5983150113483134607>⏰️</emoji> Date of registration of this account: {data}",
        "date_text_ps": "<emoji document_id=6028435952299413210>ℹ</emoji> The registration date is approximate, as it is almost impossible to know for sure",
        "no_reply": "<emoji document_id=6030512294109122096>💬</emoji> You did not reply to the user's message",
    }

    strings_ru = {
        "date_text": "<emoji document_id=5983150113483134607>⏰️</emoji> Дата регистрации этого аккаунта: {data}",
        "date_text_ps": "<emoji document_id=6028435952299413210>ℹ</emoji> Дата регистрации примерная, так как точно узнать практически невозможно",
        "no_reply": "<emoji document_id=6030512294109122096>💬</emoji> Вы не ответили на сообщение пользователя",
    }

    async def client_ready(self, client, db):
        self.hmodslib = await self.import_lib(
            "https://raw.githubusercontent.com/C0dwiz/H.Modules/refs/heads/main-fix/HModsLibrary.py"
        )

    @loader.command(
        ru_doc="Узнать примерную дату регистрации аккаунта телеграмм",
        en_doc="Find out the approximate date of registration of the telegram account",
    )
    async def accdata(self, message):
        if reply := await message.get_reply_message():
            data = await self.hmodslib.get_creation_date(reply.from_id)
            await utils.answer(
                message,
                f"{self.strings('date_text').format(data=data)}\n\n{self.strings('date_text_ps')}",
            )
        else:
            await utils.answer(message, self.strings("no_reply"))
