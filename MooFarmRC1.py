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
# Name: MooFarmRC1
# Description: Модуль для автофарма в "Коровке"!
# Author: @hikka_mods and @Frost_Shard
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods and @Frost_Shard
# scope: MooFarmRC1
# scope: MooFarmRC1 0.0.1
# requires: aioredis
# ---------------------------------------------------------------------------------

__version__ = (0, 1, 4, 10)

import os
import re
import typing
import asyncio
import base64
import aioredis
from typing import Optional
from telethon.tl.types import Message
from telethon.tl.types import InputDocument
from telethon.tl.types import User
from telethon import events
from .. import loader, utils
from ..inline.types import InlineCall
import json

class DebugLogger:

    def __init__(self, client, config):
        self.client = client
        self.config = config

    async def log(self, text: str, category: str):
        """Основной метод логирования."""
        if not self.config["config_debug_msg"]:
            return

        allowed_categories = self.config["config_debug_diff_msg"]
        if category not in allowed_categories:
            return

        await self.client.send_message(
            self.config["config_bot_used_chat_id"],
            f"[{category.upper()}] {text}",
        )

    async def eat(self, text: str):
        """Логирование для еды."""
        await self.log(text, "Eating")

    async def eat_state(self, text: str):
        """Логирование для состояния еды."""
        await self.log(text, "Eating_state")

    async def eat_click(self, text: str):
        """Логирование для автокликера еды."""
        await self.log(text, "Eating_click")

    async def craft(self, text: str):
        """Логирование для крафта."""
        await self.log(text, "Crafting")

    async def craft_state(self, text: str):
        """Логирование для состояния крафта."""
        await self.log(text, "Crafting_state")

    async def craft_click(self, text: str):
        """Логирование для автокликера еды."""
        await self.log(text, "Crafting_click")

    async def forest(self, text: str):
        """Логирование для Автолеса."""
        await self.log(text, "Forest")

    async def forest_state(self, text: str):
        """Логирование для леса."""
        await self.log(text, "Forest_state")

    async def forest_click(self, text: str):
        """Логирование для лесного автокликера."""
        await self.log(text, "Forest_click")

    async def forest_npc(self, text: str):
        """Логирование для лесных нпц."""
        await self.log(text, "Forest_npc")

    async def general(self, text: str):
        """Общий лог."""
        await self.log(text, "General")

    async def redis(self, text: str):
        """Общий лог для базы данных."""
        await self.log(text, "Redis")

    async def state(self, text: str):
        """Общий лог состояний."""
        await self.log(text, "State")

