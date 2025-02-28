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
# Name: EnvsSH
# Description: Module for reuploading files to envs.sh
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# scope: Api EnvsSH
# scope: Api EnvsSH 0.0.1
# requires: aiohttp
# ---------------------------------------------------------------------------------

import aiohttp

from .. import loader, utils  # pylint: disable=relative-beyond-top-level


@loader.tds
class EnvsMod(loader.Module):
    """Module for reuploading files to envs.sh"""

    strings = {
        "name": "EnvsSH",
        "connection_error": "🚫 Host is unreachable for now, try again later.",
        "no_reply": "⚠️ <b>You must reply to a message with media</b>",
        "success": "✅ URL for <code>{}</code>:\n\n<code>{}</code>",
        "error": "❌ An error occurred:\n<code>{}</code>",
        "uploading": "⏳ <b>Uploading {} ({}{})...</b>",
    }

    strings_ru = {
        "connection_error": "🚫 Хост в настоящее время недоступен, попробуйте позже.",
        "no_reply": "⚠️ <b>Вы должны ответить на сообщение с медиа</b>",
        "success": "✅ URL для <code>{}</code>:\n\n<code>{}</code>",
        "error": "❌ Произошла ошибка:\n<code>{}</code>",
        "uploading": "⏳ <b>Загрузка {} ({}{})...</b>",
    }

    async def client_ready(self, client, db):
        self.hmodslib = await self.import_lib('https://raw.githubusercontent.com/C0dwiz/H.Modules/refs/heads/main-fix/HModsLibrary.py')

    async def envcmd(self, message):
        """Reupload to envs.sh."""
        reply = await message.get_reply_message()
        if not reply or not reply.media:
            return await utils.answer(message, self.strings["no_reply"])

        size_len, size_unit = self.hmodslib.convert_size(reply.file.size)
        await utils.answer(
            message,
            self.strings["uploading"].format(reply.file.name, size_len, size_unit),
        )

        path = await self.client.download_media(reply)
        try:
            uploaded_url = await self.hmodslib.upload_to_envs(path)
        except aiohttp.ClientConnectionError:
            await utils.answer(message, self.strings["connection_error"])
        except aiohttp.ClientResponseError as e:
            await utils.answer(message, self.strings["error"].format(str(e)))
        else:
            await utils.answer(
                message, self.strings["success"].format(path, uploaded_url)
            )
