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
# Name: HModsLibrary
# Description: Library required for most H:Mods modules.
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# scope: HModsLibrary
# scope: HModsLibrary 0.0.1
# ---------------------------------------------------------------------------------

import logging
import re
import aiohttp
import random
import asyncio
import os

from bs4 import BeautifulSoup
from gigachat import GigaChat
from typing import Optional, Dict, Any
from .. import loader, utils

logger = logging.getLogger(__name__)
__version__ = (0, 0, 2)


class HModsLib(loader.Library):
    """Library required for most H:Mods modules."""

    developer = "@hikka_mods"
    version = __version__

    async def parse_time(self, time_str):
        time_units = {"d": 86400, "h": 3600, "m": 60, "s": 1}
        if not re.fullmatch(r"(\d+[dhms])+", time_str):
            return None
        seconds = 0
        matches = re.findall(r"(\d+)([dhms])", time_str)
        for amount, unit in matches:
            seconds += int(amount) * time_units[unit]
        return seconds if seconds > 0 else None

    @staticmethod
    def convert_size(size):
        """Convert file size to human-readable format."""
        power = 2**10
        n = 0
        units = {0: "B", 1: "KB", 2: "MB", 3: "GB", 4: "TB"}
        while size > power:
            size /= power
            n += 1
        return round(size, 2), units[n]

    async def upload_to_envs(self, path):
        """Upload file to envs.sh and return the URL."""
        url = "https://envs.sh"
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data={"file": open(path, "rb")}) as response:
                if response.status != 200:
                    os.remove(path)
                    raise aiohttp.ClientResponseError(
                        request_info=response.request_info,
                        history=response.history,
                        status=response.status,
                        message=await response.text(),
                        headers=response.headers,
                    )
                result = await response.text()

                os.remove(path)
                return result

    async def get_creation_date(tg_id: int) -> str:
        url = "https://restore-access.indream.app/regdate"
        headers = {
            "accept": "*/*",
            "content-type": "application/x-www-form-urlencoded",
            "user-agent": "Nicegram/92 CFNetwork/1390 Darwin/22.0.0",
            "x-api-key": "e758fb28-79be-4d1c-af6b-066633ded128",
            "accept-language": "en-US,en;q=0.9",
        }
        data = {"telegramId": tg_id}

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as response:
                if response.status == 200:
                    json_response = await response.json()
                    return json_response["data"]["date"]
                else:
                    return "Ошибка получения данных"

    async def get_giga_response(self, api_key, query):
        """Gets a response from GigaChat with the specified query."""
        async with GigaChat(
            credentials=api_key,
            scope="GIGACHAT_API_PERS",
            model=self.config["GIGACHAT_MODEL"],
            verify_ssl_certs=False,
        ) as giga:
            response = giga.chat(query)
            if response.choices:
                return response.choices[0].message.content
            return None

    async def get_giga_models(self, api_key):
        """Gets a response from GigaChat with the specified query."""
        async with GigaChat(
            credentials=api_key, scope="GIGACHAT_API_PERS", verify_ssl_certs=False
        ) as giga:
            response = giga.get_models()
            if response:
                return (
                    [model.id_ for model in response.data]
                    if hasattr(response, "data")
                    else []
                )
            return None

    async def get_random_image():
        random_site = random.randint(1, 3389)
        url = f"https://www.memify.ru/memes/{random_site}"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                content = await response.text()
                soup = BeautifulSoup(content, "html.parser")
                items = soup.find_all("div", {"class": "infinite-item card"})
                random_item = random.choice(items)
                second_a = random_item.find_all("a")[1]
                img = second_a.get("href")

        return img

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
                            logger.debug(
                                f"Analysis response (attempt {attempt + 1}): {analysis_response}"
                            )
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
