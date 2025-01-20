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
# Name: ASCIIArt
# Description: Converting images to ASCII art
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# scope: ASCIIArt
# scope: ASCIIArt 0.0.1
# requires: pillow
# ---------------------------------------------------------------------------------

import os
import tempfile

from PIL import Image
from .. import loader, utils


@loader.tds
class ASCIIArtMod(loader.Module):
    """Converting images to ASCII art"""

    strings = {
        "name": "ASCIIArt",
        "no_media_reply": "<b>Please reply to the image!</b>",
        "loading": "<emoji document_id=5116240346656801621>❓</emoji> <b>Converting an image to ASCII...</b>",
        "error": "<emoji document_id=5121063440311386962>👎</emoji> <b>Error when converting an image.</b>",
        "done": "<emoji document_id=5123163417326126159>✅</emoji> <b>Here is your ASCII art:</b>",
    }

    strings_ru = {
        "no_media_reply": "<b>Пожалуйста, ответьте на изображение!</b>",
        "loading": "<emoji document_id=5116240346656801621>❓</emoji> <b>Конвертирую изображение в ASCII...</b>",
        "error": "<emoji document_id=5121063440311386962>👎</emoji> <b>Ошибка при конвертации изображения.</b>",
        "done": "<emoji document_id=5123163417326126159>✅</emoji> <b>Вот ваш ASCII-арт:</b>",
    }

    @loader.command(
        ru_doc="<реплай на изображение> сделать ascii art",
        en_doc="<replay on image> make ascii art",
    )
    async def cascii(self, message):
        reply = await message.get_reply_message()
        if not self._is_image(reply):
            await utils.answer(message, self.strings("no_media_reply"))
            return

        await utils.answer(message, self.strings("loading"))
        ascii_art = await self._generate_ascii_art(reply)

        if ascii_art:
            await self._send_ascii_file(message, ascii_art)
            await message.delete()
        else:
            await utils.answer(message, self.strings("error"))

    def _is_image(self, reply):
        """Проверка, является ли ответ изображением"""
        return reply and (
            reply.photo
            or (reply.document and reply.file.mime_type.startswith("image/"))
        )

    async def _generate_ascii_art(self, reply):
        """Генерирует ASCII-арт из изображения"""
        try:
            image_path = await reply.download_media(tempfile.gettempdir())
            if not image_path:
                return None
            with Image.open(image_path) as img:
                img = img.convert("L")
                img = img.resize(self._get_new_dimensions(img), Image.NEAREST)

                chars = "@#S%?*+;:,. "
                pixels = img.getdata()

                ascii_str = "".join(chars[pixel // 25] for pixel in pixels)
                return "\n".join(
                    ascii_str[i : i + img.width]
                    for i in range(0, len(ascii_str), img.width)
                )

        except Exception as e:
            print(f"Error generating ASCII art: {e}")
            return None
        finally:
            if image_path and os.path.exists(image_path):
                os.remove(image_path)

    def _get_new_dimensions(self, img):
        """Получаем новые размеры для изображения"""
        new_width = 100
        aspect_ratio = img.height / img.width
        new_height = int(aspect_ratio * new_width * 0.55)
        return new_width, new_height

    async def _send_ascii_file(self, message, ascii_art):
        """Сохраняет ASCII-арт во временный файл и отправляет его"""
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", encoding="utf-8", suffix=".txt", delete=False
            ) as tmp_file:
                tmp_file_path = tmp_file.name
                tmp_file.write(ascii_art)

            await message.client.send_file(
                message.chat_id,
                tmp_file_path,
                caption=self.strings("done"),
                force_document=True,
                reply_to=getattr(message, "reply_to_msg_id", None),
            )
        finally:
            if tmp_file_path and os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)
