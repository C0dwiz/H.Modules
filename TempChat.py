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
# Name: TempChat
# Description: Creates a temporary private chat with a message forwarding restriction and adds the specified user to it.
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# scope: TempChat
# scope: TempChat 0.0.1
# ---------------------------------------------------------------------------------

from .. import loader, utils
from hikkatl import functions
from datetime import datetime as dt
import logging, re, asyncio

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


@loader.tds
class TempChatMod(loader.Module):
    """Creates a temporary private chat with a message forwarding restriction and adds the specified user to it."""

    strings = {
        "name": "TempChat",
        "selfchat": "You can't create a chat with yourself.",
        "wrongargs": "<emoji document_id=5980953710157632545>❌</emoji> <b>Wrong arguments. Use </b><code>.tmpchat [@user/reply] [time]</code><b>",
        "alreadychatting": "<emoji document_id=5980953710157632545>❌</emoji> <b>You already have an active conversation with this person.</b>",
        "invalidtime": "<emoji document_id=5980953710157632545>❌</emoji> <b>Invalid time format. Use combinations like 1h30m.</b>",
        "invitemsg": "<emoji document_id=5818967120213445821>🛡</emoji> You've been invited to a temporary private chat!\n\n<emoji document_id=5451646226975955576>⌛️</emoji> Auto-deletes in ",
        "joinlink": "🔗 Join link: ",
        "chatcreated": "<emoji document_id=5980930633298350051>✅</emoji> The temporary chat has been successfully created!"
    }

    strings_ru = {
        "selfchat": "Ты не можешь создать чат сам с собой.",
        "wrongargs": "<emoji document_id=5980953710157632545>❌</emoji> <b>Неверные аргументы. Используй </b><code>.tmpchat [@user/reply] [время]</code>",
        "alreadychatting": "<emoji document_id=5980953710157632545>❌</emoji> <b>У вас уже есть открытая переписка с этим человеком.</b>",
        "invalidtime": "<emoji document_id=5980953710157632545>❌</emoji> <b>Неверный формат времени. Убедитесь, что вы вводите время в формате 1h, 2h30m.</b>",
        "invitemsg": "<emoji document_id=5818967120213445821>🛡</emoji> Вы были приглашены во временный приватный чат!\n\n<emoji document_id=5451646226975955576>⌛️</emoji> Авто-удаление через ",
        "joinlink": "🔗 Ссылка: ",
        "chatcreated": "<emoji document_id=5980930633298350051>✅</emoji> Временный чат успешно создан!"
    }

    def __init__(self):
        self.temp_chats = {}

    def parse_time(self, time_str):
        time_units = {'d': 86400, 'h': 3600, 'm': 60, 's': 1}
        if not re.fullmatch(r'(\d+[dhms])+', time_str):
            return None
        seconds = 0
        matches = re.findall(r'(\d+)([dhms])', time_str)
        for amount, unit in matches:
            seconds += int(amount) * time_units[unit]
        return seconds if seconds > 0 else None

    async def check_expired_chats(self):
        while True:
            now = dt.now().timestamp()
            for chat_id in list(self.temp_chats.keys()):
                if self.temp_chats[chat_id][1] <= now:
                    try:
                        await self.client(functions.channels.DeleteChannelRequest(chat_id))
                        del self.temp_chats[chat_id]
                        self.set('temp_chats', self.temp_chats)
                    except Exception as e:
                        logger.error(f"Error deleting chat {chat_id}: {e}")
                        try: self.client(functions.channels.GetFullChannelRequest(channel=chat_id))
                        except Exception:
                            del self.temp_chats[chat_id]
                            self.set('temp_chats', self.temp_chats)
            await asyncio.sleep(30)

    async def client_ready(self, client, db):
        self.temp_chats = self.get('temp_chats', {})
        asyncio.create_task(self.check_expired_chats())

    @loader.command(
        ru_doc="Создает временный чат. Использование: .tmpchat [@user/reply] [time]"
    )
    async def tmpchat(self, message):
        """Create temporary chat. Usage: .tmpchat [@user/reply] [time]"""
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()

        if reply:
            user = await self.client.get_entity(reply.sender_id)
            time_str = args.strip() if args else None
        else:
            parts = args.split(',', 1) if ',' in args else args.rsplit(' ', 1)
            if len(parts) != 2:
                return await utils.answer(message, self.strings["wrongargs"])
            user_str, time_str = parts[0].strip(), parts[1].strip()
            try:
                user = await self.client.get_entity(user_str)
            except Exception:
                return await utils.answer(message, self.strings["wrongargs"])

        if not time_str:
            return await utils.answer(message, self.strings["wrongargs"])
        seconds = self.parse_time(time_str)
        if not seconds:
            return await utils.answer(message, self.strings["invalidtime"])

        if any(user.id == uid for uid, _ in self.temp_chats.values()):
            return await utils.answer(message, self.strings["alreadychatting"])

        try:
            created = await self.client(functions.channels.CreateChannelRequest(
                title=f'TempChat #{user.id}',
                about=f'Temporary private chat with {user.id} | Expires after: {time_str}',
                megagroup=True
            ))
            chat_id = created.chats[0].id
            expires_at = dt.now().timestamp() + seconds

            await self.client(functions.messages.ToggleNoForwardsRequest(
                peer=chat_id,
                enabled=True
            ))

            self.temp_chats[chat_id] = (user.id, expires_at)
            self.set('temp_chats', self.temp_chats)

            invite = await self.client(functions.messages.ExportChatInviteRequest(
                peer=chat_id,
                usage_limit=1
            ))
            invite_message = self.strings["invitemsg"] + time_str + f"\n{self.strings['joinlink']} {invite.link}"
            await self.client.send_message(
                user.id,
                invite_message
            )
            await utils.answer(message, self.strings['chatcreated'])

        except Exception as e:
            logger.error(f"Error creating temp chat: {e}")
            await utils.answer(message, "❌ Error! Check log-chat.")
