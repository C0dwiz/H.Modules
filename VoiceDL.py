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
# Name: VoiceDL
# Description: Voice Downloader module
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# scope: VoiceDL
# scope: VoiceDL 0.0.1
# requires: tempfile
# ---------------------------------------------------------------------------------

import os
import subprocess
import re
import tempfile
import time

from .. import loader, utils


@loader.tds
class VoiceDL(loader.Module):
    """Voice Downloader module"""

    strings = {
        "name": "VoiceDL",
        "download_success": "Voice message downloaded in MP3 format.",
        "download_error": "Error downloading voice message.",
        "no_voice_message": "Please reply to a voice message.",
        "conversion_error": "Error converting to MP3.",
        "file_not_found": "File not found.",
        "unsupported_format": "The file format is not supported.",
    }

    strings_ru = {
        "download_success": "Голосовое сообщение загружено в формате MP3.",
        "download_error": "Ошибка при загрузке голосового сообщения.",
        "no_voice_message": "Пожалуйста, ответьте на голосовое сообщение.",
        "conversion_error": "Ошибка при конвертации в MP3.",
        "file_not_found": "Файл не найден.",
        "unsupported_format": "Формат файла не поддерживается.",
    }

    @loader.command(
        ru_doc=" [reply] — загружает выбранное голосовое сообщение в виде файла mp3 и кидает его в чат.",
        en_doc=" [reply] — downloads the selected voice message as an MP3 file and sends it in the chat.",
    )
    async def voicedl(self, message):
        reply = await message.get_reply_message()

        if reply:
            if reply.voice:
                try:
                    with tempfile.NamedTemporaryFile(
                        delete=False, suffix=".ogg"
                    ) as temp_voice_file:
                        voice_file_path = temp_voice_file.name
                        await message.client.download_file(reply.voice, voice_file_path)

                    timestamp = int(time.time())
                    mp3_file_path = f"voice_message_{timestamp}.mp3"

                    await self.convert_to_mp3(voice_file_path, mp3_file_path)

                    await message.client.send_file(
                        message.chat.id,
                        mp3_file_path,
                        caption=self.strings("download_success"),
                    )

                    os.remove(voice_file_path)
                    os.remove(mp3_file_path)

                except FileNotFoundError:
                    await utils.answer(
                        message,
                        self.strings("download_error")
                        + " "
                        + self.strings("file_not_found"),
                    )
                except subprocess.CalledProcessError as e:
                    await utils.answer(
                        message,
                        self.strings("conversion_error") + f" {e.stderr.decode()}",
                    )
                except Exception as e:
                    await utils.answer(
                        message, self.strings("download_error") + f" {str(e)}"
                    )
            else:
                await utils.answer(message, self.strings("no_voice_message"))
        else:
            await utils.answer(message, self.strings("no_voice_message"))

    async def convert_to_mp3(self, input_file: str, output_file: str):
        """Convert audio file to MP3 format using FFmpeg."""
        command = ["ffmpeg", "-i", input_file, output_file]
        process = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        if process.returncode != 0:
            raise subprocess.CalledProcessError(
                process.returncode,
                command,
                output=process.stdout,
                stderr=process.stderr,
            )
