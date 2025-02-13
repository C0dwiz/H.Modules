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
# Name: Music
# Description: Searches for music using Telegram music bots.
# Author: @hikka_mods ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# scope: Music
# scope: Music 0.0.2
# ---------------------------------------------------------------------------------

import logging

from telethon.errors.rpcerrorlist import BotMethodInvalidError, FloodWaitError, MessageNotModifiedError

from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.tds
class MusicMod(loader.Module):
    """Searches for music using Telegram music bots."""

    strings = {
        "name": "Music",
        "no_query": "<emoji document_id=5337117114392127164>🤷‍♂</emoji> <b>Please provide a search query.</b>",
        "searching": "<emoji document_id=4918235297679934237>⌨️</emoji> <b>Searching...</b>",
        "found": "<emoji document_id=5336965905773504919>🗣</emoji> <b>Possible match:</b>",
        "not_found": "<emoji document_id=5228947933545635555>😫</emoji> <b>No track found with the title <code>{}</code>.</b>",
        "invalid_service": "<emoji document_id=5462295343642956603>🚫</emoji> <b>Invalid service. Supported services: yandex, vk.</b>",
        "usage": "<b>Usage:</b> <code>.music [yandex|vk] [track name]</code>",
        "error": "<emoji document_id=5228947933545635555>⚠️</emoji> <b>An error occurred:</b> <code>{}</code>",
        "no_results": "<emoji document_id=5228947933545635555>😫</emoji> <b>The bot returned no results for <code>{}</code>.</b>",
        "flood_wait": "<emoji document_id=5462295343642956603>⏳</emoji> <b>Please wait {} seconds before trying again due to Telegram rate limits.</b>",
        "bot_error": "<emoji document_id=5228947933545635555>🤖</emoji> <b>The bot encountered an error: <code>{}</code></b>",
        "no_audio": "<emoji document_id=5228947933545635555>🎵</emoji> <b>Result does not contain audio or document.</b>",
        "generic_result": "<emoji document_id=5336965905773504919>ℹ️</emoji> <b>Bot returned a non-media result.  Check the bot's chat.</b>",
    }

    strings_ru = {
        "no_query": "<emoji document_id=5337117114392127164>🤷‍♂</emoji> <b>Укажите поисковой запрос.</b>",
        "searching": "<emoji document_id=4918235297679934237>⌨️</emoji> <b>Поиск...</b>",
        "found": "<emoji document_id=5336965905773504919>🗣</emoji> <b>Возможно, это то, что вы искали:</b>",
        "not_found": "<emoji document_id=5228947933545635555>😫</emoji> <b>Не удалось найти трек с названием <code>{}</code>.</b>",
        "invalid_service": "<emoji document_id=5462295343642956603>🚫</emoji> <b>Неверный сервис. Поддерживаемые сервисы: yandex, vk.</b>",
        "usage": "<b>Использование:</b> <code>.music [yandex|vk] [название трека]</code>",
        "error": "<emoji document_id=5228947933545635555>⚠️</emoji> <b>Произошла ошибка:</b> <code>{}</code>",
        "no_results": "<emoji document_id=5228947933545635555>😫</emoji> <b>Бот не вернул результатов для запроса <code>{}</code>.</b>",
        "flood_wait": "<emoji document_id=5462295343642956603>⏳</emoji> <b>Пожалуйста, подождите {} секунд перед повторной попыткой из-за ограничений Telegram.</b>",
        "bot_error": "<emoji document_id=5228947933545635555>🤖</emoji> <b>Бот столкнулся с ошибкой: <code>{}</code></b>",
        "no_audio": "<emoji document_id=5228947933545635555>🎵</emoji> <b>В результате нет аудио или документа.</b>",
        "generic_result": "<emoji document_id=5336965905773504919>ℹ️</emoji> <b>Бот вернул немедийный результат. Проверьте чат с ботом.</b>",
    }

    def __init__(self):
        self.yandex_bot_username = "@YaMusRobot"
        self.vk_bot_username = "@vkmusic_bot"
        self.bot_names = {
            "yandex": self.yandex_bot_username,
            "vk": self.vk_bot_username,
        }

    @loader.command(
        ru_doc="Найти трек по названию в Yandex Music или VK: `.music yandex {название}` или `.music vk {название}`",
        en_doc="Find a track by name in Yandex Music or VK: `.music yandex {name}` or `.music vk {name}`",
    )
    async def music(self, message):
        """Searches for music in Yandex Music or VK using Telegram bots."""
        args = utils.get_args(message)
        reply = await message.get_reply_message()

        if len(args) < 2:
            return await utils.answer(message, self.strings("usage", message))

        service = args[0].lower()
        query = " ".join(args[1:])

        if service not in self.bot_names:
            return await utils.answer(message, self.strings("invalid_service", message))

        bot = self.bot_names[service]

        if not query:
            return await utils.answer(message, self.strings("no_query", message))

        try:
            await utils.answer(message, self.strings("searching", message))

            if service == "yandex":
                query = query + " ."

            try:
                music = await self.client.inline_query(bot, query)
            except BotMethodInvalidError as e:
                logger.error(f"Bot {bot} returned an invalid method error: {e}")
                return await utils.answer(message, self.strings("bot_error", message).format(e))
            except FloodWaitError as e:
                logger.warning(f"Flood wait error: {e.seconds} seconds")
                return await utils.answer(message, self.strings("flood_wait", message).format(e.seconds))

            if not music:
                return await utils.answer(
                    message, self.strings("no_results", message).format(query)
                )

            if len(music) <= 1:
                return await utils.answer(
                    message, self.strings("not_found", message).format(query)
                )

            sent = False
            for i in range(1, len(music), 2):
                try:
                    if hasattr(music[i].result, 'audio') and music[i].result.audio:
                        await self.client.send_file(
                            message.to_id,
                            music[i].result.audio,
                            caption=self.strings("found", message),
                            reply_to=utils.get_topic(message) if reply else None,
                        )
                        await message.delete()
                        sent = True
                        break
                    elif hasattr(music[i].result, 'document') and music[i].result.document:
                        await self.client.send_file(
                            message.to_id,
                            music[i].result.document,
                            caption=self.strings("found", message),
                            reply_to=utils.get_topic(message) if reply else None,
                        )
                        await message.delete()
                        sent = True
                        break
                    else:
                        logger.warning(f"No audio or document found in result {i}")
                        await utils.answer(message, self.strings("no_audio", message)) 
                        await message.delete()
                        sent = True
                        break
                except MessageNotModifiedError:
                    logger.warning("MessageNotModifiedError: Could not edit message, skipping.")
                except Exception as e:
                    logger.error(f"Error sending file: {e}")
                    continue

            if not sent:
                await utils.answer(
                    message, self.strings("not_found", message).format(query)
                )

        except Exception as e:
            logger.exception("Error during music search:")
            await utils.answer(message, self.strings("error", message).format(e))
