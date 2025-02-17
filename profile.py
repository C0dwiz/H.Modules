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
# Name: Profile
# Description: This module can change your Telegram profile
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# scope: Profile
# scope: Profile 0.0.1
# ---------------------------------------------------------------------------------

from telethon.errors.rpcerrorlist import UsernameOccupiedError
from telethon.tl.functions.account import UpdateProfileRequest, UpdateUsernameRequest
from .. import loader, utils


@loader.tds
class ProfileEditorMod(loader.Module):
    """This module can change your Telegram profile."""

    strings = {
        "name": "Profile",
        "error_format": "Incorrect format of args. Try again.",
        "done_name": "The new name was successfully unstalled!",
        "done_bio": "The new bio was successfully unstaled!",
        "done_username": "The new username was succesfully installed!",
        "error_occupied": "The new username is already occupied!",
    }

    strings_ru = {
        "error_format": "Неправильный формат аргумента. Попробуйте еще раз.",
        "done_name": "Новое имя успешно настроено!",
        "done_bio": "Новое био успешно настроено!",
        "done_username": "Новое имя пользователя успешно установлено!",
        "error_occupied": "Новое имя пользователя уже занято!",
    }

    @loader.command(
        ru_doc="для того, чтобы сменить свое имя/отчество",
        en_doc="for change your first/second name",
    )
    async def namecmd(self, message):
        args = utils.get_args_raw(message).split("/")

        if len(args) < 1 or len(args) > 2:
            return await utils.answer(message, self.strings("error_format"))

        firstname = args[0]
        lastname = args[1] if len(args) == 2 else ""

        await message.client(
            UpdateProfileRequest(first_name=firstname, last_name=lastname)
        )
        await utils.answer(message, self.strings("done_name"))

    @loader.command(
        ru_doc="чтобы изменить свою биографию",
        en_doc="for change your bio",
    )
    async def aboutcmd(self, message):
        args = utils.get_args_raw(message)
        if not args:
            return await utils.answer(message, self.strings("error_format"))
        await message.client(UpdateProfileRequest(about=args))
        await utils.answer(message, self.strings("done_bio"))

    @loader.command(
        ru_doc="для изменения вашего имени пользователя. Введите значение без '@'",
        en_doc="for change your username. Enter value without '@'",
    )
    async def usercmd(self, message):
        """- for change your username. Enter value without "@"."""
        args = utils.get_args_raw(message)
        if not args:
            return await utils.answer(message, self.strings("error_format"))
        try:
            await message.client(UpdateUsernameRequest(args))
            await utils.answer(message, self.strings("done_username"))
        except UsernameOccupiedError:
            await utils.answer(message, self.strings("error_occupied"))
