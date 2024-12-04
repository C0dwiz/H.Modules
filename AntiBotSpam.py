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
# Name: AntiBotSpam
# Description: Module to ban and delete incoming messages from spam bots
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# scope: Api AntiBotSpam
# scope: Api AntiBotSpam 0.0.1
# ---------------------------------------------------------------------------------

import re

from telethon.tl.functions.contacts import UnblockRequest
from telethon.tl.types import ChatAdminRights
from typing import Union

from .. import loader, utils
from ..inline.types import InlineCall


def format_state(state: Union[bool, None]) -> str:
    """Format the state for display."""
    return "❔" if state is None else "✅" if state else "🚫"


@loader.tds
class AntiBotSpam(loader.Module):
    """Module to ban and delete incoming messages from spam bots."""

    strings = {
        "name": "AntiBotSpam",
        "settings": "<b>Settings:</b>",
        "notify": "Report about the ban: {}",
        "del": "Delete dialogue: {}",
        "close": "Close",
        "state": "AntiBotSpam Activity: {}",
        "unbanned": "Bot {} unbanned",
    }

    strings_ru = {
        "settings": "<b>Настройки:</b>",
        "notify": "Сообщать о бане: {}",
        "del": "Удалять диалог: {}",
        "close": "Закрыть",
        "state": "Активность AntiBotSpam: {}",
        "unbanned": "Бот {} разблокирован",
    }

    def __init__(self):
        self._chat_id = None
        self._whitelist = []
        self._state = False
        self._notify = False
        self._delete = False

    async def client_ready(self, client, db):
        """Initialize settings after the client is ready."""
        self._chat_id = self.get("chat_id")
        self._whitelist = self.get("whitelist", [])
        self._state = self.get("state", False)
        self._notify = self.get("notify", False)
        self._delete = self.get("delete", False)

    async def form(self):
        """Create the inline button form for settings."""
        return [
            [
                {
                    "text": self.strings("state").format(format_state(self._state)),
                    "callback": self._setter,
                    "kwargs": {"param": "state"},
                }
            ],
            [
                {
                    "text": self.strings("notify").format(format_state(self._notify)),
                    "callback": self._setter,
                    "kwargs": {"param": "notify"},
                },
                {
                    "text": self.strings("del").format(format_state(self._delete)),
                    "callback": self._setter,
                    "kwargs": {"param": "delete"},
                },
            ],
            [
                {"text": self.strings("close"), "action": "close"},
            ],
        ]

    async def spamcmd(self, message: Message):
        """Display the configuration settings."""
        await self.inline.form(
            text=self.strings("settings"),
            # photo='',
            message=message,
            reply_markup=self.form(),
            force_me=True,
            ttl=10 * 60,
        )

    async def _setter(self, call: InlineCall, param: str):
        """Change the settings based on user input."""
        if param in ("notify", "delete"):
            current_value = getattr(self, f"_{param}")
            setattr(self, f"_{param}", not current_value)
            self.set(param, not current_value)
        else:
            self._state = not self._state
            self.set("state", self._state)

        await call.edit(
            text=self.strings("settings"), reply_markup=self.form(), force_me=True
        )

    async def unbancmd(self, message: Message):
        """Unblock a bot."""
        reply = await message.get_reply_message()
        if reply:
            identities = re.findall(r"@\w+", str(reply.message))
            if identities:
                await self._client(UnblockRequest(id=identities[0]))
                await utils.answer(
                    message, self.strings("unbanned").format(identities[0])
                )
            else:
                await utils.answer(message, "No valid bot username found in the reply.")
        else:
            await utils.answer(
                message, "Please reply to a message from the bot you want to unblock."
            )
