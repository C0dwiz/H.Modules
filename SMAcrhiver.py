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
# Name: SMArchiver
# Description: unloads all messages from Favorites
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# scope: SMArchiver
# scope: SMArchiver 0.0.1
# requires: zipfile
# ---------------------------------------------------------------------------------

import os
import zipfile

from hikkatl.types import Message
from datetime import datetime

from .. import loader, utils


@loader.tds
class SMArchiver(loader.Module):
    """unloads all messages from Favorites"""

    strings = {
        "name": "SMArchiver",
        "archive_created": "🎉 Archive with messages has been successfully created: {filename}",
        "no_messages": "⚠️ There are no messages in Saved Messages.",
        "error": "❌ An error occurred: {error}",
        "processing": "🛠️ Processing messages... Please wait.\n\nP.S: Be careful, if you have a lot of messages, you may get flooding, and if you have a lot of heavy files, the download will be slower than usual."
    }

    strings_ru = {
        "archive_created": "🎉 Архив с сообщениями успешно создан: {filename}",
        "no_messages": "⚠️ В Избранном нет сообщений.",
        "error": "❌ Произошла ошибка: {error}",
        "processing": "🛠️ Обработка сообщений... Пожалуйста, подождите.\n\nP.S: Будьте осторожны, если у вас много сообщений то вы можете получить флудвейт, и ещё если у вас много тяжёлых файлов то загрузка будет медленнее чем обычно."
    }

    @loader.command(
        ru_doc="выгружает все сообщения из Избранного / Saved Messages и собирает их в одном архиве.",
        en_doc="downloads all messages from Favorites / Saved Messages and collects them in one archive.",
    )
    async def smdump(self, message: Message):
        try:
            await utils.answer(message, self.strings["processing"])
            saved_messages = await message.client.get_messages("me", limit=None)

            if not saved_messages:
                return

            current_month = datetime.now().strftime("%B %Y")
            archive_path = "saved_messages.zip"

            with zipfile.ZipFile(archive_path, "w") as archive:
                month_folder = f"{current_month}/"
                archive.writestr(month_folder, "")

                text_messages_folder = f"{month_folder}Text Messages/"
                voice_messages_folder = f"{month_folder}Voice Messages/"
                video_messages_folder = f"{month_folder}Video Messages/"
                videos_folder = f"{month_folder}Videos/"
                audios_folder = f"{month_folder}Audios/"
                gifs_folder = f"{month_folder}GIFs/"
                files_folder = f"{month_folder}Files/"

                for folder in [
                    text_messages_folder,
                    voice_messages_folder,
                    video_messages_folder,
                    videos_folder,
                    audios_folder,
                    gifs_folder,
                    files_folder,
                ]:
                    archive.writestr(folder, "")

                for msg in saved_messages:
                    if msg.message:
                        timestamp = datetime.fromtimestamp(
                            msg.date.timestamp()
                        ).strftime("%Y%m%d_%H%M%S")
                        safe_name = f"message_{timestamp}.txt"
                        archive.writestr(
                            os.path.join(text_messages_folder, safe_name), msg.message
                        )

                    if msg.media:
                        if hasattr(msg.media, "document"):
                            media_file = await message.client.download_media(msg.media)
                            if media_file:
                                if msg.media.document.mime_type.startswith("audio/"):
                                    archive.write(
                                        media_file,
                                        os.path.join(
                                            audios_folder, os.path.basename(media_file)
                                        ),
                                    )
                                elif msg.media.document.mime_type.startswith("video/"):
                                    archive.write(
                                        media_file,
                                        os.path.join(
                                            videos_folder, os.path.basename(media_file)
                                        ),
                                    )
                                elif msg.media.document.mime_type.startswith(
                                    "image/gif"
                                ):
                                    archive.write(
                                        media_file,
                                        os.path.join(
                                            gifs_folder, os.path.basename(media_file)
                                        ),
                                    )
                                else:
                                    archive.write(
                                        media_file,
                                        os.path.join(
                                            files_folder, os.path.basename(media_file)
                                        ),
                                    )

            await message.client.send_file(
                message.chat_id,
                archive_path,
                caption=self.strings["archive_created"].format(
                    filename=os.path.basename(archive_path)
                ),
            )

        except Exception as e:
            if "no messages" not in str(e).lower():
                await utils.answer(message, self.strings["error"].format(error=str(e)))

        finally:
            if os.path.exists(archive_path):
                os.remove(archive_path)
