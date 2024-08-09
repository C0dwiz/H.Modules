# ---------------------------------------------------------------------------------
# Name: NSFWArt
# Description: Sends cute anime nsfw-art
# Author: @hikka_mods
# ---------------------------------------------------------------------------------

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# meta developer: @hikka_mods
# scope: Api NSFWArt
# scope: Api NSFWArt 0.0.1
# ---------------------------------------------------------------------------------

import functools
import requests
from typing import List
from telethon.tl.types import Message

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

    async def nsfwartcmd(self, message: Message):
        """- send cute nsfw-art"""

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
