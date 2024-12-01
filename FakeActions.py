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
# Name: FakeActions
# Description: Module for simulating various actions in chat
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# scope: Api FakeActions
# scope: Api FakeActions 0.0.1
# ---------------------------------------------------------------------------------

import asyncio

from telethon import events
from .. import loader, utils


@loader.tds
class FakeActionsMod(loader.Module):
    """Module for simulating various actions in chat"""

    strings = {"name": "FakeActions"}

    def __init__(self):
        self.config = loader.ModuleConfig(
            "DEFAULT_DURATION", 5, "Default duration for actions in seconds"
        )

    async def ftcmd(self, message):
        """<seconds> - Simulates typing in chat for the specified number of seconds."""
        await self._simulate_action_command(message, "typing")

    async def ffcmd(self, message):
        """<seconds> - Simulates sending a file."""
        await self._simulate_action_command(message, "document")

    async def fgcmd(self, message):
        """<seconds> - Simulates recording a voice message."""
        await self._simulate_action_command(message, "record-audio")

    async def fvgcmd(self, message):
        """<seconds> - Simulates recording a video message."""
        await self._simulate_action_command(message, "record-round")

    async def fpgcmd(self, message):
        """<seconds> - Simulates playing a game."""
        await self._simulate_action_command(message, "game")

    async def _simulate_action_command(self, message, action):
        """General function for handling action simulation commands."""
        duration = self._parse_duration(message)
        if duration is None:
            await utils.answer(
                message,
                f"Usage: {self.get_prefix()}{message.raw_text.split()[0][1:]} <seconds>",
            )
            return

        await message.delete()
        await self._simulate_action(message, action, duration)

    def _parse_duration(self, message):
        """Parse the duration from the message."""
        args = message.raw_text.split()
        if len(args) == 2 and args[1].isdigit():
            return int(args[1])
        return self.config["DEFAULT_DURATION"]

    async def _simulate_action(self, message, action, duration):
        """Simulate the specified action in chat."""
        async with message.client.action(message.chat_id, action):
            await asyncio.sleep(duration)