@loader.tds
class AutoFarmbotMod(loader.Module):
    """
    Модуль для автофарма в "Коровке"!
    В конфиге настройте: сhat_id и bot_id ->
    Синхронизируйте скин в меню ->
    Зарегистрируйтесь на Redis.io и ссылку добавьте в конфиг

    """
    # Todo: Автокрафт и Автолес готовы на 95%, автохавка на 45%
    strings = {
        "name": "AutoFarmbot",
        # Inline keys
        "auto_eating": "🌸 Автоеда",
        "auto_milk": "🥛 АвтоДойка",
        "auto_forest": "🌳 АвтоЛес",
        "auto_craft": "🧤 АвтоКрафт",
        "settings": "🛠️ Настройки",
        "close_btn": "📂 Закрыть меню",
        "back_btn": "🔙 Назад",
        "bot_forest_back": "🥺 забрать лут",
        "bot_forest_go": "🌲 гулять",
        "bot_skin_menu_key": "⭐ Настройки скина",
        "on": "✅ Включено",
        "on_btn": "✅",
        "off": "❌ Выключено",
        "off_btn": "❌",
        # main menu
        "moo_menu": "<b>🐮 Меню управления автофармом:</b>\n\n",
        "auto_forest_menu": "<b>🌳 АвтоЛес - Функции автоматического хождения в лес</b>\n",
        "auto_eating_menu": "<b>🌸 Автоеда - Функции автоматического кормления коровки</b>\n",
        "auto_craft_menu": "<b>🧤 АвтоКрафт - Автоматический крафт на верстаке</b>\n",
        "settings_menu": "<b>️Настройки - Остальные настройки модуля</b>\n",
        "skin_menu": "<b>⭐ Скин - Все настройки связанные с показом скина</b>\n",
        # Auto forest menu
        "npc_not_skipped": "<i>Никто не пропускается</i>\n",
        "npc_menu": "<b>🌲 Настройки автолеса:</b>\n\n",
        "npc_menu_autoforest": "🌲 <b>Автолес:</b>",
        "npc_menu_autoforest_btn": "🌲 Автолес:",
        "npc_menu_skip_status": "🦔 <b>АвтоСкип НПЦ:</b>",
        "npc_menu_skip_status_btn": "🦔 АвтоСкип НПЦ:",
        "npc_menu_skip": "🛠️ <b>Меню Автоскипа:</b> - <i>Выберите НПЦ для скипа.</i>",
        "npc_menu_skip_now": "\n<b>📋 Сейчас скипаются:</b>\n",
        "npc_autoskip": "🛠️ Меню Автоскипа",
        # skin menu
        "skin_menu_main_txt": "🌫️ <b>Меню настройки скина</b>\n\n",
        "skin_menu_show_skin_btn": "🌟 Показывать скин",
        "skin_menu_sync_skin_btn": "🌟 Синхронизировать скин",
        "skin_menu_txt": "🧩 <b>Скин</b>:",
        "skin_menu_show_txt": "👁️ <b>Показывать</b>:",
        # eat menu
        "auto_eat_main_menu_txt": "<b>🍽 Настройки автоеды:</b>\n\n",
        "auto_eating_main_menu_txt": "Автоеда:",
        "auto_eating_inforest_main_menu_txt": "В лесу:",
        "auto_eating_item": "🍲 Предмет:",
        "auto_eating_item_count": "🔢 Кол-во:",
        "auto_eating_lvl": "🧬 Уровень еды:",
        "auto_eating_inline_count": "✍️ Введите количество для авто-кормёжки:",
        "auto_eating_inline_lvl": "✍️ Введите % еды авто-кормёжки:",
        "auto_eating_inline_item": "✍️ Введите еду для авто-кормёжки:",
        # forest inline skip menu
        "skip_menu_main_txt": "🧪 Настройка скипа лесных жителей:",
        "skip_menu_main_on": "❌ - Не пропускать",
        "skip_menu_main_off": "✅ - Пропускать",
        "skip_menu_main_skipped": "<i>✅  пропускаем</i>",
        # craft inline menu
        "craft_menu_main_txt": "⚒ Настройки автокрафта:",
        "craft_menu_main_craft": "Автокрафт:",
        "craft_menu_main_craft_item": "🛠 Предмет:",
        "craft_menu_main_craft_count": "🔢 Кол-во:",
        "craft_menu_main_craft_item_inline": "✍️ Введите название предмета для авто-крафта:",
        "craft_menu_main_craft_count_inline": "✍️ Введите количество для авто-крафта:",
        # misc inline menu
        "misc_menu_main_txt": "⚙️ Прочие настройки:",
        "misc_menu_main_debug": "Отладка:",
        "misc_menu_main_deletemsg": "Удалять в боте:",
        "misc_menu_main_logs_chat": "📤 Куда слать логи:",
        "misc_menu_main_logs_chat_inline": "✍️ Введите чат для логов:",
        "misc_menu_main_chat_id": "ID чата:",
        "misc_menu_main_chat_id_inline": "✍️ Введите чат для работы бота:",
        "misc_menu_main_bots_id": "ID бота(ов):",
        "misc_menu_main_bots_id_inline": "✍️ Введите ID бота для работы:",
        "misc_menu_main_debug_btn_menu": "🧪 Конфиги отладки",
        # debug inline menu
        "debug_menu_main_txt": "🧪 Конфиг Debug Diff Msg:",
        # Debug message
        "Debug_Events_msg_set": "[EVENTS] Установил хендлеры.",
        "Debug_Events_msg_del": "[EVENTS] Удалил хендлеры.",
        "Debug_craft_take_ok": "[CRAFT] Забрал скрафченные предметы!",
        "Debug_craft_start_ok": "[CRAFT] Открыл список для крафта!",
        "Debug_craft_finall_ok": "[CRAFT] Нажал кнопку крафта предмета и отправил количество на крафт!",
        "Debug_craft_job_ok": "[REDIS] Найдено сообщение с крафтом, обновил таймер!",
        "Debug_Events_msg_forest_set": "[EVENTS] Устанавливаю обработчики для леса!",
        "Debug_Events_msg_forest_del": "[EVENTS] Удаляю обработчики для леса!",
        "Debug_forest_cow_takeloot_msg": "[FOREST] Коровка вернулась, обрабатываем!",
        "Debug_forest_cow_takeloot_ok": "[FOREST] Забрал лут!",
        "Debug_forest_cow_go_msg": "[FOREST] Коровка не в лесу, обрабатываем!",
        "Debug_forest_cow_go_ok": "[FOREST] Отправил коровку в лес!",
        "Debug_forest_job_go_update": "[REDIS] Обновил таймер коровки в лесу!",
        "Debug_forest_npc_chick_msg": "[NPC] Сообщение с цыпой найдено, начинаю обработку!",
        "Debug_forest_npc_chick_ok": "[NPC] Цыпа обработана, продолжаем!",
        "Debug_forest_npc_ejik_msg": "[NPC] Сообщение с ежиком найдено, начинаю обработку!",
        "Debug_forest_npc_ejik_ok": "[NPC] Ежиха обработана, продолжаем!",
        "Debug_forest_npc_djun_msg": "[NPC] Сообщение с попугаем найдено, начинаю обработку!",
        "Debug_forest_npc_djun_ok": "[NPC] Попугай обработан, продолжаем!",
        "Debug_forest_npc_bear_msg": "[NPC] Сообщение с медведем найдено, начинаю обработку!",
        "Debug_forest_npc_bear_ok": "[NPC] Медведь обработан, продолжаем!",
        "Debug_forest_npc_jabomraz_msg": "[NPC] Сообщение с жабомразью найдено, начинаю обработку!",
        "Debug_forest_npc_jabomraz_ok": "[NPC] Жабомразь обработан, продолжаем!",
        "Debug_forest_npc_edinorog_msg": "[NPC] Сообщение с единорогом найдено, начинаю обработку!",
        "Debug_forest_npc_edinorog_ok": "[NPC] Единорожка обработана, продолжаем!",
        "Debug_forest_npc_belka_msg": "[NPC] Сообщение с белкой найдено, начинаю обработку!",
        "Debug_forest_npc_belka_ok": "[NPC] Белочка обработана, продолжаем!",
        # skins
        "config_bot_skin_show": "Показывать скин при открытии меню?\n True - Показывать,\n False - Не показывать.",
        "config_bot_skin_strings_id": "ID скина",
        "config_bot_skin_strings_hash": "Hash скина",
        "config_bot_skin_strings_bytes": "Bytes скина",
        # npc
        "config_bot_autoforest_npcs": "В списке - пропускаем.",
        "npc_jabomraz": "🐸 Жабомразь",
        "npc_chick": "🐤 цыпа",
        "npc_ejik": "💕🦔 Винди",
        "npc_djun": "🦜 Джун",
        "npc_djun_farm": "🦜 Ферма Джуна",
        "npc_bear": "🐻 Тэдди",
        "npc_edinorog": "🦄 Единорожка",
        "npc_belka": "🐿 Белочка",
        # Config message
        "config_bot_auto_forest_btn": "🌳Выгулять Коровку?",
        "config_bot_auto_forest": "🌳 Выгуливать коровку?\n  True - Выгуливать,\n False - Не выгуливать.",
        "config_bot_auto_forest_skip_npc_btn": "🦄 Скипать Нпц?",
        "config_bot_auto_forest_skip_npc": "Скипать Нпц?\n  True - Скипать,\n False - Не скипать.",
        "config_bot_auto_craft": "Крафтить предметы?\n True - Крафтить,\n False - Не крафтить.",
        "config_bot_auto_craft_count": "Cколько предметов крафтить (за раз)?\n 1-100.",
        "config_bot_auto_craft_item_name": "Впишите сюда итем, который автокрафт будет крафтить\n"
                                           "Пример: масло, куки",
        "config_debug_diff_msg": "Выберите раздел для логов\n"
                                 "Redis - База данных,\n"
                                 "Forest - Автолес,\n"
                                 "Eating - Автохавка,\n"
                                 "Crafting - Автокраф,\n"
                                 "State - Хендлеры\n"
                                 "General - Общие\n",
        "config_bot_auto_eat": "Кормить коровку?\n True - Кормить,\n False - Не кормить.",
        "config_bot_auto_eating": "Кормить коровку перед забиранием лута(с леса)?\n True - Кормить,\n False - Не кормить.",
        "config_bot_eat_use_count": "Сколько раз использовать еду?\n Указывать строго числа 0-9.",
        "config_bot_eat_use_item": "Чем кормить коровку?\n травка, брокколи, молоко+, холли-суп, милк-шейк",
        "config_bot_eat_lvl": "Со скольки процентов сытости начинать кормить?\n0-99",
        "config_redis_cloud_link": "Ссылка для подключения к хранилищу Redis\n"
                                   "Ссылку брать на Redis.io",
        "config_debug_msg": "Сервисные сообщения модуля, нужны только для проверки работоспособности отдельных функций.\n"
                            "Переключает сообщения с пометками [NPC], [DEBUG] и т.д.\n"
                            "True - Включено,\n"
                            "False - Выключено",
        "config_bot_send_logs": "Куда отправлять логи?\n"
                                "False - Выключить логи,\n"
                                "me - Себе(в избранное),\n"
                                "default - дефолтный чат логов модуля,\n"
                                "ID - любой чат, который Вы укажите.\n",
        "config_bot_deletemsg_inbot": "Удалять сообщения(свои) в боте после отправки?\n"
                                      "True< - Удалять,\n"
                                      "False - Не удалять.\n",
        "config_bot_used_bot": "username или id бота, который будет использоваться для работы модуля,\nУкажите что-то одно:\n"
                               "💗 default - @moolokobot id: 1606812809 - Стандартный,\n"
                               "Любое другое значение из разрешенных:\n"
                               "💗 @moolokobot id: 1606812809 - Основной, лагает,\n"
                               "💙 @mooloko1bot id: 6467105350 - Дополнительный, лагает,\n"
                               "💜 @mooloko2bot id: 6396922937 - Второй дополнительный, лагает,\n"
                               "🦄 @ultramoobot id: 5641915741 - Ультра, не лагает, работает только по подписке,\n"
                               "🇺🇦 @uamoobot id: 6770881933 - Украинский, не лагает,\n",
        "config_bot_used_chat_id": "Если хотите чтобы модуль работал не только в боте, но и в чате, укажите Chat_id",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "config_debug_diff_msg",
                [],
                self.strings["config_debug_diff_msg"],
                validator=loader.validators.MultiChoice(["Forest", "Forest_click", "Forest_npc", "Forest_state", "Eating", "Eating_click",
                                                         "Eating_state", "Crafting", "Crafting_click", "Craft_state", "Redis", "State", "General"]),
            ),
            loader.ConfigValue(
                "config_debug_msg",
                False,
                self.strings["config_debug_msg"],
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "config_bot_deletemsg_inbot",
                False,
                self.strings["config_bot_deletemsg_inbot"],
                validator=loader.validators.Boolean(),
            ),
            loader.ConfigValue(
                "config_bot_send_logs",
                "me",
                lambda: self.strings["config_bot_send_logs"],
            ),
            loader.ConfigValue(
                "config_redis_cloud_link",
                "redis://default:S50OBWLodXYQHHeLwjWOB9xCxfGyF22H@redis-16447.c246.us-east-1-4.ec2.redns.redis-cloud.com:16447",
                lambda: self.strings["config_redis_cloud_link"],
                validator=loader.validators.Hidden(),
            ),
            loader.ConfigValue(
                "config_bot_used_bot",
                [],
                lambda: self.strings["config_bot_used_bot"],
                #validator=loader.validators.Integer(minimum=0),
                validator=loader.validators.MultiChoice(["1606812809", "6467105350", "6396922937", "5641915741", "6770881933"])
            ),
            loader.ConfigValue(
                "config_bot_used_chat_id",
                "-1001606812809",
                lambda: self.strings["config_bot_used_chat_id"],
                validator=loader.validators.Integer(minimum=-100999999999999999999)
            ),
            loader.ConfigValue(
                "config_bot_auto_eat",
                "False",
                lambda: self.strings["config_bot_auto_eat"],
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "config_bot_auto_eating_forest",
                "False",
                lambda: self.strings["config_bot_auto_eating_forest"],
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "config_bot_eat_use_count",
                "1",
                lambda: self.strings["config_bot_eat_use_count"],
                validator=loader.validators.Integer(minimum=0)
            ),
            loader.ConfigValue(
                "config_bot_eat_use_item",
                "брокколи",
                lambda: self.strings["config_bot_eat_use_item"],
                validator=loader.validators.String()
            ),
            loader.ConfigValue(
                "config_bot_eat_lvl",
                "50",
                lambda: self.strings["config_bot_eat_lvl"],
                validator=loader.validators.Integer(minimum=0)
            ),
            loader.ConfigValue(
                "config_bot_auto_craft",
                "False",
                lambda: self.strings["config_bot_auto_craft"],
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "config_bot_auto_craft_count",
                "50",
                lambda: self.strings["config_bot_auto_craft_count"],
                validator=loader.validators.Integer(minimum=0)
            ),
            loader.ConfigValue(
                "config_bot_auto_craft_item_name",
                "масло",
                lambda: self.strings["config_bot_auto_craft_item_name"],
                validator=loader.validators.String()
            ),
            loader.ConfigValue(
                "config_bot_auto_forest",
                "False",
                lambda: self.strings["config_bot_auto_forest"],
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "config_bot_auto_forest_skip_npc",
                "True",
                lambda: self.strings["config_bot_auto_forest_skip_npc"],
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "config_bot_autoforest_npcs",
                [],
                lambda: self.strings["config_bot_autoforest_npcs"],
                validator=loader.validators.MultiChoice(
                    ["npc_belka", "npc_jabomraz", "npc_edinorog", "npc_djun", "npc_djun_farm", "npc_chick",
                     "npc_bear", "npc_ejik"]),
            ),
            loader.ConfigValue(
                "config_bot_skin_show",
                "False",
                lambda: self.strings["config_bot_skin_show"],
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "config_bot_skin_strings_id",
                "5395592741939849449",
                lambda: self.strings["config_bot_skin_strings_id"],
            ),
            loader.ConfigValue(
                "config_bot_skin_strings_hash",
                "-7011006528981204019",
                lambda: self.strings["config_bot_skin_strings_hash"],
            ),
            loader.ConfigValue(
                "config_bot_skin_strings_bytes",
                "AQAAClpn9Gn8lOq0lTYlXzF9lctkuIA3lNI=",
                lambda: self.strings["config_bot_skin_strings_bytes"],
            ),
        )

    async def client_ready(self, client, *_):
        """
        Основная иницализация обьектов
        :param client:
        :param _:
        :return:
        """
        self.client = client
        self.db = 0
        self.redis = await aioredis.from_url(self.config["config_redis_cloud_link"],
                                                  encoding="utf-8",
                                                  decode_responses=True,
                                                  db=self.db)

        self.pubsub = self.redis.pubsub()
        self.debug = DebugLogger(self.client, self.config)
        await self.redis.config_set("notify-keyspace-events", "Ex")
        await self.pubsub.subscribe(f'__keyevent@{self.db}__:expired')

    @loader.command()
    async def fmoo(self, message: Message):
        """
        Инлайн-меню управления автофармом
        """
        chat_id = utils.get_chat_id(message)

        if self.config["config_bot_skin_show"]:
            sticker = InputDocument(
                id=self.config["config_bot_skin_strings_id"],
                access_hash=self.config["config_bot_skin_strings_hash"],
                file_reference = base64.b64decode(self.config["config_bot_skin_strings_bytes"]))

            await self.client.send_file(chat_id, sticker)

        msg, buttons = await self._moobot_info()
        await self.inline.form(
            message=message,
            text=msg,
            reply_markup=buttons
        )

    async def _moobot_info(self):
        """
        Inline Главное меню
        :return:
        """
        msg = (f'{self.strings["moo_menu"]}'
               f'\t\t{self.strings["auto_forest_menu"]}'
               f'\t\t{self.strings["auto_eating_menu"]}'
               f'\t\t{self.strings["auto_craft_menu"]}'
               f'\t\t{self.strings["settings_menu"]}'
               f'\t\t{self.strings["skin_menu"]}')
        markup = [
            [
                {"text": self.strings["auto_forest"], "callback": self.inline_forest_menu, "args": ()},
                {"text": self.strings["auto_eating"], "callback": self.inline_eating_menu, "args": ()},
            ],
            [
                {"text": self.strings["auto_craft"], "callback": self.inline_craft_menu, "args": ()},
                {"text": self.strings["settings"], "callback": self.inline_misc_menu, "args": ()},
            ],
            [{"text": self.strings["bot_skin_menu_key"], "callback": self.inline_skin_menu, "args": ()}],
            [{"text": self.strings["close_btn"], "callback": self.close_button, "args": ()}],
        ]
        return msg, markup

    async def moobot_info(self, call:InlineCall):
        """
        Inline Главное меню
        :param call:
        :return:
        """
        msg = (f'{self.strings["moo_menu"]}'
               f'\t\t{self.strings["auto_forest_menu"]}'
               f'\t\t{self.strings["auto_eating_menu"]}'
               f'\t\t{self.strings["auto_craft_menu"]}'
               f'\t\t{self.strings["settings_menu"]}'
               f'\t\t{self.strings["skin_menu"]}')
        markup = [
            [
                {"text": self.strings["auto_forest"], "callback": self.inline_forest_menu, "args": (call,)},
                {"text": self.strings["auto_eating"], "callback": self.inline_eating_menu, "args": (call,)},
            ],
            [
                {"text": self.strings["auto_craft"], "callback": self.inline_craft_menu, "args": (call,)},
                {"text": self.strings["settings"], "callback": self.inline_misc_menu, "args": (call,)},
            ],
            [{"text": self.strings["bot_skin_menu_key"], "callback": self.inline_skin_menu, "args": (call,)}],
            [{"text": self.strings["close_btn"], "callback": self.close_button, "args": ()}],
        ]
        await call.edit(msg, reply_markup=markup)

    async def inline_forest_menu(self, call: InlineCall):

        autoforest = f'{self.strings["on"]}' if self.config["config_bot_auto_forest"] else f'{self.strings["off"]}'
        autonpc = f'{self.strings["on"]}' if self.config[
            "config_bot_auto_forest_skip_npc"] else f'{self.strings["off"]}'

        value = self.config["config_bot_autoforest_npcs"]
        categories = [
            "npc_belka", "npc_jabomraz", "npc_edinorog",
            "npc_djun", "npc_djun_farm", "npc_chick",
            "npc_bear", "npc_ejik"
        ]

        skipped_npcs = [self.strings.get(cat, cat) for cat in categories if cat in value]
        skipped_text = "\n".join(
            f'{self.strings["on"]} {npc}' for npc in
            skipped_npcs) if skipped_npcs else f'{self.strings["npc_not_skipped"]}'

        msg = (
                f'{self.strings["npc_menu"]}'
                f'{self.strings["npc_menu_autoforest"]} - <i>{autoforest}</i>\n'
                f'{self.strings["npc_menu_skip_status"]} - <i>{autonpc}</i>\n'
                f'{self.strings["npc_menu_skip"]}'
                f'{self.strings["npc_menu_skip_now"]}' + skipped_text
        )

        markup = [
            [
                {
                    "text": f"{self.strings['npc_menu_autoforest_btn']} {self.strings['on_btn'] if self.config['config_bot_auto_forest'] else self.strings['off_btn']}",
                    "callback": self.toggle_config_and_refresh,
                    "args": ("config_bot_auto_forest", self.inline_forest_menu)
                },
                {
                    "text": f"{self.strings['npc_menu_skip_status_btn']} {self.strings['on_btn'] if self.config['config_bot_auto_forest_skip_npc'] else self.strings['off_btn']}",
                    "callback": self.toggle_config_and_refresh,
                    "args": ("config_bot_auto_forest_skip_npc", self.inline_forest_menu)
                },
            ],
            [
                {
                    "text": self.strings["npc_autoskip"],
                    "callback": self.inline_forest_skip_menu,
                    "args": ()
                }
            ],
            [
                {"text": self.strings["back_btn"], "callback": self.back_button, "args": ()},
                {"text": self.strings["close_btn"], "callback": self.close_button, "args": ()}
            ],
        ]
        await call.edit(msg, reply_markup=markup)

    async def inline_skin_menu(self, call: InlineCall):
        skin_synced = all([
            self.config.get("config_bot_skin_strings_id"),
            self.config.get("config_bot_skin_strings_hash"),
            self.config.get("config_bot_skin_strings_bytes"),
        ])
        skin_show = self.config.get("config_bot_skin_show", False)

        msg = (
            ""
            f"{self.strings['skin_menu_txt']} {self.strings['on'] if skin_synced else self.strings['off']}\n"
            f" {self.strings['skin_menu_show_txt']} {self.strings['on_btn'] if skin_show else self.strings['off_btn']}"
        )

        markup = [
            [
                {
                    "text": f"{self.strings['skin_menu_show_skin_btn']} {self.strings['on_btn'] if skin_show else self.strings['off_btn']}",
                    "callback": self.toggle_config_and_refresh,
                    "args": ("config_bot_skin_show", self.inline_skin_menu)
                }
            ],
            [
                {
                    "text": self.strings["skin_menu_sync_skin_btn"],
                    "callback": self.button_sync_skin,
                    "args": ()
                }
            ],
            [{"text": self.strings["back_btn"], "callback": self.back_button, "args": ()},
             {"text": self.strings["close_btn"], "callback": self.close_button, "args": ()}
             ],
        ]

        await call.edit(msg, reply_markup=markup)

    async def inline_forest_skip_menu(self, call: InlineCall):
        value = self.config["config_bot_autoforest_npcs"]
        categories = [
            "npc_belka", "npc_jabomraz", "npc_edinorog",
            "npc_djun", "npc_djun_farm", "npc_chick",
            "npc_bear", "npc_ejik"
        ]

        msg = (
            f"<b>{self.strings['skip_menu_main_txt']}\n\n"
            f"\t\t{self.strings['skip_menu_main_on']}\n"
            f"\t\t{self.strings['skip_menu_main_off']}</b>\n\n"
        )

        for cat in categories:
            if cat in value:
                display_name = self.strings.get(cat, cat)
                msg += f"{display_name} {self.strings['skip_menu_main_skipped']}\n"

        markup = []
        row = []
        for i, cat in enumerate(categories):
            display_name = self.strings.get(cat, cat)
            mark = f"{self.strings['on_btn']}" if cat in value else f"{self.strings['off_btn']}"

            row.append({
                "text": f"{display_name}: {mark}",
                "callback": self.toggle_multi_choice,
                "args": ("config_bot_autoforest_npcs", cat, self.inline_forest_skip_menu),
            })

            if len(row) == 2 or i == len(categories) - 1:
                markup.append(row)
                row = []

        markup.append([{"text": self.strings["back_btn"], "callback": self.back_forest_button, "args": ()},
                       {"text": self.strings["close_btn"], "callback": self.close_button, "args": ()}
                       ])

        await call.edit(msg, reply_markup=markup)

    async def inline_eating_menu(self, call: InlineCall):
        auto_eat = f'{self.strings["on"]}' if self.config['config_bot_auto_eat'] else f'{self.strings["off"]}'
        eat_forest = f'{self.strings["on"]}' if self.config[
            'config_bot_auto_eating_forest'] else f'{self.strings["off"]}'
        item = self.config['config_bot_eat_use_item']
        count = self.config['config_bot_eat_use_count']
        lvl = self.config['config_bot_eat_lvl']

        msg = (
            f"{self.strings['auto_eat_main_menu_txt']}"
            f"\t\t<b>{self.strings['auto_eating_main_menu_txt']}</b> - <i>{auto_eat}</i>\n\n"
        f"\t\t<b>{self.strings['auto_eating_inforest_main_menu_txt']}</b> - <i>{eat_forest}</i>\n\n"
        f"\t\t<b>{self.strings['auto_eating_item']}</b> - <i>{item}</i>\n\n"
        f"\t\t<b>{self.strings['auto_eating_item_count']}</b> - <i>{count}</i>\n\n"
        f"\t\t<b>{self.strings['auto_eating_lvl']}</b> - <i>{lvl}%</i>\n"
        )

        markup = [
            [
                {
                    "text": f"{self.strings['auto_eating_main_menu_txt']} {self.strings['on_btn'] if self.config['config_bot_auto_eat'] else self.strings['off_btn']}",
                    "callback": self.toggle_config_and_refresh,
                    "args": ("config_bot_auto_eat", self.inline_eating_menu)},
                {
                    "text": f"{self.strings['auto_eating_inforest_main_menu_txt']} {self.strings['on_btn'] if self.config['config_bot_auto_eating_forest'] else self.strings['off_btn']}",
                    "callback": self.toggle_config_and_refresh,
                    "args": ("config_bot_auto_eating_forest", self.inline_eating_menu)},
            ],
            [
                {"text": f"{self.strings['auto_eating_item_count']} {count}",
                 "input": self.strings['auto_eating_inline_count'],
                 "handler": self.ask_config_value_handler,
                 "args": ("config_bot_eat_use_count",)},
                {"text": f"{self.strings['auto_eating_lvl']} - {lvl}%",
                 "input": self.strings['auto_eating_inline_lvl'],
                 "handler": self.ask_config_value_handler,
                 "args": ("config_bot_eat_lvl",)},
            ],
            [
                {"text": f"{self.strings['auto_eating_item']} {item}",
                 "input": self.strings['auto_eating_inline_item'],
                 "handler": self.ask_config_value_handler,
                 "args": ("config_bot_eat_use_item",)},
            ],
            [{"text": self.strings["back_btn"], "callback": self.back_button, "args": ()},
             {"text": self.strings["close_btn"], "callback": self.close_button, "args": ()}
             ],
        ]
        await call.edit(msg, reply_markup=markup)

    async def inline_craft_menu(self, call: InlineCall):
        auto_craft = f'{self.strings["on"] if self.config["config_bot_auto_craft"] else self.strings["off"]}'
        item = self.config['config_bot_auto_craft_item_name']
        count = self.config['config_bot_auto_craft_count']

        msg = (
            f"<b>{self.strings['craft_menu_main_txt']}</b>\n\n"
            f"<b>{self.strings['craft_menu_main_craft']}</b> - <i>{auto_craft}</i>\n"
            f"<b>{self.strings['craft_menu_main_craft_item']}</b> - <code>{item}</code>\n"
            f"<b>{self.strings['craft_menu_main_craft_count']}</b> - <code>{count}</code>"
        )

        markup = [
            [
                {
                    "text": f"{self.strings['craft_menu_main_craft']} {self.strings['on_btn'] if self.config['config_bot_auto_craft'] else self.strings['off_btn']}",
                    "callback": self.toggle_config_and_refresh,
                    "args": ("config_bot_auto_craft", self.inline_craft_menu)},
            ],
            [
                {
                    "text": f"{self.strings['craft_menu_main_craft_item']} {item}",
                    "input": self.strings['craft_menu_main_craft_item_inline'],
                    "handler": self.ask_config_value_handler,
                    "args": ("config_bot_auto_craft_item_name", self.inline_craft_menu),
                }
            ],
            [
                {"text": f"{self.strings['craft_menu_main_craft_count']} {count}",
                 "input": self.strings['craft_menu_main_craft_count_inline'],
                 "handler": self.ask_config_value_handler,
                 "args": ("config_bot_auto_craft_count", self.inline_craft_menu)},
            ],
            [{"text": self.strings["back_btn"], "callback": self.back_button, "args": ()},
             {"text": self.strings["close_btn"], "callback": self.close_button, "args": ()}
             ],
        ]
        await call.edit(msg, reply_markup=markup)

    async def inline_misc_menu(self, call: InlineCall):
        msg = f"<b>{self.strings['misc_menu_main_txt']}</b>"
        markup = [
            [
                {
                    "text": f"{self.strings['misc_menu_main_debug']} {self.strings['on_btn'] if self.config['config_debug_msg'] else self.strings['off_btn']}",
                    "callback": self.toggle_config_and_refresh,
                    "args": ("config_debug_msg", self.inline_misc_menu)},
            ],
            [
                {
                    "text": f"{self.strings['misc_menu_main_deletemsg']} {self.strings['on_btn'] if self.config['config_bot_deletemsg_inbot'] else self.strings['off_btn']}",
                    "callback": self.toggle_config_and_refresh,
                    "args": ("config_bot_deletemsg_inbot", self.inline_misc_menu)},
            ],
            [
                {"text": f"{self.strings['misc_menu_main_logs_chat']} {self.config['config_bot_send_logs']}",
                 "input": self.strings['misc_menu_main_logs_chat_inline'],
                 "handler": self.ask_config_value_handler,
                 "args": ("config_bot_send_logs", self.inline_misc_menu)},
            ],
            [
                {"text": f"{self.strings['misc_menu_main_chat_id']} {self.config['config_bot_used_chat_id']}",
                 "input": self.strings['misc_menu_main_chat_id_inline'],
                 "handler": self.ask_config_value_handler,
                 "args": ("config_bot_used_chat_id", self.inline_misc_menu)},
            ],
            [
                {
                    "text": f"{self.strings['misc_menu_main_bots_id']} {', '.join(self.config['config_bot_used_bot']) or 'Нет'}",
                    "callback": self.inline_bot_select_menu,
                    "args": (call,)
                },
            ],
            [
                {"text": self.strings['misc_menu_main_debug_btn_menu'], "callback": self.inline_debug_menu, "args": ()},
            ],
            [{"text": self.strings["back_btn"], "callback": self.back_button, "args": ()},
             {"text": self.strings["close_btn"], "callback": self.close_button, "args": ()}
             ],
        ]
        await call.edit(msg, reply_markup=markup)

    async def inline_bot_select_menu(self, call: InlineCall, *args):
        msg = "<b>🤖 Выберите основного бота:</b>\nТекущий: "
        current = ", ".join(self.config["config_bot_used_bot"]) or "❌ Не выбран"

        msg += f"<code>{current}</code>"

        bots = [
            ("1606812809", "💗 @moolokobot"),
            ("6467105350", "💙 @mooloko1bot"),
            ("6396922937", "💜 @mooloko2bot"),
            ("5641915741", "🦄 @ultramoobot"),
            ("6770881933", "🇺🇦 @uamoobot"),
        ]

        markup = [
            [
                {
                    "text": f"{name} {'✅' if bot_id in self.config['config_bot_used_bot'] else '❌'}",
                    "callback": self.set_config_bot_used_bot,
                    "args": (bot_id, self.inline_bot_select_menu)
                }
            ] for bot_id, name in bots
        ]

        markup.append([
            {"text": "🗑 Очистить", "callback": self.clear_config_bot_used_bot, "args": (self.inline_bot_select_menu,)},
            {"text": "🔙 Назад", "callback": self.inline_misc_menu, "args": ()}
        ])

        await call.edit(msg, reply_markup=markup)

    async def set_config_bot_used_bot(self, call: InlineCall, bot_id: str, refresh_callback, *args):
        self.config["config_bot_used_bot"] = [bot_id]
        await refresh_callback(call)

    async def clear_config_bot_used_bot(self, call: InlineCall, refresh_callback, *args):
        self.config["config_bot_used_bot"] = []
        await refresh_callback(call)

    async def inline_debug_menu(self, call: InlineCall):
        msg = f"<b>{self.strings['debug_menu_main_txt']}</b>"
        value = self.config["config_debug_diff_msg"]
        categories = ["Forest", "Forest_click", "Forest_npc", "Forest_state", "Eating", "Eating_click", "Eating_state",
                      "Crafting", "Crafting_click", "Craft_state", "Redis", "State", "General"]
        markup = []
        row = []
        for i, cat in enumerate(categories):
            row.append({
                "text": f"{cat}: {self.strings['on_btn'] if cat in value else self.strings['off_btn']}",
                "callback": self.toggle_multi_choice,
                "args": ("config_debug_diff_msg", cat, self.inline_debug_menu),
            })
            if len(row) == 2 or i == len(categories) - 1:
                markup.append(row)
                row = []

        markup.append([{"text": self.strings["back_btn"], "callback": self.inline_misc_menu, "args": ()},
                       {"text": self.strings["close_btn"], "callback": self.close_button, "args": ()}
                       ])
        await call.edit(msg, reply_markup=markup)

    async def toggle_config_and_refresh(self, call: InlineCall, key, refresh_func):
        self.config[key] = not self.config[key]
        await refresh_func(call)

    async def ask_config_value_handler(self, call: InlineCall, value: str, key: str, back_func):
        self.config[key] = value
        await back_func(call)

    async def toggle_multi_choice(self, call: InlineCall, config_key: str, value: str, redraw_callback):
        current = list(self.config[config_key])
        if value in current:
            current.remove(value)
        else:
            current.append(value)

        try:
            self.config[config_key] = current
        except Exception as e:
            await call.answer("❌ Ошибка валидации")
            return

        await redraw_callback(call)

    async def syncskin_inline(self, call: InlineCall):
        await call.answer("🔄 Синхронизация началась...")

        chat_id = self.get_chat_id
        bot_id = self.config["config_bot_used_bot"]

        msg = await self.client.send_message(chat_id, "/cow")
        start_id = msg.id

        for _ in range(15):
            await asyncio.sleep(1)

            messages = await self.client.get_messages(chat_id, limit=10)
            for m in messages:
                if m.id > start_id and m.sticker:
                    sticker = m.media.document

                    self.config["config_bot_skin_strings_id"] = sticker.id
                    self.config["config_bot_skin_strings_hash"] = sticker.access_hash
                    file_reference_b64 = base64.b64encode(sticker.file_reference).decode()

                    self.config["config_bot_skin_strings_bytes"] = file_reference_b64

                    return await call.answer("✅ Скин синхронизирован!")

        await call.answer("⚠️ Стикер не получен — бот молчит?")

    async def button_sync_skin(self, call: InlineCall):
        await self.syncskin_inline(call)

    async def back_forest_button(self, call: InlineCall):
        """Вернуться обратно"""
        await call.answer("OK")
        await self.inline_forest_menu(call)

    async def back_button(self, call: InlineCall):
        """Вернуться обратно"""
        await call.answer("OK")
        msg, markup = await self._moobot_info()
        await call.edit(msg, reply_markup=markup)

    @staticmethod
    async def close_button(call: InlineCall):
        await call.answer("Закрываю...")
        await call.delete()

    @property
    def get_chat_id(self):
        """
        Проверяет наличие chat_id и bot_id в конфиге.
        Возвращает chat_id, если он есть, иначе bot_id.
        """
        bot_id = self.config["config_bot_used_bot"]
        chat_id = self.config["config_bot_used_chat_id"]

        if chat_id and chat_id != "-100":
            return int(chat_id)

        if bot_id:
            return int(bot_id)

    @loader.command()
    async def auto_eating(self, message):
        """Автоматически кормит персонажа, если уровень еды ниже 70%"""
         #TODO: Прикрутить к инлайн-хендлеру
        if not self.config["config_bot_auto_eat"]:
            return
        chat_id = self.get_chat_id

        await self.debug.eat_state(self.strings["Debug_Events_msg_set"])
        self.client.add_event_handler(self.eating_handler, events.NewMessage)
        self.client.add_event_handler(self.eating_handler, events.MessageEdited)

        msg = await self.client.send_message(chat_id, "/cow")
        await self.save_forest_msg(chat_id, "eating_msg", msg)



    async def eating_handler(self, event):
        chat_id = self.get_chat_id
        user_id = self.tg_id
        food = self.config["config_bot_eat_lvl"]
        if event.chat_id != chat_id:
            return

        if not event.is_reply:
            return
        eating_msg = await self.get_forest_msg(chat_id, "eating_msg")
        reply_msg = await event.get_reply_message()

        if not reply_msg or reply_msg.id != eating_msg["id"]:
            return

        text = event.raw_text
        await self.debug.eat(f"[DEBUG] Получен текст: {text}")

        match = re.search(r"🌿\s*хавчик\s*(\d+)%", text)

        if match:
            food_level = int(match.group(1))
            await self.debug.eat(f"[DEBUG] Найден уровень еды: {food_level}%")

            if food_level <= food:
                await self.save_forest_msg(chat_id, "food", event)
                await self.debug.eat(f"[ACTION] Еда {food_level}%, запускаю кормление")
                await self.eating()
            else:
                await self.debug.eat(f"[INFO] Еды {food_level}%, кормить не надо")
        elif "🌿 голодает" in text:
            await self.save_forest_msg(chat_id, "food", event)
            await self.debug.eat("[ACTION] Обнаружено голодание! Запускаю кормление")
            await self.eating()

    async def eating(self):
        """
        Ищет кнопку 'Брокколи' и использует её eat_use_count раз
        """
        use_count = 0
        user_id = self.tg_id
        chat_id = self.get_chat_id
        eat_use_count = self.config["config_bot_eat_use_count"]
        eat_use_item = self.config["config_bot_eat_use_item"]
        msg_data = await self.get_forest_msg(chat_id, "food")
        msg = await self.client.get_messages(chat_id, ids=msg_data["id"])

        if not msg.buttons:
            return await self.debug.eat_click("[EATING] Кнопки не найдены.")

        for _ in range(eat_use_count):
            for row in msg.buttons:
                for button in row:
                    if button.data.decode() == f"check_items {user_id}":
                        await msg.click(msg._buttons_flat.index(button))
                        await self.debug.eat_click("[EATING] Нажата кнопка 'check_items'")
                        await asyncio.sleep(2)

                        msg = await self.client.get_messages(chat_id, ids=msg_data["id"])
                        break

            for row in msg.buttons:
                for button in row:
                    if button.data.decode() == f"itemuse {user_id} {eat_use_item}":
                        await msg.click(msg._buttons_flat.index(button))
                        use_count += 1
                        await self.debug.eat_click(f"[EATING] Используем брокколи ({use_count}/{eat_use_count})")
                        await asyncio.sleep(3)
                        if use_count >= eat_use_count:
                            return await self.debug.eat_click("[EATING] Достигнут лимит использования брокколи. Завершаем.")

    @loader.command()
    async def auto_craft_txt(self, message):
        """
        Команда для автоматической работы авто-крафта
        """
        # Todo: Прикрутить это все к инлайн-хендлеру
        if not self.config["config_bot_auto_craft"]:
            return

        chat_id = self.get_chat_id

        await self.debug.craft_state(self.strings["Debug_Events_msg_set"])
        self.client.add_event_handler(self.craft_handler, events.NewMessage)
        self.client.add_event_handler(self.craft_handler, events.MessageEdited)

        msg = await self.client.send_message(chat_id, "/craft")
        await self.save_forest_msg(chat_id, "craft_msg", msg)

        await self.auto_forest_jobs(20, "del_auto_craft_handlers")

    async def craft_handler(self, event):
        chat_id = self.get_chat_id
        if event.chat_id != chat_id:
            return
        text = event.raw_text

        if "мин." in text:
            wait_time_match = re.search(r"(?:(\d+)\s*(?:час(?:а|ов)?|⏱))?\s*(\d+)\s*мин\.", text)
            if wait_time_match:
                hours = int(wait_time_match.group(1)) if wait_time_match.group(1) else 0
                minutes = int(wait_time_match.group(2)) if wait_time_match.group(2) else 0
                wait_time = (hours * 60 + minutes) * 60
                wait_time += 2 * 60
                await self.auto_forest_jobs(wait_time, "crafting")
                await self.debug.craft(self.strings["Debug_craft_job_ok"])

        if not event.is_reply:
            return
        craft_msg = await self.get_forest_msg(chat_id, "craft_msg")
        reply_msg = await event.get_reply_message()

        if not reply_msg or reply_msg.id != craft_msg["id"]:
            return

        if "Твой верстак" in text:
            if "готово" in text:
                await self.save_forest_msg(chat_id, "craft_take", event)
                await self.craft_take()

            elif "пусто" in text:
                await self.save_forest_msg(chat_id, "craft_check", event)
                await self.craft_start()

            elif "•50" in text:
                wait_time_match = re.search(r"(?:(\d+)\s*(?:час(?:а|ов)?|⏱))?\s*(\d+)\s*мин\.", text)
                if wait_time_match:
                    hours = int(wait_time_match.group(1)) if wait_time_match.group(1) else 0
                    minutes = int(wait_time_match.group(2)) if wait_time_match.group(2) else 0
                    wait_time = (hours * 60 + minutes) * 60
                    wait_time += 2 * 60
                    await self.auto_forest_jobs(wait_time, "crafting")
                    await self.debug.craft(self.strings["Debug_craft_job_ok"])

        elif "Что будем крафтить" in text:
            await self.save_forest_msg(chat_id, "craft_finall", event)
            await self.craft_finall()

    async def craft_take(self):
        """
        Ищет кнопку 'Забрать' и забирает предеты.
        """
        user_id = self.tg_id
        chat_id = self.get_chat_id
        msg_data = await self.get_forest_msg(chat_id, "craft_take")
        if msg_data:
            msg = await self.client.get_messages(chat_id, ids=msg_data["id"])
            if msg.buttons:
                for row in msg.buttons:
                    for button in row:
                        if button.data.decode() == f"craft {user_id} takeout":
                            await msg.click(msg._buttons_flat.index(button))
                            await self.debug.craft_click(self.strings["Debug_craft_take_ok"])
                            await asyncio.sleep(3)

    async def craft_start(self):
        """
        Ищет кнопку 'Скрафтить' и вызываем следующее меню
        """
        chat_id = self.get_chat_id
        user_id = self.tg_id
        msg_data = await self.get_forest_msg(chat_id, "craft_check")
        if msg_data:
            msg = await self.client.get_messages(chat_id, ids=msg_data["id"])
            if msg.buttons:
                for row in msg.buttons:
                    for button in row:
                        if button.data.decode() == f"craft {user_id} check":
                            await msg.click(msg._buttons_flat.index(button))
                            await self.debug.craft_click(self.strings["Debug_craft_start_ok"])
                            await asyncio.sleep(3)

    async def craft_finall(self):
        """
        Ищет кнопку 'Скрафтить' и вызываем следующее меню
        """
        chat_id = self.get_chat_id
        user_id = self.tg_id
        item_name = self.config["config_bot_auto_craft_item_name"]
        msg_data = await self.get_forest_msg(chat_id, "craft_finall")
        if msg_data:
            msg = await self.client.get_messages(chat_id, ids=msg_data["id"])
            if msg.buttons:
                for row in msg.buttons:
                    for button in row:
                        if button.data.decode().endswith(f"{user_id} f-craft {item_name}"):
                            await msg.click(msg._buttons_flat.index(button))
                            await asyncio.sleep(2)
                            await msg.reply("50")
                            await self.debug.craft_click(self.strings["Debug_craft_finall_ok"])

    @loader.command()
    async def auto_forest_txt(self, message):
        """
        Команда для автоматической работы авто-леса
        """
        if not self.config["config_bot_auto_forest"]:
            return

        chat_id = self.get_chat_id

        if self.config["config_bot_auto_eating_forest"]:
            await self.auto_eating(message)


        self.client.add_event_handler(self.forest_handler, events.NewMessage)
        self.client.add_event_handler(self.forest_handler, events.MessageEdited)
        await self.debug.forest_state(self.strings["Debug_Events_msg_set"])

        msg = await self.client.send_message(chat_id, "/forest")
        await self.save_forest_msg(chat_id, "forest_msg", msg)

        await self.auto_forest_jobs(20, "del_forest_handlers")


    async def forest_handler(self, event):
        chat_id = self.get_chat_id
        if event.chat_id != chat_id:
            return

        if not event.is_reply:
            return
        forest_msg = await self.get_forest_msg(chat_id, "mymsg")

        reply_msg = await event.get_reply_message()
        if not reply_msg and reply_msg.id != forest_msg["id"]:
            return

        text = event.raw_text

        if "Твоя коровка гуляет" in text:
            wait_time_match = re.search(r"через (?:(\d+) час(?:а|ов)? )?(\d+) минут", text)
            if wait_time_match:
                hours = int(wait_time_match.group(1)) if wait_time_match.group(1) else 0
                minutes = int(wait_time_match.group(2))
                wait_time = (hours * 60 + minutes) * 60
                wait_time += 2 * 60
                await self.auto_forest_jobs(wait_time, "takeloot")
                await self.debug.redis(self.strings["Debug_forest_job_go_update"])

        elif "🐤 цыпа" in text:
            if "npc_chick" in self.config["config_bot_autoforest_npcs"]:
                return
            await self.save_forest_msg(chat_id, "chick", event)
            await self.debug.forest_npc(self.strings["Debug_forest_npc_chick_msg"])
            await self.npc_chick()

        elif "💕🦔 Винди" in text:
            if "npc_ejik" in self.config["config_bot_autoforest_npcs"]:
                return
            await self.save_forest_msg(chat_id, "ejik", event)
            await self.debug.forest_npc(self.strings["Debug_forest_npc_ejik_msg"])
            await self.npc_ejik()

        elif "🦜 Джун" in text:
            if "npc_djun" in self.config["config_bot_autoforest_npcs"]:
                return
            await self.save_forest_msg(chat_id, "djun", event)
            await self.debug.forest_npc(self.strings["Debug_forest_npc_djun_msg"])
            await self.npc_djun()

        elif "🦜 Ферма Джуна" in text:
            if "npc_djun_farm" in self.config["config_bot_autoforest_npcs"]:
                return
            await self.save_forest_msg(chat_id, "djun", event)
            await self.debug.forest_npc(self.strings["Debug_forest_npc_djun_msg"])
            await self.npc_djun()

        elif "🐻 Тэдди" in text:
            if "npc_bear" in self.config["config_bot_autoforest_npcs"]:
                return
            await self.save_forest_msg(chat_id, "bear", event)
            await self.debug.forest_npc(self.strings["Debug_forest_npc_bear_msg"])
            await self.npc_bear()

        elif "🐸 Жабомразь" in text:
            if "npc_jabomraz" in self.config["config_bot_autoforest_npcs"]:
                return
            await self.save_forest_msg(chat_id, "jabomraz", event)
            await self.debug.forest_npc(self.strings["Debug_forest_npc_jabomraz_msg"])
            await self.npc_jabomraz()

        elif "🦄 Единорожка" in text:
            if "npc_edinorog" in self.config["config_bot_autoforest_npcs"]:
                return
            await self.save_forest_msg(chat_id, "edinorog", event)
            await self.debug.forest_npc(self.strings["Debug_forest_npc_edinorog_msg"])
            await self.npc_edinorog()

        elif "🐿 Белочка" in text:
            if "npc_belka" in self.config["config_bot_autoforest_npcs"]:
                return
            await self.save_forest_msg(chat_id, "belka", event)
            await self.debug.forest_npc(self.strings["Debug_forest_npc_belka_msg"])
            await self.npc_belka()

        elif any(trigger in text for trigger in ["Отправь коровку погулять", "не кушает травку"]):
            await self.save_forest_msg(chat_id, "go", event)
            await self.debug.forest_npc(self.strings["Debug_forest_cow_go_msg"])
            await self.auto_forest_go()

        elif any(trigger in text for trigger in [
            "коровка вернулась", "Коровка пришла", "пришла домой", "прискакала", "Проверишь лут",
            "Коровочка вернулась", "вернулась из леса", "коровка принесла"]):
            await self.save_forest_msg(chat_id, "go", event)
            await self.debug.forest_npc(self.strings["Debug_forest_cow_takeloot_msg"])
            await self.auto_forest_takeloot()

    async def auto_forest_go(self):
        """
        Ищет кнопку 'Гулять' и отправляет коровку на прогулку.
        """
        chat_id = self.get_chat_id
        user_id = self.tg_id
        msg_data = await self.get_forest_msg(chat_id, "go")
        if msg_data:
            msg = await self.client.get_messages(chat_id, ids=msg_data["id"])
            if msg.buttons:
                for row in msg.buttons:
                    for button in row:
                        if button.data.decode() == f"forest {user_id} go":
                            await msg.click(msg._buttons_flat.index(button))
                            await self.redis.delete(f"forest_msg:{chat_id}:go")
                            await self.debug.forest_click(self.strings["Debug_forest_cow_go_ok"])

    async def auto_forest_takeloot(self):
        """
        После прогулки проверяет, можно ли забрать лут.
        """
        chat_id = self.get_chat_id
        user_id = self.tg_id
        msg_data = await self.get_forest_msg(chat_id, "go")
        if msg_data:
            msg = await self.client.get_messages(chat_id, ids=msg_data["id"])
            if msg.buttons:
                for row in msg.buttons:
                    for button in row:
                        if button.data.decode() == f"forest {user_id} takeloot":
                            await msg.click(msg._buttons_flat.index(button))
                            await self.auto_forest_go()
                            await self.debug.forest_click(self.strings["Debug_forest_cow_takeloot_ok"])

    async def save_forest_msg(self, chat_id, action, msg):
        """
        Сохраняем сообщение с уникальным ключом в Redis
        """
        key = f"forest_msg:{chat_id}:{action}"
        data = {"id": msg.id, "text": msg.raw_text}
        await self.redis.set(key, json.dumps(data), ex=30)
        await self.debug.redis(f"[REDIS] Сохранил данные в временное хранилище!\n"
                        f"Данные: {data}")

    async def get_forest_msg(self, chat_id, action):
        """
        Получаем сообщение по уникальному ключу
        """
        key = f"forest_msg:{chat_id}:{action}"
        data = await self.redis.get(key)
        if data:
            await self.debug.redis(f"[REDIS] Получил данные из хранилища!\n"
                                    f"Ключ: {key}\n"
                                    f"Данные: {data}")
            return json.loads(data)
        return None


    @loader.loop(interval=1, autostart=True)
    async def listen_to_expired_keys(self):
        """
        Своеобразный слушатель для истекших TTL ключей редиса.
        Если ключ есть - отправляем в self.handle_expired_key()
        :return:
        """
        async for message in self.pubsub.listen():
            if message["type"] == "message":
                key = message["data"]
                await self.handle_expired_key(key)

    async def handle_expired_key(self, key):
        """
        Обработчик истекших ключей, чтоб не путать - все ключи подписываются.
        Ключ:Пользователь:Действие
        :param key:
        :return:
        """
        parts = key.split(":")
        if len(parts) < 3:
            return

        user_id = parts[1]
        action = parts[2]

        if str(user_id) != str(self.tg_id):
            return

        if action == "takeloot":
            await self.auto_forest_txt(None)

        elif action == "crafting":
            await self.auto_craft_txt(None)

        elif action == "del_forest_handlers":
            self.client.remove_event_handler(self.forest_handler, events.NewMessage)
            self.client.remove_event_handler(self.forest_handler, events.MessageEdited)
            await self.debug.forest_state(self.strings["Debug_Events_msg_del"])

        elif action == "del_auto_craft_handlers":
            self.client.remove_event_handler(self.craft_handler, events.NewMessage)
            self.client.remove_event_handler(self.craft_handler, events.MessageEdited)
            await self.debug.craft_state(self.strings["Debug_Events_msg_del"])

        elif action == "del_auto_eat_handlers":
            self.client.remove_event_handler(self.eating_handler, events.NewMessage)
            self.client.remove_event_handler(self.eating_handler, events.MessageEdited)
            await self.debug.eat_state(self.strings["Debug_Events_msg_del"])

    async def auto_forest_jobs(self, wait_time: int, action: str):
        """
        Сюда отправляются время и задание, мы его пакуем в ключ и отправляем с TTL на хранение в Redis.
        :param wait_time:
        :param action:
        :return:
        """
        chat_id = self.config["config_bot_used_chat_id"]
        user_id = self.tg_id
        key = f"forest_task:{user_id}:{action}"
        await self.redis.set(key, "pending", ex=wait_time)
        await self.debug.redis(f"[DEBUG] Таймер на {wait_time // 60} минут до {action} поставлен.")

    async def npc_ejik(self):
        """
        Обрабатывает появление НПЦ Ежиха.
        """
        chat_id = self.get_chat_id
        user_id = self.tg_id
        msg_data = await self.get_forest_msg(chat_id, "ejik")
        if msg_data:
            msg = await self.client.get_messages(chat_id, ids=msg_data["id"])
            if msg.buttons:
                for row in msg.buttons:
                    for button in row:
                        if button.data.decode() == f"npc_inter {user_id} wind leave":
                            await msg.click(msg._buttons_flat.index(button))
                            await self.debug.forest_npc(self.strings["Debug_forest_npc_ejik_ok"])

    async def npc_bear(self):
        """
        Обрабатывает появление НПЦ Медведя.
        """
        chat_id = self.get_chat_id
        user_id = self.tg_id
        msg_data = await self.get_forest_msg(chat_id, "bear")
        if msg_data:
            msg = await self.client.get_messages(chat_id, ids=msg_data["id"])
            if msg.buttons:
                for row in msg.buttons:
                    for button in row:
                        if button.data.decode() == f"npctrade {user_id} Тэдди no":
                            await msg.click(msg._buttons_flat.index(button))
                            await self.debug.forest_npc(self.strings["Debug_forest_npc_bear_ok"])

    async def npc_belka(self):
        """
        Обрабатывает появление НПЦ Белку.
        """
        chat_id = self.get_chat_id
        user_id = self.tg_id
        msg_data = await self.get_forest_msg(chat_id, "belka")
        if msg_data:
            msg = await self.client.get_messages(chat_id, ids=msg_data["id"])
            if msg.buttons:
                for row in msg.buttons:
                    for button in row:
                        if button.data.decode() == f"npctrade {user_id} Белочка no":
                            await msg.click(msg._buttons_flat.index(button))
                            await self.debug.forest_npc(self.strings["Debug_forest_npc_belka_ok"])

    async def npc_djun_farm(self):
        """
        Обрабатывает появление НПЦ Фермы Попугая.
        """
        chat_id = self.get_chat_id
        user_id = self.tg_id
        msg_data = await self.get_forest_msg(chat_id, "djun_farm")
        if msg_data:
            msg = await self.client.get_messages(chat_id, ids=msg_data["id"])
            if msg.buttons:
                for row in msg.buttons:
                    for button in row:
                        if button.data.decode() == f"npc_inter {user_id} goaway home":
                            await msg.click(msg._buttons_flat.index(button))
                            await self.debug.forest_npc(self.strings["Debug_forest_npc_djun_ok"])

    async def npc_djun(self):
        """
        Обрабатывает появление НПЦ Попугая.
        """
        chat_id = self.get_chat_id
        user_id = self.tg_id
        msg_data = await self.get_forest_msg(chat_id, "djun")
        if msg_data:
            msg = await self.client.get_messages(chat_id, ids=msg_data["id"])
            if msg.buttons:
                for row in msg.buttons:
                    for button in row:
                        if button.data.decode() == f"npc_inter {user_id} djun no":
                            await msg.click(msg._buttons_flat.index(button))
                            await self.debug.forest_npc(self.strings["Debug_forest_npc_djun_ok"])

    async def npc_edinorog(self):
        """
        Обрабатывает появление НПЦ Единорожка.
        """
        chat_id = self.get_chat_id
        user_id = self.tg_id
        msg_data = await self.get_forest_msg(chat_id, "edinorog")
        if msg_data:
            msg = await self.client.get_messages(chat_id, ids=msg_data["id"])
            if msg.buttons:
                for row in msg.buttons:
                    for button in row:
                        if button.data.decode() == f"npctrade {user_id} Единорожка no":
                            await msg.click(msg._buttons_flat.index(button))
                            await self.debug.forest_npc(self.strings["Debug_forest_npc_edinorog_ok"])

    async def npc_jabomraz(self):
        """
        Обрабатывает появление НПЦ Жабомразь.
        """
        chat_id = self.get_chat_id
        user_id = self.tg_id
        msg_data = await self.get_forest_msg(chat_id, "jabomraz")
        if msg_data:
            msg = await self.client.get_messages(chat_id, ids=msg_data["id"])
            if msg.buttons:
                for row in msg.buttons:
                    for button in row:
                        if button.data.decode() == f"npctrade {user_id} Жабомразь no":
                            await msg.click(msg._buttons_flat.index(button))
                            await self.debug.forest_npc(self.strings["Debug_forest_npc_jabomraz_ok"])

    async def npc_chick(self):
        """
        Обрабатывает появление НПЦ Цыпа.
        """
        chat_id = self.get_chat_id
        user_id = self.tg_id
        msg_data = await self.get_forest_msg(chat_id, "chick")
        if msg_data:
            msg = await self.client.get_messages(chat_id, ids=msg_data["id"])
            if msg.buttons:
                for row in msg.buttons:
                    for button in row:
                        if button.data.decode() == f"npc_inter {user_id} chick catch":
                            await msg.click(msg._buttons_flat.index(button))
                            await self.debug.forest_npc(self.strings["Debug_forest_npc_chick_ok"])

