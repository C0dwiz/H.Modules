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
# Name: NoVoice
# Description: A module for prohibiting the sending of voice and video messages
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# scope: NoVoice
# scope: NoVoice 0.0.1
# ---------------------------------------------------------------------------------

from telethon.tl.custom import Message

from .. import loader, utils


@loader.tds
class NoVoiceMod(loader.Module):
    """A module for prohibiting the sending of voice and video messages"""

    strings = {
        "name": "NoVoice",
        "novoice_true": "❌ Voice messages are disabled for all users!",
        "novoice_false": "✅ Voice messages are allowed for all users again!",
        "novoice_no_args": "Usage: .novoice [on/off]",
        "novoiceuser_no_reply": "Usage: .novoiceuser [username/reply]",
        "novoiceuser_true": "❌ User {user_id} is now forbidden to send voice messages!",
        "novoicerm_no_reply": "Usage: .novoicerm [username/reply]",
        "novoicerm_yes": "✅ User {user_id} is now allowed to send voice messages again!",
        "novoicerm_no": "⚠️ User {user_id} not found in the banned list.",
        "text": "❌ I do not accept voice messages!",
    }

    strings_ru = {
        "novoice_true": "❌ Голосовые сообщения отключены для всех пользователей!",
        "novoice_false": "✅ Голосовые сообщения снова разрешены для всех пользователей!",
        "novoice_no_args": "Использование: .novoice [on/off]",
        "novoiceuser_no_reply": "Использование: .novoiceuser [username/reply]",
        "novoiceuser_true": "❌ Пользователю {user_id} запрещено отправлять голосовые сообщения!",
        "novoicerm_no_reply": "Использование: .novoicerm [username/reply]",
        "novoicerm_yes": "✅ Пользователю {user_id} снова разрешено отправлять голосовые сообщения!",
        "novoicerm_no": "⚠ Пользователь {user_id} не найден в списке запрещенных.",
        "text": "❌ Я не принимаю голосовые сообщения!",
    }

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self.novoice_global = self.db.get("NoVoice", "global", False)
        self.banned_users = self.db.get("NoVoice", "banned_users", {})

    @loader.command(
        ru_doc="[on/off] — запрещает/разрешает всем пользователям отправку голосовых и видеосообщений.",
        en_doc="[on/off] — prohibits/allows all users to send voice and video messages.",
    )
    async def novoice(self, message):
        args = utils.get_args_raw(message)
        if args == "on":
            self.novoice_global = True
            self.db.set("NoVoice", "global", self.novoice_global)
            await utils.answer(message, self.strings("novoice_true"))
        elif args == "off":
            self.novoice_global = False
            self.db.set("NoVoice", "global", self.novoice_global)
            await utils.answer(message, self.strings("novoice_false"))
        else:
            await utils.answer(message, self.strings("novoice_no_args"))

    @loader.command(
        ru_doc="[username/reply] — запрещает пользователю отправку голосовых и видеосообщений.",
        en_doc="[username/reply] — prohibits the user from sending voice and video messages.",
    )
    async def novoiceuser(self, message):
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if not args and not reply:
            return await utils.answer(message, self.strings("novoiceuser_no_reply"))

        if reply:
            user_id = reply.from_id
        else:
            user = await self.client.get_entity(args)
            user_id = user.id

        self.banned_users[user_id] = True
        self.db.set("NoVoice", "banned_users", self.banned_users)
        await utils.answer(
            message, self.strings("novoiceuser_true").format(user_id=user_id)
        )

    @loader.command(
        ru_doc="[username/reply] — разрешает пользователю отправку голосовых и видеосообщений.",
        en_doc="[username/reply] — allows the user to send voice and video messages.",
    )
    async def novoicerm(self, message):
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()

        if not args and not reply:
            return await utils.answer(message, self.strings("novoicerm_no_reply"))

        user_id = None
        if reply:
            user_id = reply.sender_id
        else:
            try:
                user = await self.client.get_entity(args)
                user_id = user.id
            except Exception as e:
                logger.error(f"Failed to get entity for {args}: {e}")

        if user_id in self.banned_users:
            del self.banned_users[user_id]
            self.db.set("NoVoice", "banned_users", self.banned_users)
            await utils.answer(
                message, self.strings("novoicerm_yes").format(user_id=user_id)
            )
        else:
            await utils.answer(
                message, self.strings("novoicerm_no").format(user_id=user_id)
            )

    async def watcher(self, message: Message):
        """Обрабатывает входящие сообщения"""
        if (
            isinstance(message, Message)
            and not message.out
            and message.is_private
            and (self.novoice_global or message.sender_id in self.banned_users)
            and (message.voice or message.video_note)
        ):
            await message.delete()
            await utils.answer(message, self.strings("text"))

            logger.debug(
                "Deleted voice/video message from user %s in chat %s",
                message.sender_id,
                message.chat_id,
            )
