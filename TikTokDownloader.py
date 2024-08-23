# ---------------------------------------------------------------------------------
# Name: TikTokDownloader
# Description: A module for downloading videos from TikTok without a watermark
# Author: @hikka_mods
# ---------------------------------------------------------------------------------

# 🔒    Licensed under the GNU AGPLv3
# 🌐 https://www.gnu.org/licenses/agpl-3.0.html

# meta developer: @hikka_mods
# scope: Api TikTokDownloader
# scope: Api TikTokDownloader 0.0.1
# ---------------------------------------------------------------------------------

from tiktok_downloader import snaptik
import tempfile
import os

from .. import loader, utils


@loader.tds
class TikTokDownloaderMod(loader.Module):
    """A module for downloading videos from TikTok without a watermark"""

    strings = {
        "name": "TikTokDownloader",
        "args_no": "<emoji document_id=5465665476971471368>❌</emoji> Specify the link to the TikTok video",
        "download": "<emoji document_id=5899757765743615694>⬇️</emoji> Uploading a video...",
        "done": "<emoji document_id=5280662183057825163>🎥</emoji> Your video from TikTok",
        "error": "<emoji document_id=5465665476971471368>❌</emoji> Error downloading video: {str(e)}",
    }

    strings_ru = {
        "args_no": "<emoji document_id=5465665476971471368>❌</emoji> Укажите ссылку на видео TikTok",
        "download": "<emoji document_id=5899757765743615694>⬇️</emoji> Загрузка видео...",
        "done": "<emoji document_id=5280662183057825163>🎥</emoji> Ваше видео с TikTok",
        "error": "<emoji document_id=5465665476971471368>❌</emoji> Ошибка при скачивании видео: {str(e)}",
    }

    @loader.command(
        ru_doc="Скачивает видео с TikTok по ссылке",
        en_doc="Downloads videos from TikTok via the link",
    )
    async def ttdlcmd(self, message):
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings("args_no"))
            return

        await utils.answer(message, self.strings("download"))

        try:
            get_video = snaptik(f"{args}")
            get_video_list = list(get_video)

            with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_file:
                get_video_list[0].download(temp_file.name)
                temp_file_path = temp_file.name

            with open(temp_file_path, "rb") as video:
                await message.client.send_file(
                    message.to_id, video, caption=self.strings("done")
                )

            os.remove(temp_file_path)
            await message.delete()

        except Exception as e:
            await utils.answer(message, self.strings("error").format(e=e))
