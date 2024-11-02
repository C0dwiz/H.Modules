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
# Name: InlineHelper
# Description: Basic management of the UB in case only the inline works
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# scope: InlineHelper
# scope: InlineHelper 0.0.1
# ---------------------------------------------------------------------------------

import sys
import os
import asyncio
import logging

from ..inline.types import InlineQuery

from .. import loader, utils, main


@loader.tds
class InlineHelperMod(loader.Module):
    """Basic management of the UB in case only the inline works"""

    strings = {
        "name": "InlineHelper",
        "call_restart": "Restarting...",
        "call_update": "Updating...",
        "res_prefix": "Successfully reset prefix to default",
        "restart_inline_handler_title": "Restart Userbot",
        "restart_inline_handler_description": "Restart your userbot via inline",
        "restart_inline_handler_message": "Press the button below to restart your userbot",
        "restart_inline_handler_reply_text": "Restart",
        "update_inline_handler_title": "Update Userbot",
        "update_inline_handler_description": "Update your userbot via inline",
        "update_inline_handler_message": "Press the button below to update your userbot",
        "update_inline_handler_reply_text": "Update",
        "terminal_inline_handler_title": "Command Executed!",
        "terminal_inline_handler_description": "Command executed successfully",
        "terminal_inline_handler_message": "Command {text} executed successfully in terminal",
        "modules_inline_handler_title": "Modules",
        "modules_inline_handler_description": "List all installed modules",
        "modules_inline_handler_result": "☘️ Installed modules:\n",
        "resetprefix_inline_handler_title": "Reset Prefix",
        "resetprefix_inline_handler_description": "Reset your prefix back to default",
        "resetprefix_inline_handler_message": "Are you sure you want to reset your prefix to default dot?",
        "resetprefix_inline_handler_reply_text_yes": "Yes",
        "resetprefix_inline_handler_reply_text_no": "No",
    }

    strings_ru = {
        "call_restart": "Перезагружаю...",
        "call_update": "Обновляю...",
        "res_prefix": "Префикс успешно сброшен по умолчанию",
        "restart_inline_handler_title": "Перезагрузить юзербота",
        "restart_inline_handler_description": "Перезагрузить юзербота через инлайн",
        "restart_inline_handler_message": "<b>Нажмите на кнопку ниже для рестарта юзербота</b>",
        "restart_inline_handler_reply_text": "Перезапуск",
        "update_inline_handler_title": "Обновить юзербота",
        "update_inline_handler_description": "Обновить юзербота через инлайн",
        "update_inline_handler_message": "<b>Нажмите на кнопку ниже для обновления юзербота</b>",
        "update_inline_handler_reply_text": "Обновить",
        "terminal_inline_handler_title": "Команда выполнена!",
        "terminal_inline_handler_description": "Команда завершена.",
        "terminal_inline_handler_message": "Команда <code>{text}</code> была успешно выполнена в терминале",
        "modules_inline_handler_title": "Модули",
        "modules_inline_handler_description": "Вывести список установленных моудей",
        "modules_inline_handler_result": "☘️ Все установленные модули:\n",
        "resetprefix_inline_handler_title": "Сбросить префикс",
        "resetprefix_inline_handler_description": "Сбросить префикс по умолчанию",
        "resetprefix_inline_handler_message": "Вы действительно хотите сбросить ваш префикс и установить стандартную точку?",
        "resetprefix_inline_handler_reply_text_yes": "Да",
        "resetprefix_inline_handler_reply_text_no": "Нет",
    }

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    async def restart(self, call):
        """Restart callback"""
        logging.error("InlineHelper: restarting userbot...")
        await call.edit(self.strings("call_restart"))
        await sys.exit(0)

    async def update(self, call):
        """Update callback"""
        logging.error("InlineHelper: updating userbot...")
        os.system(f"cd {utils.get_base_dir()} && cd .. && git reset --hard HEAD")
        os.system("git pull")
        await call.edit(self.strings("call_update"))
        await sys.exit(0)

    async def reset_prefix(self, call):
        """Reset prefix"""
        self.db.set(main.__name__, "command_prefix", ".")
        await call.edit(self.strings("res_prefix"))

    @loader.command(
        ru_doc="Перезагрузить юзербота",
        en_doc="Reboot the userbot",
    )
    async def restart_inline_handler(self, _: InlineQuery):
        return {
            "title": self.strings("restart_inline_handler_title"),
            "description": self.strings("restart_inline_handler_description"),
            "message": self.strings("restart_inline_handler_message"),
            "reply_markup": [
                {
                    "text": self.strings("restart_inline_handler_reply_text"),
                    "callback": self.restart,
                }
            ],
        }

    @loader.command(
        ru_doc="Обновить юзербота",
        en_doc="Update the userbot",
    )
    async def update_inline_handler(self, _: InlineQuery):
        return {
            "title": self.strings("update_inline_handler_title"),
            "description": self.strings("update_inline_handler_description"),
            "message": self.strings("update_inline_handler_message"),
            "reply_markup": [
                {
                    "text": self.strings("update_inline_handler_reply_text"),
                    "callback": self.update,
                }
            ],
        }

    @loader.command(
        ru_doc="Выполнить команду в терминале (лучше сразу подготовить команду и просто вставить)",
        en_doc="Execute the command in the terminal (it is better to prepare the command immediately and just paste it)",
    )
    async def terminal_inline_handler(self, _: InlineQuery):
        text = query.args

        await asyncio.create_subprocess_shell(
            f"{text}",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=utils.get_base_dir(),
        )

        return {
            "title": self.strings("terminal_inline_handler_title"),
            "description": self.strings("terminal_inline_handler_description"),
            "message": self.strings("terminal_inline_handler_message").format(
                text=text
            ),
        }

    @loader.command(
        ru_doc="Вывести список установленных модулей через инлайн",
        en_doc="Display a list of installed modules via the inline",
    )
    async def modules_inline_handler(self, _: InlineQuery):
        result = self.strings("modules_inline_handler_result")

        for mod in self.allmodules.modules:
            try:
                name = mod.strings["name"]
            except KeyError:
                name = mod.__clas__.__name__
            result += f"• {name}\n"

        return {
            "title": self.strings("modules_inline_handler_title"),
            "description": self.strings("modules_inline_handler_description"),
            "message": result,
        }

    @loader.command(
        ru_doc="Сбросить префикс (осторожнее, сбрасывает ваш префикс на . )",
        en_doc="Reset the prefix (be careful, resets your prefix to . )",
    )
    async def resetprefix_inline_handler(self, _: InlineQuery):
        return {
            "title": self.strings("resetprefix_inline_handler_title"),
            "description": self.strings("resetprefix_inline_handler_description"),
            "message": self.strings("resetprefix_inline_handler_message"),
            "reply_markup": [
                {
                    "text": self.strings("resetprefix_inline_handler_reply_text_yes"),
                    "callback": self.reset_prefix,
                },
                {
                    "text": self.strings("resetprefix_inline_handler_reply_text_no"),
                    "action": "close",
                },
            ],
        }
