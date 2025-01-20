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
# Name: Text2File
# Description: Module for convertation your text to file
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# scope: Text2File
# scope: Text2File 0.0.1
# ---------------------------------------------------------------------------------

import io

from .. import loader, utils


@loader.tds
class Text2File(loader.Module):
    """Module for convertation your text to file"""

    strings = {
        "name": "Text2File",
        "no_args": "Don't have any args! Use .ttf text/code",
        "cfg_name": "You can change the extension and file name",
    }

    strings_ru = {
        "no_args": "Недостаточно аргументов! Используйте: .ttf текст/код",
        "cfg_name": "Вы можете выбрать расширение и название для файла",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "name",
                "file.txt",
                lambda: self.strings("cfg_name"),
            ),
        )

    @loader.command(
        ru_doc="Создать файл с вашим текстом или кодом",
        en_doc="Create a file with your text or code",
    )
    async def ttfcmd(self, message):
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings("no_args"))
        else:
            text = args
            by = io.BytesIO(text.encode("utf-8"))
            by.name = self.config["name"]

            await utils.answer_file(
                message,
                by,
                reply_to=getattr(message, "reply_to_msg_id", None),
            )
