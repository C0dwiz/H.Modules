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
# Name: Weather
# Description: Advanced weather module with detailed information
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# scope: api Weather
# scope: api Weather 0.0.1
# ---------------------------------------------------------------------------------

import logging
import requests

from datetime import datetime
from typing import Union, Dict, List
from dataclasses import dataclass

from .. import loader, utils

logger = logging.getLogger(__name__)

DEFAULT_FORECAST_DAYS = 3
DEFAULT_HOURLY_INDEX = 4
WEATHER_API_URL = "https://wttr.in/{city}?format=j1&lang=en"


@dataclass
class WeatherCondition:
    """Represents a weather condition with its emoji."""

    condition: str
    emoji: str


@dataclass
class WindDirection:
    """Represents a wind direction with its description."""

    direction: str
    description: str


@dataclass
class ForecastDay:
    """Represents a single day's weather forecast."""

    date: str
    emoji: str
    condition: str
    temp_min: str
    temp_max: str
    wind_speed: str
    wind_direction: str


WEATHER_EMOJI: List[WeatherCondition] = [
    WeatherCondition("clear", "<emoji document_id=5402477260982731644>☀️</emoji>"),
    WeatherCondition("sunny", "<emoji document_id=5402477260982731644>☀️</emoji>"),
    WeatherCondition("partly cloudy", "<emoji document_id=5350424168615649565>⛅️</emoji>"),
    WeatherCondition("cloudy", "☁️<emoji document_id=5208563370218762357>☁️</emoji>"),
    WeatherCondition("overcast", "<emoji document_id=5208563370218762357>☁️</emoji>"),
    WeatherCondition("mist", "<emoji document_id=5449510395574229527>😶‍🌫️</emoji>"),
    WeatherCondition("fog", "<emoji document_id=5449510395574229527>😶‍🌫️</emoji>"),
    WeatherCondition("light rain", "<emoji document_id=5283097055852503586>🌦</emoji>"),
    WeatherCondition("rain", "<emoji document_id=5283243028905994049>🌧</emoji>"),
    WeatherCondition("heavy rain", "<emoji document_id=5282939632416206153>⛈</emoji>"),
    WeatherCondition("thunderstorm", "<emoji document_id=5282939632416206153>⛈</emoji>"),
    WeatherCondition("snow", "<emoji document_id=5282833267551117457>🌨</emoji>"),
    WeatherCondition("heavy snow", "<emoji document_id=5449449325434266744>❄️</emoji>"),
    WeatherCondition("sleet", "<emoji document_id=5282833267551117457>🌨</emoji>"),
    WeatherCondition("wind", "💨"),
]

WIND_DIRECTIONS: List[WindDirection] = [
    WindDirection("N", "⬆️ North"),
    WindDirection("NE", "↗️ Northeast"),
    WindDirection("E", "➡️ East"),
    WindDirection("SE", "↘️ Southeast"),
    WindDirection("S", "⬇️ South"),
    WindDirection("SW", "↙️ Southwest"),
    WindDirection("W", "⬅️ West"),
    WindDirection("NW", "↖️ Northwest"),
]

WIND_DIRECTIONS_RU: List[WindDirection] = [
    WindDirection("N", "⬆️ Северный"),
    WindDirection("NE", "↗️ Северо-восточный"),
    WindDirection("E", "➡️ Восточный"),
    WindDirection("SE", "↘️ Юго-восточный"),
    WindDirection("S", "⬇️ Южный"),
    WindDirection("SW", "↙️ Юго-западный"),
    WindDirection("W", "⬅️ Западный"),
    WindDirection("NW", "↖️ Северо-западный"),
]


