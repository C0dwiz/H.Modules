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
# Name: Article
# Description: Displays your article Criminal Code of the Russian Federation
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# scope: Article
# scope: Article 0.0.1
# requires: requests
# ---------------------------------------------------------------------------------

import requests
import json
import random
from typing import Dict

from .. import loader, utils


@loader.tds
class ArticleMod(loader.Module):
    """Displays your article Criminal Code of the Russian Federation"""

    strings = {
        "name": "Article",
        "article": "<emoji document_id=5226512880362332956>📖</emoji> <b>Your article of the Criminal Code of the Russian Federation</b>:\n\n<blockquote>Number {}\n\n{}</blockquote>",
    }

    strings_ru = {
        "article": "<emoji document_id=5226512880362332956>📖</emoji> <b>Твоя статья УК РФ</b>:\n\n<blockquote>Номер {}\n\n{}</blockquote>",
    }

    @loader.command(
        ru_doc="Отображается ваша статья Уголовного кодекса Российской Федерации",
        en_doc="Displays your article Criminal Code of the Russian Federation",
    )
    async def arccmd(self, message):
        if values := self._load_values():
            random_key = random.choice(list(values.keys()))
            random_value = values[random_key]
            await utils.answer(
                message, self.strings("article").format(random_key, random_value)
            )

    def _load_values(self) -> Dict[str, str]:
        url = "https://raw.githubusercontent.com/Codwizer/ReModules/main/assets/zakon.json"
        try:
            response = requests.get(url)
            if response.ok:
                data = json.loads(response.text)
                return data
        except (requests.RequestException, json.JSONDecodeError):
            pass

        return {}
