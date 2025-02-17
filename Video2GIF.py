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
# Name: Video2GIF
# Description: Converts video to GIF
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# scope: Video2GIF
# scope: Video2GIF 0.0.1
# requires: moviepy
# ---------------------------------------------------------------------------------

import os
import subprocess

from .. import loader, utils


@loader.tds
class Video2GIFModule(loader.Module):
    """Converts video to GIF"""

    strings = {
        "name": "Video2GIF",
        "conversion_success": "🎉 The conversion is completed!",
        "conversion_error": "❌ An error occurred when converting video to GIF.",
        "not_video": "⚠️ Please reply to the message with the video or send the video in one message.",
        "loading": "⏳ Conversion is underway",
    }

    strings_ru = {
        "conversion_success": "🎉 Конвертация завершена!",
        "conversion_error": "❌ Произошла ошибка при конвертации видео в GIF.",
        "not_video": "⚠️ Пожалуйста, ответьте на сообщение с видео или отправьте видео в одном сообщении.",
        "loading": "⏳ Идёт конвертация",
    }

    @loader.command(
        ru_doc="[reply | в одном сообщении с видео] — конвертирует видео в GIF.",
        en_doc="[reply | in one message with video] — Converts video to GIF.",
    )
    async def gifc(self, message):
        if reply := await message.get_reply_message():
            video = reply.video
        else:
            video = message.video

        if not video:
            await utils.answer(message, self.strings["not_video"])
            return

        await utils.answer(message, self.strings["loading"])
        video_path = await self.client.download_media(video)
        gif_path = f"{os.path.splitext(video_path)[0]}.gif"

        try:
            command = [
                "ffmpeg",
                "-i",
                video_path,
                "-vf",
                "fps=25,scale=640:-1:flags=lanczos",
                gif_path,
            ]
            subprocess.run(command, check=True)

            await message.client.send_file(
                message.chat_id, gif_path, caption=self.strings["conversion_success"]
            )

        except subprocess.CalledProcessError:
            await utils.answer(message, self.strings["conversion_error"])

        finally:
            for temp_file in [video_path, gif_path]:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
