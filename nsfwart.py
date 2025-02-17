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
# Name: NSFWArt
# Description: Sends cute anime nsfw-art
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# scope: Api NSFWArt
# scope: Api NSFWArt 0.0.1
# ---------------------------------------------------------------------------------

import functools
import requests
from typing import List

from .. import loader, utils


async def photos(tags: str, subreddit: str, quantity: int) -> List[str]:
    ans = (
        await utils.run_sync(
            requests.get,
            f"https://api.lolicon.app/setu/v2?tag={tags}",
            json={
                "query": (
                    " query SubredditQuery( $url: String! $filter: SubredditPostFilter"
                    " $iterator: String ) { getSubreddit(url: $url) { children("
                    f" limit: {quantity} iterator: $iterator filter: $filter"
                    " disabledHosts: null ) { iterator items {url subredditTitle"
                    " isNsfw mediaSources { url } } } } } "
                ),
                "variables": {"url": subreddit, "filter": None, "hostsDown": None},
                "authorization": None,
            },
        )
    ).json()

    return [ans["data"][0]["urls"]["original"]]


@loader.tds
class NSFWArtMod(loader.Module):
    """Sends cute anime nsfw-art"""

    strings = {
        "name": "NSFWArt",
        "sreddit404": "🚫 <b>Subreddit not found</b>",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "tags",
                "drool",
                lambda: "tag: masturbation, drool, completely, sleeping, yuri",
            )
        )

    @loader.command(
        ru_doc="Отправьте симпатичный nsfw-арт",
        en_doc="Send cute nsfw-art",
    )
    async def nsfwartcmd(self, message):
        tags = self.config["tags"]
        subreddit = f"/v2?tag={tags}"

        ans = await utils.run_sync(
            requests.get, f"https://api.lolicon.app/setu{subreddit}"
        )
        if ans.status_code != 200:
            await utils.answer(message, self.strings("sreddit404", message))
            return

        await self.inline.gallery(
            message=message,
            next_handler=functools.partial(
                photos, tags, subreddit=subreddit, quantity=15
            ),
            caption=f"<i>{utils.ascii_face()}</i>",
        )