@loader.tds
class Weather(loader.Module):
    """Advanced weather module with detailed information"""

    strings = {
        "name": "Weather",
        "no_city": "🚫 <b>Please specify a city</b>",
        "invalid_city": "🚫 <b>City not found</b>",
        "loading": "🔄 <b>Fetching weather data for {}</b>...",
        "error": "<emoji document_id=5980953710157632545>❌</emoji> <b>Error retrieving weather data</b>",
        "default_city": "<emoji document_id=5980930633298350051>✅</emoji> Default city set to: <code>{city}</code>",
        "weather_text": """<b>{emoji} Weather: {location}</b>

<b>📊 Current conditions:</b>
├ 🌡 Temperature: <code>{temp}°C</code>
├– <i>Feels like:</i> <code>{feels_like}°C</code>
├ 💧 Humidity: <code>{humidity}%</code>
├ 💨 Wind: <code>{wind_speed} km/h</code> {wind_direction}
├ 🌪 Pressure: <code>{pressure} mmHg</code>
├ 👁 Visibility: <code>{visibility} km</code>
└ ☁️ Cloudiness: <code>{clouds}</code>

<b>🌅 Time:</b>
├ 🌅 Sunrise: <code>{sunrise}</code>
├ 🌇 Sunset: <code>{sunset}</code>
└ ⏱ Local time: <code>{local_time}</code>

<b>📅 Forecast for {forecast_days} days:</b>
{forecast}
⏰ Updated: <code>{updated}</code>""",
        "forecast_day": """<b>{date}</b> {emoji}
├ 🌡 Temperature: {temp_min}°C ... {temp_max}°C
└ 💨 Wind: {wind_speed} km/h {wind_direction}

""",
    }

    strings_ru = {
        "no_city": "🚫 <b>Пожалуйста, укажите город</b>",
        "invalid_city": "🚫 <b>Город не найден</b>",
        "loading": "🔄 <b>Получаю метеоданные для {}</b>...",
        "default_city": "<emoji document_id=5980930633298350051>✅</emoji> Город по умолчанию установлен: <code>{city}</code>",
        "error": "<emoji document_id=5980953710157632545>❌</emoji> <b>Ошибка при получении данных о погоде</b>",
        "weather_text": """<b>{emoji} Погода: {location}</b>

<b>📊 Текущие условия:</b>
├ 🌡 Температура: <code>{temp}°C</code>
├– <i>Ощущается как:</i> <code>{feels_like}°C</code>
├ 💧 Влажность: <code>{humidity}%</code>
├ 💨 Ветер: <code>{wind_speed} км/ч</code> {wind_direction}
├ 🌪 Давление: <code>{pressure} мм.рт.ст</code>
├ 👁 Видимость: <code>{visibility} км</code>
└ ☁️ Облачность: <code>{clouds}</code>

<b>🌅 Время:</b>
├ 🌅 Восход: <code>{sunrise}</code>
├ 🌇 Закат: <code>{sunset}</code>
└ ⏱ Местное время: <code>{local_time}</code>

<b>📅 Прогноз на {forecast_days} дня:</b>
{forecast}
⏰ Обновлено: <code>{updated}</code>""",
        "forecast_day": """<b>{date}</b> {emoji}
├ 🌡 Температура: {temp_min}°C ... {temp_max}°C
└ 💨 Ветер: {wind_speed} км/ч {wind_direction}

""",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "default_city",
                None,
                lambda: "Default city for weather command",
            ),
            loader.ConfigValue(
                "language",
                "ru",
                lambda: "Language for weather output (en/ru)",
            ),
        )

    def get_weather_emoji(self, condition: str) -> str:
        """Get emoji for weather conditions"""
        condition = condition.lower()
        for item in WEATHER_EMOJI:
            if item.condition in condition:
                return item.emoji
        return "🌡"

    def get_wind_direction(self, direction: str) -> str:
        """Get wind direction description"""
        lang = self.config["language"]
        directions = WIND_DIRECTIONS_RU if lang == "ru" else WIND_DIRECTIONS
        for item in directions:
            if item.direction == direction.upper():
                return item.description
        return direction

    async def get_weather_data(self, city: str) -> Union[Dict, None]:
        """Get weather data from wttr.in"""
        lang = self.config["language"]
        url = WEATHER_API_URL.format(city=city)
        if lang == "ru":
            url = f"https://wttr.in/{city}?format=j1&lang=ru"
        try:
            response = await utils.run_sync(requests.get, url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch weather data for {city}: {e}")
            return None
        except Exception as e:
            logger.exception(f"Error fetching weather data: {e}")
            return None

    def format_forecast(self, forecast_data: list) -> str:
        """Format weather forecast for multiple days."""
        forecast_text = ""
        for day in forecast_data:
            hourly = day["hourly"][DEFAULT_HOURLY_INDEX]
            forecast_day = ForecastDay(
                date=day["date"],
                emoji=self.get_weather_emoji(hourly["weatherDesc"][0]["value"]),
                condition=hourly["weatherDesc"][0]["value"],
                temp_min=day["mintempC"],
                temp_max=day["maxtempC"],
                wind_speed=hourly["windspeedKmph"],
                wind_direction=self.get_wind_direction(hourly["winddir16Point"]),
            )

            forecast_text += self.strings("forecast_day").format(
                date=forecast_day.date,
                emoji=forecast_day.emoji,
                condition=forecast_day.condition,
                temp_min=forecast_day.temp_min,
                temp_max=forecast_day.temp_max,
                wind_speed=forecast_day.wind_speed,
                wind_direction=forecast_day.wind_direction,
            )
        return forecast_text

    async def process_weather_data(self, weather_data: Dict) -> str:
        """Process weather data and format the text."""
        current = weather_data["current_condition"][0]
        forecast = weather_data["weather"]
        location = (
            f"{weather_data['nearest_area'][0]['areaName'][0]['value']}, "
            f"{weather_data['nearest_area'][0]['country'][0]['value']}"
        )

        forecast_text = self.format_forecast(forecast[:DEFAULT_FORECAST_DAYS])

        return self.strings("weather_text").format(
            location=location,
            emoji=self.get_weather_emoji(current["weatherDesc"][0]["value"]),
            temp=current["temp_C"],
            feels_like=current["FeelsLikeC"],
            humidity=current["humidity"],
            wind_speed=current["windspeedKmph"],
            wind_direction=self.get_wind_direction(current["winddir16Point"]),
            pressure=current["pressure"],
            visibility=current["visibility"],
            clouds=current["weatherDesc"][0]["value"],
            sunrise=forecast[0]["astronomy"][0]["sunrise"],
            sunset=forecast[0]["astronomy"][0]["sunset"],
            local_time=current["observation_time"],
            forecast=forecast_text,
            forecast_days=DEFAULT_FORECAST_DAYS,
            updated=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )

    @loader.command(
        ru_doc="Узнайте погоду для указанного города",
        en_doc="Get the weather for the specified city",
    )
    async def weather(self, message):
        city = utils.get_args_raw(message) or self.config["default_city"]
        if not city:
            await utils.answer(message, self.strings("no_city"))
            return

        await utils.answer(message, self.strings("loading").format(city))

        weather_data = await self.get_weather_data(city)
        if not weather_data:
            await utils.answer(message, self.strings("error"))
            return

        try:
            weather_text = await self.process_weather_data(weather_data)
            await utils.answer(message, weather_text)

        except Exception as e:
            logger.exception(f"Error processing weather data: {e}")
            await utils.answer(message, self.strings("error"))

    @loader.command(
        ru_doc="Установите город по умолчанию для определения погоды",
        en_doc="Set the default city for weather",
    )
    async def weatherset(self, message):
        city = utils.get_args_raw(message)
        if not city:
            await utils.answer(message, self.strings("no_city"))
            return

        weather_data = await self.get_weather_data(city)
        if not weather_data:
            await utils.answer(message, self.strings("invalid_city"))
            return

        self.config["default_city"] = city
        await utils.answer(message, self.strings("default_city").format(city=city))
