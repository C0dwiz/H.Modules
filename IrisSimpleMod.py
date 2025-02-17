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
# Name: IrisSimpleMod
# Description: Module for basic interaction with Iris.
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# scope: IrisSimpleMod
# scope: IrisSimpleMod 1.0.1
# ---------------------------------------------------------------------------------

from .. import loader, utils

__version__ = (1, 0, 1)

@loader.tds
class IrisSimpleMod(loader.Module):
    """Модуль для базового взаимодействия с Ирисом"""
    strings = {"name": "IrisSimpleMod"}


    @loader.command(
        ru_doc="Проверить мешок"
    )
    async def bag(self, message):
        """Check bag"""
        async with self.client.conversation(5443619563) as conv:
            usermessage = await conv.send_message('мешок')
            await usermessage.delete()
            bagmessage = await conv.get_response()
        await utils.answer(message, 'Ваш мешок:\n' + bagmessage.text)
        await bagmessage.delete()
        

    @loader.command(
        ru_doc="Зафармить ирис-коины"
    )
    async def farm(self, message):
        """Farm iris-coins"""
        async with self.client.conversation(5443619563) as conv:
            usermessage = await conv.send_message('ферма')
            await usermessage.delete()
            farmmessage = await conv.get_response()
        await utils.answer(message, farmmessage.text)
        await farmmessage.delete()
        
    @loader.command(
        ru_doc="Вывести анкету"
    )
    async def irisstats(self, message):
        """Display user stats"""
        async with self.client.conversation(5443619563) as conv:
            usermessage = await conv.send_message('анкета')
            await usermessage.delete()
            statsmessage = await conv.get_response()
        await utils.answer(message, statsmessage.text)
        await statsmessage.delete()
        
    @loader.command(
        ru_doc="Вывести статистику ботов"
    )
    async def irisping(self, message):
        """Display bot stats"""
        async with self.client.conversation(5443619563) as conv:
            usermessage = await conv.send_message('🌺 Семейство ирисовых')
            await usermessage.delete()
            pingmessage = await conv.get_response()
        await utils.answer(message, pingmessage.text)
        await pingmessage.delete()

    
