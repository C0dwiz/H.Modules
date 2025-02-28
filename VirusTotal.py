# Proprietary License Agreement

# Copyright (c) 2024-29 CodWiz

# Permission is hereby granted to any person obtaining a copy of this software and associated documentation files (the "Software"), to use the Software for personal and non-commercial purposes, subject to the following conditions:

# 1. The Software may not be modified, altered, or otherwise changed in any way without the explicit written permission of the author.

# 2. Redistribution of the Software, in original or modified form, is strictly prohibited without the explicit written permission of the author.

# 3. The Software is provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and non-infringement. In no event shall the author or copyright holder be liable for any claim, damages, or other liability, whether in an action of contract, tort, or otherwise, arising from, out of or in connection with the Software or the use or other dealings in the Software.

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
import tempfile
import logging

from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.tds
class VirusTotalMod(loader.Module):
    """Checks files for viruses using VirusTotal."""

    strings = {
        "name": "VirusTotal",
        "no_file": "<emoji document_id=5210952531676504517>🚫</emoji> <b>You haven't selected a file.</b>",
        "download": "<emoji document_id=5334677912270415274>😑</emoji> <b>Downloading...</b>",
        "scan": "<emoji document_id=5325792861885570739>🫥</emoji>  <b>Scanning...</b>",
        "link": "🦠 VirusTotal Link",
        "no_virus": "✅ File is clean.",
        "error": "<emoji document_id=5463193238393274687>⚠️</emoji> Scan error.",
        "no_format": "This format is not supported.",
        "no_apikey": "<emoji document_id=5260342697075416641>🚫</emoji> You have not specified an API Key",
        "config": "Need a token with www.virustotal.com/gui/my-apikey",
        "scanning": "<emoji document_id=5325792861885570739>🫥</emoji>  <b>Waiting for scan results...</b>",
        "getting_upload_url": "<emoji document_id=5325792861885570739>🫥</emoji>  <b>Getting upload URL...</b>",
        "analysis_failed": "<emoji document_id=5463193238393274687>⚠️</emoji> Analysis failed after multiple retries.",
    }

    strings_ru = {
        "no_file": "<emoji document_id=5210952531676504517>🚫</emoji> </b>Вы не выбрали файл.</b>",
        "download": "<emoji document_id=5334677912270415274>😑</emoji> </b>Скачивание...</b>",
        "scan": "<emoji document_id=5325792861885570739>🫥</emoji>  <b>Сканирую...</b>",
        "link": "🦠 Ссылка на VirusTotal",
        "no_virus": "✅ Файл чист.",
        "error": "<emoji document_id=5463193238393274687>⚠️</emoji> Ошибка сканирования.",
        "no_format": "Этот формат не поддерживается.",
        "no_apikey": "<emoji document_id=5260342697075416641>🚫</emoji> Вы не указали Api Key",
        "config": "Need a token with www.virustotal.com/gui/my-apikey",
        "scanning": "<emoji document_id=5325792861885570739>🫥</emoji>  <b>Ожидание результатов сканирования...</b>",
        "getting_upload_url": "<emoji document_id=5325792861885570739>🫥</emoji>  <b>Получение URL для загрузки...</b>",
        "analysis_failed": "<emoji document_id=5463193238393274687>⚠️</emoji> Анализ не удался после нескольких попыток.",
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

    async def client_ready(self, client, db):
        self.hmodslib = await self.import_lib(
            "https://raw.githubusercontent.com/C0dwiz/H.Modules/refs/heads/main-fix/HModsLibrary.py"
        )

    @loader.command(
        ru_doc="<ответ на файл> - Проверяет файлы на наличие вирусов с использованием VirusTotal",
        en_doc="<file response> - Checks files for viruses using VirusTotal",
    )
    async def vt(self, message):
        if not message.is_reply:
            await utils.answer(message, self.strings("no_file"))
            return

        reply = await message.get_reply_message()
        if not reply.document:
            await utils.answer(message, self.strings("no_file"))
            return

        api_key = self.config.get("token-vt")
        if not api_key:
            await utils.answer(message, self.strings("no_apikey"))
            return

        file_extension = os.path.splitext(reply.file.name)[1].lower()
        allowed_extensions = (".jpg", ".png", ".ico", ".mp3", ".mp4", ".gif", ".txt")
        if file_extension in allowed_extensions:
            await utils.answer(message, self.strings("no_format"))
            return

        try:
            await utils.answer(message, self.strings("download"))
            with tempfile.TemporaryDirectory() as temp_dir:
                file_path = os.path.join(temp_dir, reply.file.name)
                await reply.download_media(file_path)

                file_size = os.path.getsize(file_path)
                is_large_file = file_size > 32 * 1024 * 1024

                if is_large_file:
                    await utils.answer(message, self.strings("getting_upload_url"))
                await utils.answer(message, self.strings("scan"))

                analysis_results = await self.hmodslib.scan_file_virustotal(
                    file_path, api_key, is_large_file
                )

                if analysis_results:
                    formatted_results = self.hmodslib.format_analysis_results(
                        analysis_results
                    )
                    try:
                        await self.inline.form(
                            text=formatted_results["text"],
                            message=message,
                            reply_markup={
                                "text": self.strings("link"),
                                "url": formatted_results["url"],
                            }
                            if formatted_results["url"]
                            else None,
                        )
                    except Exception as e:
                        logger.error(f"Error displaying inline results: {e}")
                        await utils.answer(
                            message,
                            self.strings("error_report").format(
                                formatted_results["url"]
                            ),
                        )

                else:
                    await utils.answer(message, self.strings("analysis_failed"))

        except Exception as e:
            logger.exception("An error occurred during the VT scan process.")
            await utils.answer(
                message, self.strings("error") + f"\n\n{type(e).__name__}: {str(e)}"
            )
