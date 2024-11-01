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

from ..inline.types import InlineQuery  # type: ignore
from .. import loader, utils

__version__ = (1, 0, 0)


@loader.tds
class InlineButtonMod(loader.Module):
    """Create inline button"""

    strings = {
        "name": "InlineButton",
        "titles": "Create a message with the Inline Button",
    }

    strings_ru = {"titles": "Создай сообщение с Inline Кнопкой"}

    @loader.command(
        ru_doc="Создать inline кнопку\nНапример: @username_bot crinl Текст сообщения, Текст кнопки, Ссылка в кнопке",
        en_doc="Create an inline button\nexample: @username_bot crinl Message text, Button text, Link in the button",
    )
    async def crinl_inline_handler(self, query: InlineQuery):
        args = utils.get_args_raw(query.query)
        if args:
            args_list = args.split(",")
            if len(args_list) == 3:
                message = args_list[0].strip()
                name = args_list[1].strip()
                url = args_list[2].strip()

            return {
                "title": self.strings("titles"),
                "description": f"{message}, {name}, {url}",
                "message": message,
                "reply_markup": [{"text": name, "url": url}],
            }
