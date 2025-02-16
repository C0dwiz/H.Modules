# meta developer: @archquise
# meta banner: https://envs.sh/M6F.png
# meta pic: https://emojio.ru/images/apple-b/1f36c.png
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

    