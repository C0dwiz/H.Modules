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
# Name: TikTokDownloader
# Description: A module for downloading videos and photos from TikTok without watermark
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# scope: Api TikTokDownloader
# scope: Api TikTokDownloader 0.0.1
# ---------------------------------------------------------------------------------

import aiohttp
import asyncio
import re
import os
import warnings
import functools
import logging

from dataclasses import dataclass
from urllib.parse import urljoin
from typing import Union, Optional, Literal, List
from tqdm import tqdm
from bs4 import BeautifulSoup
import requests
from .. import loader, utils


@dataclass
class data:
    dir_name: str
    media: Union[str, List[str]]
    type: str


class TikTok:
    def __init__(self, host: Optional[str] = None):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) "
            "Version/4.0.4 Mobile/7B334b Safari/531.21.10"
        }
        self.host = host or "https://www.tikwm.com/"
        self.session = aiohttp.ClientSession()

        self.data_endpoint = "api"
        self.search_videos_keyword_endpoint = "api/feed/search"
        self.search_videos_hashtag_endpoint = "api/challenge/search"

        self.link = None
        self.result = None

        self.logger = logging.getLogger("damirtag-TikTok")
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "[damirtag-TikTok:%(funcName)s]: %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def _warn(reason: str = "This function is NOT used but may be useful"):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                warnings.warn(
                    f"Warning! Deprecated: {func.__name__}\nReason: {reason}",
                    category=DeprecationWarning,
                    stacklevel=2,
                )
                return func(*args, **kwargs)

            return wrapper

        return decorator

    async def close_session(self):
        await self.session.close()

    async def _ensure_data(self, link: str):
        try:
            if self.result is None or self.link != link:
                self.link = link
                self.result = await self.fetch(link)
                self.logger.info("Successfully ensured data from the link")
        except Exception as e:
            self.logger.error(f"Error occurred when trying to get data from tikwm: {e}")
            raise

    async def __getimages(self, download_dir: Optional[str] = None):
        download_dir = download_dir or self.result["id"]
        os.makedirs(download_dir, exist_ok=True)
        tasks = [
            self._download_file(url, os.path.join(download_dir, f"image_{i + 1}.jpg"))
            for i, url in enumerate(self.result["images"])
        ]
        await asyncio.gather(*tasks)
        self.logger.info(f"Images - Downloaded and saved photos to {download_dir}")

        return data(
            dir_name=download_dir,
            media=[
                os.path.join(download_dir, f"image_{i + 1}.jpg")
                for i in range(len(self.result["images"]))
            ],
            type="images",
        )

    async def __getvideo(self, video_filename: Optional[str] = None, hd: bool = False):
        video_url = self.result["hdplay"] if hd else self.result["play"]
        video_filename = video_filename or f"{self.result['id']}.mp4"

        async with self.session.get(video_url) as response:
            response.raise_for_status()
            total_size = int(response.headers.get('content-length', 0))
            with open(video_filename, 'wb') as file:
                with tqdm(total=total_size, unit='B', unit_scale=True,
                                                         desc=video_filename) as pbar:
                    async for chunk in response.content.iter_any():
                        file.write(chunk)
                        pbar.update(len(chunk))

        self.logger.info(f"Video - Downloaded and saved video as {video_filename}")

        return data(
            dir_name=os.path.dirname(video_filename), media=video_filename, type="video"
        )

    async def _makerequest(self, endpoint: str, params: dict) -> dict:
        async with self.session.get(
            urljoin(self.host, endpoint), params=params, headers=self.headers
        ) as response:
            response.raise_for_status()
            data = await response.json()
            return data.get("data", {})

    @staticmethod
    def get_url(text: str) -> Optional[str]:
        urls = re.findall(r"http[s]?://[^\s]+", text)
        return urls[0] if urls else None

    @_warn()
    async def convert_share_urls(self, url: str) -> Optional[str]:
        url = self.get_url(url)
        if "@" in url:
            return url
        async with self.session.get(
            url, headers=self.headers, allow_redirects=False
        ) as response:
            if response.status == 301:
                return response.headers["Location"].split("?")[0]
        return None

    @_warn()
    async def get_tiktok_video_id(self, original_url: str) -> Optional[str]:
        original_url = await self.convert_share_urls(original_url)
        matches = re.findall(r"/video|v|photo/(\d+)", original_url)
        return matches[0] if matches else None

    async def fetch(self, link: str) -> dict:
        url = self.get_url(link)
        params = {"url": url, "hd": 1}
        return await self._makerequest(self.data_endpoint, params=params)

    async def _download_file(self, url: str, path: str):
        async with self.session.get(url) as response:
            response.raise_for_status()
            with open(path, "wb") as file:
                while chunk := await response.content.read(1024):
                    file.write(chunk)

    async def download_sound(
        self,
        link: Union[str],
        audio_filename: Optional[str] = None,
        audio_ext: Optional[str] = ".mp3",
    ):
        await self._ensure_data(link)

        if not audio_filename:
            audio_filename = f"{self.result['music_info']['title']}{audio_ext}"
        else:
            audio_filename += audio_ext

        await self._download_file(self.result["music_info"]["play"], audio_filename)
        self.logger.info(f"Sound - Downloaded and saved sound as {audio_filename}")
        return audio_filename

    async def download(
        self, link: Union[str], video_filename: Optional[str] = None, hd: bool = False
    ) -> data:
        """
        Asynchronously downloads a TikTok video or photo post.

        Args:
            video_filename (Optional[str]): The name of the file for the TikTok video or photo. If None, the file will be named based on the video or photo ID.
            hd (bool): If True, downloads the video in HD format. Defaults to False.

        Returns:
            dir_name (str): Directory name
            media (Union[str, List[str]]): Full list of downloaded media
            type (str): The type of downloaded objects: Images or video

        Raises:
            Exception: No downloadable content found in the provided link.

        """
        await self._ensure_data(link)
        if "images" in self.result:
            self.logger.info("Starting to download images")
            return await self.__getimages(video_filename)
        elif "hdplay" in self.result or "play" in self.result:
            self.logger.info("Starting to download video.")
            return await self.__getvideo(video_filename, hd)
        else:
            self.logger.error("No downloadable content found in the provided link.")
            raise Exception("No downloadable content found in the provided link.")

    def _get_video_link(self, unique_id: str, aweme_id: str) -> str:
        return f"https://www.tiktok.com/@{unique_id}/video/{aweme_id}"

    def _get_uploader_link(self, unique_id: str) -> str:
        return f"https://www.tiktok.com/@{unique_id}"


