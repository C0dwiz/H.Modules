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
# Name: HAFK
# Description: Your personal assistant while you are in AFK mode
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# scope: HAFK
# scope: HAFK 0.0.1
# ---------------------------------------------------------------------------------

import datetime
import logging
import time

from telethon import types  # type: ignore

from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.tds
class HAFK(loader.Module):
    """Your personal assistant while you are in AFK mode"""

    strings = {
        "name": "HAFK",
        "afk_on": "<emoji document_id=5357107687484038897>🫶</emoji> <b>AFK mode is on!</b>",
        "afk_on_reason": "<emoji document_id=5357107687484038897>🫶</emoji> <b>AFK mode is on!</b>\n\n<b>Reason:</b> <i>{}</i>",
        "afk_here_on": "<emoji document_id=5357107687484038897>🫶</emoji> <b>AFK mode is on in this chat!</b>",
        "afk_here_on_reason": "<emoji document_id=5357107687484038897>🫶</emoji> <b>AFK mode is on in this chat!</b>\n\n<b>Reason:</b> <i>{}</i>",
        "afk_off": "<emoji document_id=5472234792659458002>🤌</emoji> <b>AFK mode is off!</b>",
        "afk_off_time": "<emoji document_id=5472234792659458002>🤌</emoji> <b>AFK mode is off!</b>\n\n<b>You were AFK for:</b> {}",
        "afk_off_here_time": "<emoji document_id=5472234792659458002>🤌</emoji> <b>AFK mode is off in this chat!</b>\n\n<b>You were AFK for:</b> {}",
        "already_afk": "<emoji document_id=5465665476971471368>❌</emoji> <b>You are already in AFK mode!</b>",
        "already_afk_here": "<emoji document_id=5465665476971471368>❌</emoji> <b>You are already in AFK mode in this chat!</b>",
        "not_afk": "<emoji document_id=5330365133745038003>😐</emoji> <b>AFK mode is already off.</b>",
        "not_afk_here": "<emoji document_id=5330365133745038003>😐</emoji> <b>AFK mode is already off in this chat.</b>",
        "afk_message": "<emoji document_id=5330130448142049118>🫤</emoji> <b>I'm currently not accepting messages!</b>\n<b>Reason:</b> <i>{}</i>\n\n<i>Inactive mode has been on for:</i> {}",
        "afk_message_reason": "<emoji document_id=5330130448142049118>🫤</emoji> <b>I'm currently not accepting messages!</b>\n<b>Reason:</b> <i>{}</i>\n\n<i>Inactive mode has been on for:</i> {}",
        "ratelimit": "<b>Please wait a bit before using this command again.</b>",
        "afk_set_failed": "<b>Failed to set AFK status. Check logs.</b>",
    }

    strings_ru = {
        "afk_on": "<emoji document_id=5357107687484038897>🫶</emoji> <b>AFK-режим включен!</b>",
        "afk_on_reason": "<emoji document_id=5357107687484038897>🫶</emoji> <b>AFK-режим включен!</b>\n\n<b>Причина:</b> <i>{}</i>",
        "afk_here_on": "<emoji document_id=5357107687484038897>🫶</emoji> <b>AFK-режим включен в этом чате!</b>",
        "afk_here_on_reason": "<emoji document_id=5357107687484038897>🫶</emoji> <b>AFK-режим включен в этом чате!</b>\n\n<b>Причина:</b> <i>{}</i>",
        "afk_off": "<emoji document_id=5472234792659458002>🤌</emoji> <b>AFK-режим отключен!</b>",
        "afk_off_time": "<emoji document_id=5472234792659458002>🤌</emoji> <b>AFK-режим отключен!</b>\n\n<b>Вы были AFK:</b> {}",
        "afk_off_here_time": "<emoji document_id=5472234792659458002>🤌</emoji> <b>AFK-режим отключен в этом чате!</b>\n\n<b>Вы были AFK:</b> {}",
        "already_afk": "<emoji document_id=5465665476971471368>❌</emoji> <b>Вы уже находитесь в AFK-режиме!</b>",
        "already_afk_here": "<emoji document_id=5465665476971471368>❌</emoji> <b>Вы уже находитесь в AFK-режиме в этом чате!</b>",
        "not_afk": "<emoji document_id=5330365133745038003>😐</emoji> <b>AFK-режим уже отключён.</b>",
        "not_afk_here": "<emoji document_id=5330365133745038003>😐</emoji> <b>AFK-режим уже отключен в этом чате.</b>",
        "afk_message": "<emoji document_id=5330130448142049118>🫤</emoji> <b>На данный момент я не принимаю сообщения!</b>\n<b>Причина:</b> <i>{}</i>\n\n<i>С момента включения режима неактивности:</i> {}",
        "afk_message_reason": "<emoji document_id=5330130448142049118>🫤</emoji> <b>На данный момент я не принимаю сообщения!</b>\n<b>Причина:</b> <i>{}</i>\n\n<i>С момента включения режима неактивности:</i> {}",
        "ratelimit": "<b>Пожалуйста, подождите немного перед повторным использованием этой команды.</b>",
        "afk_set_failed": "<b>Не удалось установить AFK-статус. Проверьте логи.</b>",
    }

    DEFAULT_AFK_TIMEOUT = 60

    async def client_ready(self, client, db):
        self.client = client
        self.db = db
        self._me = await client.get_me()
        self._ratelimit_cache = {}

        self.global_afk = self.db.get(__name__, "afk", False)
        self.global_afk_reason = self.db.get(__name__, "afk_reason", None)
        self.global_gone_time = self.db.get(__name__, "gone_afk", None)

        logger.debug(f"Initial global AFK state: afk={self.global_afk}, reason={self.global_afk_reason}, gone_time={self.global_gone_time}")

    @loader.command(
        ru_doc="[reason / none] – Установить режим AFK",
    )
    async def afk(self, message):
        """[reason / none] – Set AFK mode globally."""
        await self._afk_toggle(message, global_afk=True)

    @loader.command(
        ru_doc="[reason / none] – Установить режим AFK только в этом чате.",
    )
    async def afkhere(self, message):
        """[reason / none] – Set AFK mode in current chat only."""
        await self._afk_toggle(message, global_afk=False)

    async def _afk_toggle(self, message, global_afk: bool):
        """Toggles AFK mode, either globally or in the current chat."""
        chat_id = utils.get_chat_id(message)
        db_key = "afk" if global_afk else f"afk_here_{chat_id}"
        already_afk_string = "already_afk" if global_afk else "already_afk_here"
        afk_on_string = "afk_on" if global_afk else "afk_here_on"
        afk_on_reason_string = "afk_on_reason" if global_afk else "afk_here_on_reason"

        if self._is_afk_enabled(chat_id, global_afk):
            await utils.answer(message, self.strings(already_afk_string, message))
            return

        reason = utils.get_args_raw(message) or None

        success = self._set_afk(True, reason=reason, chat_id=chat_id if not global_afk else None)

        if not success:
            await utils.answer(message, self.strings("afk_set_failed", message))
            return

        if reason:
            await utils.answer(message, self.strings(afk_on_reason_string, message).format(reason))
        else:
            await utils.answer(message, self.strings(afk_on_string, message))

    @loader.command(
        ru_doc="Выйти из режима AFK",
    )
    async def unafk(self, message):
        """Exit AFK mode"""
        await self._unafk_toggle(message, global_afk=True)

    @loader.command(
        ru_doc="Выйти из режима AFK в этом чате",
    )
    async def unafkhere(self, message):
        """Exit AFK mode in this chat"""
        await self._unafk_toggle(message, global_afk=False)

    async def _unafk_toggle(self, message, global_afk: bool):
        """Turns off AFK mode, either globally or in the current chat."""
        chat_id = utils.get_chat_id(message)
        db_key = "afk" if global_afk else f"afk_here_{chat_id}"
        not_afk_string = "not_afk" if global_afk else "not_afk_here"
        afk_off_time_string = "afk_off_time" if global_afk else "afk_off_here_time"

        if not self._is_afk_enabled(chat_id, global_afk):
            await utils.answer(message, self.strings(not_afk_string, message))
            return

        now = datetime.datetime.now().replace(microsecond=0)
        total_gone_time = self._calculate_total_afk_time(now, chat_id=chat_id if not global_afk else None)

        self._set_afk(False, chat_id=chat_id if not global_afk else None)

        await self.allmodules.log("unafk" if global_afk else "unafkhere")
        await utils.answer(message, self.strings(afk_off_time_string, message).format(total_gone_time))

    async def watcher(self, message):
        if not isinstance(message, types.Message):
            return

        chat_id = utils.get_chat_id(message)
        user_id = getattr(message.to_id, "user_id", None)
        is_mentioned = message.mentioned or user_id == self._me.id
        is_private = isinstance(message.to_id, types.PeerUser)

        if not (is_mentioned or is_private):
            return

        reason = None
        afk_state = False
        gone_time = None

        is_afk_here = self._is_afk_enabled(chat_id, False)
        if is_afk_here:
            reason = self.db.get(__name__, f"afk_here_{chat_id}_reason", None)
            afk_state = True
            gone_time = self.db.get(__name__, f"gone_afk_here_{chat_id}", None)
            ratelimit_key = f"ratelimit_here_{chat_id}"
        elif self.global_afk:
            reason = self.global_afk_reason
            afk_state = True
            gone_time = self.global_gone_time
            ratelimit_key = "ratelimit"
        else:
            return

        if afk_state:
            if gone_time is None:
                logger.warning(f"No 'gone' time found in database for {ratelimit_key}. Cannot send AFK message.")
                return

            if self._ratelimit(chat_id, ratelimit_key):
                await self._send_afk_message(message, reason, gone_time)
            else:
                await utils.answer(message, self.strings("ratelimit", message))

    def _set_afk(self, value: bool, reason: str = None, chat_id: int = None) -> bool:
        """Sets the AFK status in the database and updates class variables. Returns True on success, False on failure."""
        try:
            key_prefix = f"afk_here_{chat_id}" if chat_id else "afk"

            self.db.set(__name__, key_prefix, value)
            self.db.set(__name__, f"{key_prefix}_reason", reason)

            gone_key = f"gone_{key_prefix}"
            if value:
                gone_time = time.time()
                self.db.set(__name__, gone_key, gone_time)
                logger.debug(f"AFK enabled. {gone_key} set to {gone_time}")
            else:
                self.db.set(__name__, gone_key, None)
                logger.debug(f"AFK disabled. {gone_key} set to None")

            if chat_id is None:
                self.global_afk = value
                self.global_afk_reason = reason
                self.global_gone_time = gone_time if value else None
                logger.debug("Updated global AFK vars")

            return True

        except Exception as e:
            logger.exception(f"Error setting AFK status: {e}")
            return False

    def _calculate_total_afk_time(self, now: datetime.datetime, chat_id: int = None) -> datetime.timedelta:
        """Calculates the total time spent in AFK mode."""
        key_prefix = f"afk_here_{chat_id}" if chat_id else "afk"
        gone_time = self.db.get(__name__, f"gone_{key_prefix}")

        if gone_time is None:
            return datetime.timedelta(seconds=0)

        try:
            gone = datetime.datetime.fromtimestamp(gone_time).replace(microsecond=0)
            total_gone = (now - gone).total_seconds()
            return datetime.timedelta(seconds=total_gone)
        except Exception as e:
            logger.error(f"Error calculating AFK time: {e}")
            return datetime.timedelta(seconds=0)

    def _ratelimit(self, chat_id: int, key: str) -> bool:
        """Ratelimits AFK messages to avoid spam."""
        now = time.time()
        last_sent = self._ratelimit_cache.get((chat_id, key), 0)

        if now - last_sent < self.DEFAULT_AFK_TIMEOUT:
            return False

        self._ratelimit_cache[(chat_id, key)] = now
        return True

    async def _send_afk_message(self, message, reason, gone_time):
        """Sends the AFK message to the user."""
        user = await utils.get_user(message)
        if user.is_self or user.bot or user.verified:
            logger.debug("User is self, bot, or verified. Not sending AFK message.")
            return

        if gone_time is None:
            logger.warning("No 'gone' time found in database.  Cannot calculate AFK duration.")
            return

        now = datetime.datetime.now().replace(microsecond=0)
        try:
            gone = datetime.datetime.fromtimestamp(gone_time).replace(microsecond=0)
        except (TypeError, ValueError) as e:
            logger.error(f"Error converting timestamp: {e}")
            return

        diff = now - gone
        time_string = str(diff)

        if reason:
            ret = self.strings("afk_message_reason", message).format(reason, time_string)
        else:
            ret = self.strings("afk_message", message).format(time_string)

        try:
            await utils.answer(message, ret, reply_to=message)
        except Exception as e:
            logger.exception(f"Error sending AFK message: {e}")

    def _is_afk_enabled(self, chat_id: int = None, global_afk: bool = False) -> bool:
        """Helper function to check if AFK is enabled, either globally or for a specific chat."""
        if global_afk:
            return self.global_afk
        else:
            return self.db.get(__name__, f"afk_here_{chat_id}", False)
