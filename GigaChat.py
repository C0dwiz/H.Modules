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
# Name: GigaChat
# Description: Module for using GigaChat
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# scope: Api GigaChat
# scope: Api GigaChat 0.0.1
# ---------------------------------------------------------------------------------

from gigachat import GigaChat

from .. import loader, utils


@loader.tds
class GigaChatMod(loader.Module):
    """Module for using GigaChat"""

    strings = {
        "name": "GigaChat",
        "api_key_missing": "Please set the API key in the module configuration.",
        "query_missing": "Please enter a query after the command.",
        "response_error": "Failed to get a response from GigaChat.",
        "error_occurred": "An error occurred: {}",
        "formatted_response": (
             "<emoji document_id=6030848053177486888>❓</emoji> Query: {}\n"
             "<emoji document_id=6030400221232501136>🤖</emoji> GigaResponse: {}"
        )
    }

    strings_ru = {
        "api_key_missing": "Пожалуйста, установите API ключ в конфигурации модуля.",
        "query_missing": "Пожалуйста, введите запрос после команды.",
        "response_error": "Не удалось получить ответ от GigaChat.",
        "error_occurred": "Произошла ошибка: {}",
        "formatted_response": (
             "<emoji document_id=6030848053177486888>❓</emoji> Запрос: {}\n"
             "<emoji document_id=6030400221232501136>🤖</emoji> GigaChat ответ: {}"
        )
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            "GIGACHAT_API_KEY",
            None,
            "Введите ваш API ключ для GigaChat, Чтобы получить ключ API, перейдите сюда: https://developers.sber.ru/studio/workspaces"
        )

    @loader.command(
        ru_doc="Получите исчерпывающий ответ на свой вопрос"
        en_doc="Get GigaResponse to your question"
    )
    async def gigacmd(self, message):
        api_key = self.config["GIGACHAT_API_KEY"]
        if not api_key:
            return await utils.answer(message, self.strings("api_key_missing"))

        query = utils.get_args_raw(message)
        if not query:
            return await utils.answer(message, self.strings("query_missing"))

        try:
            response = await self.get_giga_response(api_key, query)
            if response:
                await utils.answer(message, self.strings("formatted_response").format(query, response))
            else:
                await utils.answer(message, self.strings("response_error"))
        except Exception as e:
            await utils.answer(message, self.strings("error_occurred").format(str(e)))

    async def get_giga_response(self, api_key, query):
        """Gets a response from GigaChat with the specified query."""
        async with GigaChat(credentials=api_key, scope="GIGACHAT_API_PERS", verify_ssl_certs=False) as giga:
            response = await giga.chat(query)
            if response.choices:
                return response.choices[0].message.content
            return None