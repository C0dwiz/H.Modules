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
# Name: InlineButton
# Description: Create inline button
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# scope: InlineButton
# scope: InlineButton 0.0.1
# ---------------------------------------------------------------------------------

import asyncio
from ..inline.types import InlineQuery

from .. import loader, utils


@loader.tds
class InlineButtonMod(loader.Module):
    """Create inline button"""

    strings = {
        "name": "InlineButton",
        "titles": "Create a message with the Inline Button",
        "error_title": "Error",
        "error_description": "Invalid input format. Please provide exactly three comma-separated values.",
        "error_message": "Make sure your input is formatted as: message, name, url.",
    }

    strings_ru = {
        "titles": "Создай сообщение с Inline Кнопкой",
        "error_title": "Ошибка",
        "error_description": "Неверный формат ввода. Пожалуйста, укажите ровно три значения, разделенных запятыми.",
        "error_message": "Убедитесь, что ваш ввод имеет следующий формат: сообщение, имя, url.",
    }

    @loader.command(
        ru_doc="Создать inline кнопку\nНапример: @username_bot crinl Текст сообщения, Текст кнопки, Ссылка в кнопке",
        en_doc="Create an inline button\nexample: @username_bot crinl Message text, Button text, Link in the button",
    )
    async def crinl_inline_handler(self, query: InlineQuery):
        args = utils.get_args_raw(query.query)

        if args:
            args_list = [arg.strip() for arg in args.split(",")]

            if len(args_list) == 3:
                message, name, url = args_list

                return {
                    "title": self.strings("titles"),
                    "description": f"{message}, {name}, {url}",
                    "message": message,
                    "reply_markup": [{
                        "text": name,
                        "url": url
                    }]
                }

        return {
            "title": self.strings("error_title"),
            "description": self.strings("error_description"),
            "message": self.strings("error_message"),
        }