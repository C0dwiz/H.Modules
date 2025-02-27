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
# Author: @hikka_mods
# meta developer: @hikka_mods
# scope: Music
# scope: Music 0.0.2
# ---------------------------------------------------------------------------------

# Thanks to @murpizz for the search code yandex

import logging

from telethon.errors.rpcerrorlist import (
    BotMethodInvalidError,
    FloodWaitError,
    MessageNotModifiedError,
)
from telethon.tl.types import Message

from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.tds
class MusicMod(loader.Module):
    strings = {
        "name": "Music",
        "no_query": "<emoji document_id=5337117114392127164>🤷‍♂</emoji> <b>Provide a search query.</b>",
        "searching": "<emoji document_id=4918235297679934237>⌨️</emoji> <b>Searching...</b>",
        "found": "<emoji document_id=5336965905773504919>🗣</emoji> <b>Possible match:</b>",
        "not_found": "<emoji document_id=5228947933545635555>😫</emoji> <b>Track not found: <code>{}</code>.</b>",
        "invalid_service": "<emoji document_id=5462295343642956603>🚫</emoji> <b>Invalid service. (yandex, vk)</b>",
        "usage": "<b>Usage:</b> <code>.music [yandex|vk] [track name]</code>",
        "error": "<emoji document_id=5228947933545635555>⚠️</emoji> <b>Error:</b> <code>{}</code>",
        "no_results": "<emoji document_id=5228947933545635555>😫</emoji> <b>No results: <code>{}</code>.</b>",
        "flood_wait": "<emoji document_id=5462295343642956603>⏳</emoji> <b>Wait {}s (Telegram limits).</b>",
        "bot_error": "<emoji document_id=5228947933545635555>🤖</emoji> <b>Bot error: <code>{}</code></b>",
        "no_audio": "<emoji document_id=5228947933545635555>🎵</emoji> <b>No audio.</b>",
        "generic_result": "<emoji document_id=5336965905773504919>ℹ️</emoji> <b>Non-media result. Check the bot's chat.</b>",
        "yafind_searching": "<emoji document_id=5258396243666681152>🔎</emoji> <b>Searching Yandex.Music...</b>",
        "yafind_not_found": "<emoji document_id=5843952899184398024>🚫</emoji> <b>Track not found on Yandex.Music.</b>",
        "yafind_error": "<emoji document_id=5843952899184398024>🚫</emoji> <b>Error (Yandex): {}</b>",
    }

    strings_ru = {
        "name": "Music",
        "no_query": "<emoji document_id=5337117114392127164>🤷‍♂</emoji> <b>Укажите запрос.</b>",
        "searching": "<emoji document_id=4918235297679934237>⌨️</emoji> <b>Поиск...</b>",
        "found": "<emoji document_id=5336965905773504919>🗣</emoji> <b>Возможно, это оно:</b>",
        "not_found": "<emoji document_id=5228947933545635555>😫</emoji> <b>Трек не найден: <code>{}</code>.</b>",
        "invalid_service": "<emoji document_id=5462295343642956603>🚫</emoji> <b>Неверный сервис. (yandex, vk)</b>",
        "usage": "<b>Использование:</b> <code>.music [yandex|vk] [название трека]</code>",
        "error": "<emoji document_id=5228947933545635555>⚠️</emoji> <b>Ошибка:</b> <code>{}</code>",
        "no_results": "<emoji document_id=5228947933545635555>😫</emoji> <b>Нет результатов: <code>{}</code>.</b>",
        "flood_wait": "<emoji document_id=5462295343642956603>⏳</emoji> <b>Подождите {}с (лимиты Telegram).</b>",
        "bot_error": "<emoji document_id=5228947933545635555>🤖</emoji> <b>Ошибка бота: <code>{}</code></b>",
        "no_audio": "<emoji document_id=5228947933545635555>🎵</emoji> <b>Нет аудио.</b>",
        "generic_result": "<emoji document_id=5336965905773504919>ℹ️</emoji> <b>Немедийный результат. Проверьте чат с ботом.</b>",
        "yafind_searching": "<emoji document_id=5258396243666681152>🔎</emoji> <b>Поиск в Яндекс.Музыке...</b>",
        "yafind_not_found": "<emoji document_id=5843952899184398024>🚫</emoji> <b>Трек не найден в Яндекс.Музыке.</b>",
        "yafind_error": "<emoji document_id=5843952899184398024>🚫</emoji> <b>Ошибка (Яндекс): {}</b>",
    }

    def __init__(self):
        self.murglar_bot = "@murglar_bot"
        self.vk_bot = "@vkmusic_bot"

    @loader.command(
        ru_doc="Найти трек в Yandex Music или VK: `.music yandex {название}` или `.music vk {название}`",
        en_doc="Find a track in Yandex Music or VK: `.music yandex {name}` or `.music vk {name}`",
    )
    async def music(self, message):
        args = utils.get_args(message)

        if not args:
            if reply := await message.get_reply_message():
                await self._yafind(message, reply.raw_text.strip())
            else:
                await utils.answer(message, self.strings("usage", message))
            return

        service, query = args[0].lower(), " ".join(args[1:])

        if service == "yandex":
            await self._yafind(message, query)
        elif service == "vk":
            await self._vkfind(message, query)
        else:
            await utils.answer(message, self.strings("invalid_service", message))

    async def _yafind(self, message: Message, query: str):
        if not query:
            return await utils.answer(message, self.strings("no_query", message))

        await utils.answer(message, self.strings("yafind_searching", message))

        try:
            results = await message.client.inline_query(
                self.murglar_bot, f"s:ynd {query}"
            )

            if not results:
                return await utils.answer(
                    message, self.strings("yafind_not_found", message)
                )

            await results[0].click(
                entity=message.chat_id,
                hide_via=True,
                reply_to=message.reply_to_msg_id if message.reply_to_msg_id else None,
            )
            await message.delete()

        except Exception as e:
            logger.exception("Yandex search error:")
            await utils.answer(message, self.strings("yafind_error", message).format(e))

    async def _vkfind(self, message, query: str):
        if not query:
            return await utils.answer(message, self.strings("no_query", message))

        await utils.answer(message, self.strings("searching", message))

        try:
            music = await message.client.inline_query(self.vk_bot, query)

            if not music or len(music) <= 1:
                return await utils.answer(
                    message, self.strings("not_found", message).format(query)
                )

            for i in range(1, len(music), 2):
                try:
                    result = music[i].result
                    if hasattr(result, "audio") and result.audio:
                        await message.client.send_file(
                            message.to_id,
                            result.audio,
                            caption=self.strings("found", message),
                            reply_to=utils.get_topic(message)
                            if message.reply_to_msg_id
                            else None,
                        )
                        await message.delete()
                        return
                    if hasattr(result, "document") and result.document:
                        await message.client.send_file(
                            message.to_id,
                            result.document,
                            caption=self.strings("found", message),
                            reply_to=utils.get_topic(message)
                            if message.reply_to_msg_id
                            else None,
                        )
                        await message.delete()
                        return

                    logger.warning(f"No audio/document in result {i}")
                    await utils.answer(message, self.strings("no_audio", message))
                    await message.delete()
                    return

                except MessageNotModifiedError:
                    logger.warning("MessageNotModifiedError, skipping.")
                except Exception as e:
                    logger.error(f"Send error: {e}")

            await utils.answer(
                message, self.strings("not_found", message).format(query)
            )

        except BotMethodInvalidError as e:
            logger.error(f"VK bot error: {e}")
            await utils.answer(message, self.strings("bot_error", message).format(e))
        except FloodWaitError as e:
            logger.warning(f"Flood wait: {e.seconds}s")
            await utils.answer(
                message, self.strings("flood_wait", message).format(e.seconds)
            )
        except Exception as e:
            logger.exception("VK search error:")
            await utils.answer(message, self.strings("error", message).format(e))
