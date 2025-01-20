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
# Name: SafetyMod
# Description: generate random password
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# scope: Api SafetyMod
# scope: Api SafetyMod 0.0.1
# ---------------------------------------------------------------------------------

import random
import string

from .. import loader, utils


def generate_password(
    length: int, letters: bool = True, numbers: bool = True, symbols: bool = True
) -> str:
    """Generates a random password with customizable options.

    Args:
        length: The desired length of the password.
        letters: Include lowercase and uppercase letters (default: True).
        numbers: Include digits (default: True).
        symbols: Include common symbols (default: True).

    Returns:
        A randomly generated password string.

    Raises:
        ValueError: If all character sets are disabled (letters, numbers, symbols).
    """
    character_sets = []
    if letters:
        character_sets.append(string.ascii_letters)
    if numbers:
        character_sets.append(string.digits)
    if symbols:
        character_sets.append(string.punctuation)

    if not character_sets:
        raise ValueError("At least one of letters, numbers, or symbols must be True")

    combined_characters = "".join(character_sets)
    password = "".join(random.choice(combined_characters) for _ in range(length))
    return password


@loader.tds
class SafetyMod(loader.Module):
    """generate random password"""

    strings = {
        "name": "Safety",
        "pass": "<emoji document_id=5472287483318245416>*⃣</emoji> <b>Here is your secure password:</b> <code>{}</code>",
    }
    strings_ru = {
        "pass": "<emoji document_id=5472287483318245416>*⃣</emoji> <b>Вот ваш безопасный пароль:</b> <code>{}</code>"
    }

    @loader.command(
        ru_doc="Случайный пароль\n-n - цифры\n-s - символы \n -l - буквы",
        en_doc="Random password\n-n - numbers\n-s - symbols \n -l - letters",
    )
    async def password(self, message):
        """random password\n-n - numbers\n-s - symbols \n -l - letters"""
        text = message.text.split()
        length = 10
        letters = True
        numbers = False
        symbols = False
        for i in text:
            if i.startswith("password"):
                length = int(i.split("password")[1])
            elif i == "-n":
                numbers = True
            elif i == "-s":
                symbols = True
            elif i == "-l":
                letters = True
        password = generate_password(
            length=length, letters=letters, numbers=numbers, symbols=symbols
        )
        await utils.answer(message, self.strings("pass").format(password))
