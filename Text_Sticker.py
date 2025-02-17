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
# Name: Text in sticker
# Description: Text in sticker
# Author: @hikka_mods
# Commands:
# .st <hex color> [text]
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# scope: Text in sticker
# scope: Text in sticker 0.0.1
# requires: requests
# ---------------------------------------------------------------------------------

import io
from textwrap import wrap

import requests
from PIL import Image, ImageColor, ImageDraw
from PIL import ImageFont

from .. import loader, utils


@loader.tds
class TextinstickerMod(loader.Module):
    """Text to sticker"""

    strings = {
        "name": "Text in sticker",
        "error": "white st <color name> [text]",
    }

    strings_ru = {
        "error": "Укажите .st <color name> [text]",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "font",
                "https://github.com/CodWize/ReModules/blob/main/assets/Samson.ttf?raw=true",
                lambda: "add a link to the font you want",
            )
        )

    @loader.command(
        ru_doc="<название цвета> [текст]",
        en_doc="<color name> [text]",
    )
    @loader.owner
    async def stcmd(self, message):
        await message.delete()
        text = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if not text:
            if not reply:
                text = self.strings("error")
            elif not reply.message:
                text = self.strings("error")
            else:
                text = reply.raw_text
        color_name = text.split(" ", 1)[0].lower()
        color = None
        if len(text.split(" ", 1)) > 1:
            text = text.split(" ", 1)[1]
        else:
            if reply and reply.message:
                text = reply.raw_text
        try:
            color = ImageColor.getrgb(color_name)
        except ValueError:
            color = (255, 255, 255)
        txt = []
        for line in text.split("\n"):
            txt.append("\n".join(wrap(line, 30)))
        text = "\n".join(txt)
        bytes_font = requests.get(self.config["font"]).content
        font = io.BytesIO(bytes_font)
        font = ImageFont.truetype(font, 100)
        image = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        w, h = draw.multiline_textsize(text=text, font=font)
        image = Image.new("RGBA", (w + 100, h + 100), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.multiline_text((50, 50), text=text, font=font, fill=color, align="center")
        output = io.BytesIO()
        output.name = f"{color_name}.webp"
        image.save(output, "WEBP")
        output.seek(0)
        await self.client.send_file(message.to_id, output, reply_to=reply)