@loader.tds
class TikTokDownloader(loader.Module):
    """TikTok Downloader module"""

    strings = {
        "name": "TikTokDownloader",
        "downloading": "<emoji document_id=5436024756610546212>⚡</emoji> <b>Downloading…</b>",
        "success_photo": "<emoji document_id=5436246187944460315>❤️</emoji> <b>The photo(s) has/have been successfully downloaded!</b>!",
        "success_video": "<emoji document_id=5436246187944460315>❤️</emoji> <b>The video has been successfully downloaded!</b>",
        "error": "Error occurred while downloading.\n{}",
    }

    strings_ru = {
        "downloading": "<emoji document_id=5436024756610546212>⚡</emoji> <b>Загружаем…</b>",
        "success_photo": "<emoji document_id=5436246187944460315>❤️</emoji> <b>Фотография(-и) была(-и) успешно загружены!</b>!",
        "success_video": "<emoji document_id=5436246187944460315>❤️</emoji> <b>Видео было успешно загружено!</b>",
        "error": "Во время загрузки произошла ошибка.\n{}",
    }

    @loader.command(
        ru_doc="Скачать видео или фото с TikTok",
        en_doc="Download videos or photos from TikTok",
    )
    async def tt(self, message):
        args = utils.get_args(message)
        if not args:
            await utils.answer(message, "Please provide a TikTok URL.")
            return

        url = args[0]
        await utils.answer(message, self.strings("downloading"))

        tiktok_downloader = TikTok()
        await message.delete()

        try:
            download_result = await tiktok_downloader.download(url)

            if download_result.type == "video":
                await message.client.send_file(message.to_id, download_result.media, caption=self.strings("success_video"))
            elif download_result.type == "images":
                await message.client.send_file(message.to_id, download_result.media, caption=self.strings("success_photo"))

        except Exception as e:
            await utils.answer(message, self.strings("error").format(e))
        finally:
            await tiktok_downloader.close_session()
