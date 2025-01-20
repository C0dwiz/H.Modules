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
# Name: CheckSpamBan
# Description: Check spam ban for your account.
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# scope: CheckSpamBan
# scope: CheckSpamBan 0.0.1
# ---------------------------------------------------------------------------------

from .. import loader, utils

__version__ = (1, 0, 0)


@loader.tds
class SpamBanCheckMod(loader.Module):
    """Check spam ban for your account."""

    strings = {
        "name": "CheckSpamBan",
        "svo": "Your account is free from any restrictions.",
        "good": "<b>Everything is fine! You don't have a spam ban.</b>",
        "spamban": "<b>Unfortunately, your account has received a spam ban...\n\nReason: {reason}\nDuration: {duration}</b>",
        "spam_bot_error": "<b>Failed to communicate with @SpamBot. Please try again later.</b>",
        "no_bot": "<b>Can't find @SpamBot. Make sure you have started a chat with this bot.</b>",
        "bot_not_started": "<b>It seems you haven't started a chat with @SpamBot. Please start a chat and try again.</b>",
        "checking": "<b>Checking your account for spam ban...</b>",
    }

    strings_ru = {
        "svo": "Ваш аккаунт свободен от каких-либо ограничений.",
        "good": "<b>Все прекрасно! У вас нет спам бана.</b>",
        "spamban": "<b>К сожалению, ваш аккаунт получил спам-бан...\n\nПричина: {reason}\nДлительность: {duration}</b>",
        "spam_bot_error": "<b>Не удалось связаться с @SpamBot. Пожалуйста, попробуйте позже.</b>",
        "no_bot": "<b>Не могу найти @SpamBot. Убедитесь, что вы начали чат с этим ботом.</b>",
        "bot_not_started": "<b>Похоже, вы не начали чат с @SpamBot. Пожалуйста, начните чат и попробуйте еще раз.</b>",
        "checking": "<b>Проверяю ваш аккаунт на наличие спам-бана...</b>",
    }

    @loader.command(
        ru_doc="Проверяет вашу учетную запись на спам-бан с помощью бота @SpamBot",
        en_doc="Checks your account for spam ban via @SpamBot bot",
    )
    async def spambancmd(self, message):
        await utils.answer(message, self.strings("checking"))
        try:
            bot_user = await self._client.get_entity("SpamBot")
            if not isinstance(bot_user, User):
                await utils.answer(message, self.strings("no_bot"))
                return

            async with self._client.conversation("@SpamBot") as conv:
                try:
                    response = await conv.send_message("/start")
                    if response:
                        await conv.get_response()

                        last_message = (await conv.get_history(limit=1))[0]

                        if last_message.message.startswith("/start"):
                            if last_message.message.endswith(self.strings("svo")):
                                reply_text = self.strings("good")
                            else:
                                lines = last_message.message.split("\n")
                                if len(lines) >= 5:
                                    ban_reason = lines[2].strip()
                                    ban_duration = lines[4].strip()
                                    reply_text = self.strings("spamban").format(
                                        reason=ban_reason, duration=ban_duration
                                    )
                                else:
                                    reply_text = self.strings("spam_bot_error")
                        else:
                            reply_text = self.strings("bot_not_started")
                    else:
                        reply_text = self.strings("spam_bot_error")

                    await utils.answer(message, reply_text)
                except ChatAdminRequiredError:
                    await utils.answer(message, self.strings("bot_not_started"))
                except Exception as e:
                    await utils.answer(message, self.strings("spam_bot_error"))
        except Exception as e:
            await utils.answer(message, self.strings("spam_bot_error"))