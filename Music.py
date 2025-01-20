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
# Description: Search for music through music bots.
# Author: @hikka_mods
# Commands:
# ym / vkm
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# scope: Music
# scope: Music 0.0.1
# ---------------------------------------------------------------------------------

from .. import loader, utils


@loader.tds
class MusicMod(loader.Module):
    """Поиск музыки через музыкальных ботов."""

    strings = {
        "name": "Music",
        "nenashel": (
            "<emoji document_id=5337117114392127164>🤷‍♂</emoji> <b>And what should I look for?</b>"
        ),
        "searching": "<emoji document_id=4918235297679934237>⌨️</emoji> <b>Searching...</b>",
        "done": "<emoji document_id=5336965905773504919>🗣</emoji> <b>Perhaps this is the track you were looking for</b>",
        "error": "<emoji document_id=5228947933545635555>😫</emoji> <b>I couldn't find a track with the title <code>{}</code></b>",
    }

    strings_ru = {
        "nenashel": (
            "<emoji document_id=5337117114392127164>🤷‍♂</emoji> <b>А что искать то?</b>"
        ),
        "searching": "<emoji document_id=4918235297679934237>⌨️</emoji> <b>Поиск...</b>",
        "done": "<emoji document_id=5336965905773504919>🗣</emoji> <b>Возможно, это тот трек, который вы искали</b>",
        "error": "<emoji document_id=5228947933545635555>😫</emoji> <b>Я не смог найти трек с названием <code>{}</code><b>",
    }

    @loader.command(
        ru_doc="Найти трек по названию в Yandex Music или VK: `searchm yandex {название}` или `searchm vk {название}`",
        en_doc="Find a track by name in Yandex Music or VK: `searchm yandex {name}` or `searchm vk {name}`",
    )
    async def searchm(self, message):
        args = utils.get_args_raw(message)
        r = await message.get_reply_message()

        if len(args) < 2:
            return await message.edit(self.strings("wrong_format"))

        service = args[0].lower()
        name = " ".join(args[1:])

        bot_names = {
            "yandex": "@Yandex_music_download_bot",
            "vk": "@vkmusic_bot",
        }

        if service not in bot_names:
            return await message.edit(self.strings("wrong_service"))

        bot = bot_names[service]

        if not name:
            return await message.edit(self.strings("nenashel"))

        try:
            await message.edit(self.strings("searching"))
            music = await message.client.inline_query(bot, name)
            await message.delete()
            for i in range(1, len(music), 2):
                try:
                    await message.client.send_file(
                        message.to_id,
                        music[i].result.document,
                        caption=self.strings("done"),
                        reply_to=utils.get_topic(message) if r else None,
                    )
                    return
                except:
                    pass
            return await message.client.send_message(
                message.chat_id, self.strings("error").format(args=name)
            )
        except:
            return await message.client.send_message(
                message.chat_id, self.strings("error").format(args=name)
            )
