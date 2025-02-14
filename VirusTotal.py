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
import aiohttp
import tempfile
import asyncio
import logging

from typing import Optional, Dict, Any

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
        "analysis_failed": "<emoji document_id=5463193238393274687>⚠️</emoji> Analysis failed after multiple retries."
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
        "analysis_failed": "<emoji document_id=5463193238393274687>⚠️</emoji> Анализ не удался после нескольких попыток."
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

    async def virustotal_request(
        self,
        session: aiohttp.ClientSession,
        url: str,
        headers: Dict[str, str],
        method: str = "GET",
        data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Generic function to make requests to the VirusTotal API.
        """
        try:
            if files:
                form = aiohttp.FormData()
                for k, v in files.items():
                    form.add_field(k, v)

                async with session.request(
                    method, url, headers=headers, data=form
                ) as response:
                    logger.debug(f"Response status: {response.status}")
                    logger.debug(f"Response body: {await response.text()}")

                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.error(
                            f"VirusTotal API request failed with status: {response.status}, reason: {response.reason}"
                        )
                        return None
            else:
                async with session.request(
                    method, url, headers=headers, json=data
                ) as response:
                    logger.debug(f"Response status: {response.status}")
                    logger.debug(f"Response body: {await response.text()}")

                    if response.status == 200:
                        return await response.json()
                    else:
                        logger.error(
                            f"VirusTotal API request failed with status: {response.status}, reason: {response.reason}"
                        )
                        return None

        except aiohttp.ClientError as e:
            logger.exception(f"AIOHTTP Client error: {e}")
            return None
        except Exception as e:
            logger.exception(f"An unexpected error occurred: {e}")
            return None

    async def get_upload_url(self, api_key: str) -> Optional[str]:
        """
        Retrieves a special upload URL for large files.
        """
        headers = {"x-apikey": api_key, "accept": "application/json"}
        url = "https://www.virustotal.com/api/v3/files/upload_url"

        async with aiohttp.ClientSession() as session:
            response = await self.virustotal_request(session, url, headers)

            if response and "data" in response and isinstance(response["data"], str):
                return response["data"]
            else:
                logger.error(f"Failed to retrieve upload URL: {response}")
                return None

    async def scan_file_virustotal(
        self, file_path: str, api_key: str, is_large_file: bool = False
    ) -> Optional[Dict[str, Any]]:
        """
        Uploads a file to VirusTotal and retrieves the analysis results. Handles files larger than 32MB.
        """
        headers = {"x-apikey": api_key}
        url = "https://www.virustotal.com/api/v3/files"

        async with aiohttp.ClientSession() as session:
            try:
                with open(file_path, "rb") as file:
                    files = {"file": file}
                    if is_large_file:
                        upload_url = await self.get_upload_url(api_key)
                        if not upload_url:
                            logger.error("Failed to get upload URL for large file.")
                            return None
                        url = upload_url

                    upload_response = await self.virustotal_request(
                        session, url, headers, method="POST", files=files
                    )

                    if (
                        upload_response
                        and "data" in upload_response
                        and "id" in upload_response["data"]
                    ):
                        analysis_id = upload_response["data"]["id"]

                        analysis_url = (
                            f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"
                        )
                        for attempt in range(20):
                            analysis_response = await self.virustotal_request(
                                session, analysis_url, headers
                            )
                            logger.debug(f"Analysis response (attempt {attempt+1}): {analysis_response}")
                            if (
                                analysis_response
                                and "data" in analysis_response
                                and "attributes" in analysis_response["data"]
                                and analysis_response["data"]["attributes"].get(
                                    "status"
                                )
                                == "completed"
                            ):
                                return analysis_response
                            await asyncio.sleep(10)

                        logger.warning(
                            f"Analysis not completed after multiple retries for ID: {analysis_id}"
                        )
                        return None

                    else:
                        logger.error(
                            f"File upload or analysis request failed: {upload_response}"
                        )
                        return None

            except FileNotFoundError:
                logger.error(f"File not found: {file_path}")
                return None
            except Exception as e:
                logger.exception(f"An error occurred during file scanning: {e}")
                return None

    def format_analysis_results(self, analysis_results: Dict[str, Any]) -> str:
        """
        Formats the analysis results into a user-friendly message, including specific detections.
        """
        if (
            not analysis_results
            or "data" not in analysis_results
            or "attributes" not in analysis_results["data"]
            or "stats" not in analysis_results["data"]["attributes"]
            or "results" not in analysis_results["data"]["attributes"]
        ):
            logger.warning(
                f"Unexpected structure in analysis_results: {analysis_results}"
            )
            return self.strings("error")

        stats = analysis_results["data"]["attributes"]["stats"]
        harmless = stats.get("harmless", 0)
        malicious = stats.get("malicious", 0)
        suspicious = stats.get("suspicious", 0)
        undetected = stats.get("undetected", 0)
        total_scans = harmless + malicious + suspicious + undetected
        analysis_id = analysis_results["data"]["id"]
        url = f"https://www.virustotal.com/gui/file-analysis/{analysis_id}"

        text = (
            f"<b>📊 VirusTotal Scan Results</b>\n\n"
            f"🦠 <b>Detections:</b> {malicious} / {total_scans}\n"
            f"🟢 <b>Harmless:</b> {harmless}\n"
            f"⚠️ <b>Suspicious:</b> {suspicious}\n"
            f"❓ <b>Undetected:</b> {undetected}\n\n"
        )

        if malicious > 0:
            text += "<b>⚠️ Detections by engine:</b>\n"
            results = analysis_results["data"]["attributes"]["results"]
            for engine, result in results.items():
                if result["category"] == "malicious":
                    engine_name = engine.replace("_", " ").title()
                    text += f"  • <b>{engine_name}:</b> {result['result']}\n"

            text += "\n"

        return {"text": text, "url": url}

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
                is_large_file = (
                    file_size > 32 * 1024 * 1024
                )

                if is_large_file:
                    await utils.answer(message, self.strings("getting_upload_url"))
                await utils.answer(message, self.strings("scan"))

                analysis_results = await self.scan_file_virustotal(
                    file_path, api_key, is_large_file
                )

                if analysis_results:
                    formatted_results = self.format_analysis_results(analysis_results)
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
                            self.strings("error_report").format(formatted_results["url"]),
                        )

                else:
                    await utils.answer(message, self.strings("analysis_failed"))

        except Exception as e:
            logger.exception("An error occurred during the VT scan process.")
            await utils.answer(
                message, self.strings("error") + f"\n\n{type(e).__name__}: {str(e)}"
                )
