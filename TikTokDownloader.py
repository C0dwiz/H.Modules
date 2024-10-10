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
# Description: A module for downloading videos from TikTok without a watermark
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# scope: Api TikTokDownloader
# scope: Api TikTokDownloader 0.0.1
# ---------------------------------------------------------------------------------

from tiktok_downloader import snaptik
import tempfile
import os

from .. import loader, utils


@loader.tds
class TikTokDownloaderMod(loader.Module):
    """A module for downloading videos from TikTok without a watermark"""

    strings = {
        "name": "TikTokDownloader",
        "args_no": "<emoji document_id=5465665476971471368>❌</emoji> Specify the link to the TikTok video",
        "download": "<emoji document_id=5899757765743615694>⬇️</emoji> Uploading a video...",
        "done": "<emoji document_id=5280662183057825163>🎥</emoji> Your video from TikTok",
        "error": "<emoji document_id=5465665476971471368>❌</emoji> Error downloading video: {str(e)}",
    }

    strings_ru = {
        "args_no": "<emoji document_id=5465665476971471368>❌</emoji> Укажите ссылку на видео TikTok",
        "download": "<emoji document_id=5899757765743615694>⬇️</emoji> Загрузка видео...",
        "done": "<emoji document_id=5280662183057825163>🎥</emoji> Ваше видео с TikTok",
        "error": "<emoji document_id=5465665476971471368>❌</emoji> Ошибка при скачивании видео: {str(e)}",
    }

    @loader.command(
        ru_doc="Скачивает видео с TikTok по ссылке",
        en_doc="Downloads videos from TikTok via the link",
    )
    async def ttdlcmd(self, message):
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings("args_no"))
            return

        await utils.answer(message, self.strings("download"))

        try:
            get_video = snaptik(f"{args}")
            get_video_list = list(get_video)

            with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_file:
                get_video_list[0].download(temp_file.name)
                temp_file_path = temp_file.name

            with open(temp_file_path, "rb") as video:
                await message.client.send_file(
                    message.to_id, video, caption=self.strings("done")
                )

            os.remove(temp_file_path)
            await message.delete()

        except Exception as e:
            await utils.answer(message, self.strings("error").format(e=e))
