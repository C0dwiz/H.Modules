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
# Name: VirusTotal
# Description: Checks files for viruses using VirusTotal
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# scope: Api VirusTotal
# scope: Api VirusTotal 0.0.1
# requires: json aiohttp tempfile
# ---------------------------------------------------------------------------------

import os
import aiohttp
import tempfile

from .. import loader, utils

__version__ = (1, 0, 0)


@loader.tds
class VirusTotalMod(loader.Module):
    """Checks files for viruses using VirusTotal"""

    strings = {
        "name": "VirusTotal",
        "no_file": "<emoji document_id=5210952531676504517>🚫</emoji> </b>You haven't selected a file.</b>",
        "download": (
            "<emoji document_id=5334677912270415274>😑</emoji> </b>Downloading...</b>"
        ),
        "skan": "<emoji document_id=5325792861885570739>🫥</emoji>  <b>Scanning...</b>",
        "link": "🦠 VirusTotal Link",
        "no_virus": "✅ File is clean.",
        "error": "Scan error.",
        "no_format": "This format is not supported.",
        "no_apikey": (
            "<emoji document_id=5260342697075416641>🚫</emoji> You have not specified an API Key"
        ),
        "confing": "Нужен токен с www.virustotal.com/gui/my-apikey",
    }

    strings_ru = {
        "no_file": "<emoji document_id=5210952531676504517>🚫</emoji> </b>Вы не выбрали файл.</b>",
        "download": (
            "<emoji document_id=5334677912270415274>😑</emoji> </b>Скачивание...</b>"
        ),
        "skan": "<emoji document_id=5325792861885570739>🫥</emoji>  <b>Сканирую...</b>",
        "link": "🦠 Ссылка на VirusTotal",
        "no_virus": "✅ Файл чист.",
        "error": "Ошибка сканирования.",
        "no_format": "Этот формат не поддерживается.",
        "no_apikey": (
            "<emoji document_id=5260342697075416641>🚫</emoji> Вы не указали Api Key"
        ),
        "confing": "Need a token with www.virustotal.com/gui/my-apikey",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "token-vt",
                None,
                lambda: "Need a token with www.virustotal.com/gui/my-apikey",
                validator=loader.validators.Hidden(),
            )
        )

    @loader.command(
        ru_doc="<ответ на файл> - Проверяет файлы на наличие вирусов с использованием VirusTotal",
        en_doc="<file response> - Checks files for viruses using VirusTotal",
    )
    async def vt(self, message):
        if not message.is_reply:
            await utils.answer(message, self.strings("no_reply"))
            return
        reply = await message.get_reply_message()
        if not reply.document:
            await utils.answer(message, self.strings("reply_not_document"))
            return
        if not self.config.get("token-vt"):
            await utils.answer(message, self.strings("no_apikey"))
            return

        async with aiohttp.ClientSession() as session:
            with tempfile.TemporaryDirectory() as temp_dir:
                await utils.answer(message, self.strings("download"))
                file_path = os.path.join(temp_dir, reply.file.name)
                await reply.download_media(file_path)
                file_extension = os.path.splitext(reply.file.name)[1].lower()
                allowed_extensions = (
                    ".jpg",
                    ".png",
                    ".ico",
                    ".mp3",
                    ".mp4",
                    ".gif",
                    ".txt",
                )
                if file_extension not in allowed_extensions:
                    try:
                        token = self.config["token-vt"]
                        headers = {"x-apikey": token}

                        with open(file_path, "rb") as file:
                            files = {"file": file}
                            async with session.post(
                                "https://www.virustotal.com/api/v3/files",
                                headers=headers,
                                data=files,
                            ) as response:
                                if response.status == 200:
                                    result = await response.json()
                                    data_id = result["data"]["id"]

                                    async with session.get(
                                        f"https://www.virustotal.com/api/v3/analyses/{data_id}",
                                        headers=headers,
                                    ) as response:
                                        if response.status == 200:
                                            result = await response.json()
                                            hash = result["meta"]["file_info"]["sha256"]
                                            detections = []
                                            for engine, details in result["data"][
                                                "attributes"
                                            ]["results"].items():
                                                if details["category"] == "malicious":
                                                    detections.append(
                                                        f"⛔️ {engine}\n ╰ {details['result']}"
                                                    )
                                            out = (
                                                "\n".join(detections)
                                                if detections
                                                else self.strings("no_virus")
                                            )
                                            url = f"https://www.virustotal.com/gui/file/{hash}/detection"
                                            await self.inline.form(
                                                text=f"Detections: {len(detections)} / {len(result['data']['attributes']['results'])}\n\n{out}\n\n",
                                                message=message,
                                                reply_markup={
                                                    "text": self.strings("link"),
                                                    "url": url,
                                                },
                                            )
                    except Exception as e:
                        await utils.answer(
                            message,
                            self.strings("error") + f"\n\n{type(e).__name__}: {str(e)}",
                        )
                else:
                    await utils.answer(message, self.strings("no_format"))
