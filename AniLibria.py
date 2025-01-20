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
# Name: AniLibria
# Description: Searches and gives random agtme on the AniLibria database.
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# scope: AniLibria
# scope: AniLibria 0.0.1
# requires: anilibria.py
# ---------------------------------------------------------------------------------

from ..inline.types import InlineQuery
from aiogram.types import InlineQueryResultPhoto, CallbackQuery
from anilibria import AniLibriaClient

from .. import loader

ani_client = AniLibriaClient()


@loader.tds
class AniLibriaMod(loader.Module):
    """Searches and gives random agtme on the AniLibria database."""

    strings = {
        "name": "AniLibria",
        "announce": "<b>The announcement</b>:",
        "status": "<b>Status</b>:",
        "type": "<b>Type</b>:",
        "genres": "<b>Genres</b>:",
        "favorite": "<b>Favourites &lt;3</b>:",  # &lt; == <
        "season": "<b>Season</b>:",
    }

    strings_ru = {
        "announce": "<b>Анонс</b>:",
        "status": "<b>Статус</b>:",
        "type": "<b>Тип</b>:",
        "genres": "<b>Жанры</b>:",
        "favorite": "<b>Избранное &lt;3</b>:",  # &lt; == <
        "season": "<b>Сезон</b>:",
    }

    link = "https://anilibria.tv"

    async def client_ready(self, client, db) -> None:
        self._client = client

    @loader.command(
        ru_doc="Возвращает случайный тайтл из базы",
        en_doc="Returns a random title from the database",
    )
    async def arandom(self, message) -> None:
        anime_title = await ani_client.get_random_title()

        text = f"{anime_title.names.ru} \n"
        text += f"{self.strings['status']} {anime_title.status.string}\n\n"
        text += f"{self.strings['type']} {anime_title.type.full_string}\n"
        text += f"{self.strings['season']} {anime_title.season.string}\n"
        text += f"{self.strings['genres']} {' '.join(anime_title.genres)}\n\n"

        text += f"<code>{anime_title.description}</code>\n\n"
        text += f"{self.strings['favorite']} {anime_title.in_favorites}"

        kb = [
            [
                {
                    "text": "Ссылка",
                    "url": f"https://anilibria.tv/release/{anime_title.code}.html",
                }
            ]
        ]

        kb.extend(
            [
                {
                    "text": f"{torrent.quality.string}",
                    "url": f"https://anilibria.tv/{torrent.url}",
                }
            ]
            for torrent in anime_title.torrents.list
        )
        kb.append([{"text": "🔃 Обновить", "callback": self.inline__update}])
        kb.append([{"text": "🚫 Закрыть", "callback": self.inline__close}])

        await self.inline.form(
            text=text,
            photo=self.link + anime_title.posters.original.url,
            message=message,
            reply_markup=kb,
            silent=True,
        )

    @loader.command(
        ru_doc="Возвращает список найденных по названию тайтлов",
        en_doc="Returns a list of titles found by name",
    )
    async def asearch_inline_handler(self, query: InlineQuery) -> None:
        text = query.args

        if not text:
            return

        anime_titles = await ani_client.search_titles(search=text)

        inline_query = []
        for anime_title in anime_titles:
            title_text = (
                f"{anime_title.names.ru} | {anime_title.names.en}\n"
                f"{self.strings['status']} {anime_title.status.string}\n\n"
                f"{self.strings['type']} {anime_title.type.full_string}\n"
                f"{self.strings['season']} {anime_title.season.string} {anime_title.season.year}\n"
                f"{self.strings['genres']} {' '.join(anime_title.genres)}\n\n"
                f"<code>{anime_title.description}</code>\n\n"
                f"{self.strings['favorite']} {anime_title.in_favorites}"
            )

            inline_query.append(
                InlineQueryResultPhoto(
                    id=str(anime_title.code),
                    title=anime_title.names.ru,
                    description=anime_title.type.full_string,
                    caption=title_text,
                    thumb_url=self.link + anime_title.posters.small.url,
                    photo_url=self.link + anime_title.posters.original.url,
                    parse_mode="html",
                )
            )
        await query.answer(inline_query, cache_time=0)

    async def inline__close(self, call: CallbackQuery) -> None:
        await call.delete()

    async def inline__update(self, call: CallbackQuery) -> None:
        anime_title = await ani_client.get_random_title()

        text = (
            f"{anime_title.names.ru} \n"
            f"{self.strings['status']} {anime_title.status.string}\n\n"
            f"{self.strings['type']} {anime_title.type.full_string}\n"
            f"{self.strings['season']} {anime_title.season.string}\n"
            f"{self.strings['genres']} {' '.join(anime_title.genres)}\n\n"
            f"<code>{anime_title.description}</code>\n\n"
            f"{self.strings['favorite']} {anime_title.in_favorites}"
        )

        kb = [
            [
                {
                    "text": "Ссылка",
                    "url": f"https://anilibria.tv/release/{anime_title.code}.html",
                }
            ]
        ]

        kb.extend(
            [
                {
                    "text": f"{torrent.quality.string}",
                    "url": f"https://anilibria.tv/{torrent.url}",
                }
            ]
            for torrent in anime_title.torrents.list
        )
        kb.append([{"text": "🔃 Обновить", "callback": self.inline__update}])
        kb.append([{"text": "🚫 Закрыть", "callback": self.inline__close}])

        await call.edit(
            text=text,
            photo=self.link + anime_title.posters.original.url,
            reply_markup=kb,
        )
