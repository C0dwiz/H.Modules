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
# Name: CryptoCurrency
# Description: Module for displaying current cryptocurrency exchange rates.
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# scope: Api CryptoCurrency
# scope: Api CryptoCurrency 0.0.1
# ---------------------------------------------------------------------------------

import aiohttp

from telethon import events
from .. import loader, utils


@loader.tds
class CryptoCurrencyMod(loader.Module):
    """Module for displaying current cryptocurrency exchange rates."""

    strings = {
        "name": "CryptoCurrency",
        "query_missing": "Please specify a cryptocurrency ticker or name.",
        "coin_not_found": "Cryptocurrency '{query}' not found.",
    }

    strings_ru = {
        "query_missing": "Пожалуйста, укажите тикер или название криптовалюты.",
        "coin_not_found": "Криптовалюта '{query}' не найдена.",
    }

    async def fetch_json(self, url):
        """Fetch JSON data from a given URL."""
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.json()

    async def get_exchange_rates(self):
        """Get exchange rates for RUB and EUR based on USD."""
        data = await self.fetch_json("https://open.er-api.com/v6/latest/USD")
        return data["rates"]["RUB"], data["rates"]["EUR"]

    async def find_coin(self, query):
        """Find a cryptocurrency by its name or symbol."""
        data = await self.fetch_json(
            "https://api.coinlore.net/api/tickers/?start=0&limit=100"
        )
        return next(
            (
                item
                for item in data["data"]
                if query.lower() in item["name"].lower()
                or query.lower() in item["symbol"].lower()
            ),
            None,
        )

    @loader.command(
        ru_doc="Отображает текущий курс криптовалюты в рублях, долларах США и евро",
        en_doc="Displays the current cryptocurrency rate in RUB, USD, and EUR",
    )
    async def crypto(self, message):
        query = utils.get_args_raw(message)
        if not query:
            return await utils.answer(message, self.strings("query_missing"))

        coin = await self.find_coin(query)
        if not coin:
            return await utils.answer(
                message, self.strings("coin_not_found").format(query=query)
            )

        price_usd = float(coin["price_usd"])
        usd_rub_rate, usd_eur_rate = await self.get_exchange_rates()

        price_rub = price_usd * usd_rub_rate
        price_eur = price_usd * usd_eur_rate

        response = self.format_response(coin, price_usd, price_rub, price_eur)
        await utils.answer(message, response)

    def format_response(self, coin, price_usd, price_rub, price_eur):
        """Format the response message with cryptocurrency information."""
        return (
            f"💰 {coin['name']} ({coin['symbol']})\n"
            f"USD: ${price_usd:.2f}\n"
            f"RUB: ₽{price_rub:.2f}\n"
            f"EUR: €{price_eur:.2f}\n"
        )
