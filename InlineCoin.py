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
# Name: InlineCoin
# Description: Mini game heads or tails.
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# scope: InlineCoin
# scope: InlineCoin 0.0.1
# ---------------------------------------------------------------------------------

import random

from ..inline.types import InlineQuery

from .. import loader, utils

__version__ = (1, 0, 0)

coin = [
    "🌚 Выпал орёл!",
    "🌝 Выпала решка!",
    "🙀 Чудо, монетка осталась на ребре!",
    "🌚 Выпал орёл!",
    "🌚 Выпал орёл!",
    "🌝 Выпала решка!",
    "🌝 Выпала решка!",
]


@loader.tds
class CoinSexMod(loader.Module):
    """Mini game heads or tails"""

    strings = {
        "name": "InlineCoin",
        "titles": "Heads or tails?",
        "description": "Let's find out!",
    }

    strings_ru = {"titles": "Орёл или решка?", "description": "Давай узнаем!"}

    @loader.inline_everyone
    async def coin_inline_handler(self, query: InlineQuery):
        coinrand = random.choice(coin)
        return {
            "title": self.strings("titles"),
            "description": self.strings("description"),
            "message": f"<b>{coinrand}</b>",
            "thumb": "https://github.com/Codwizer/ReModules/blob/main/assets/images.png",
        }
