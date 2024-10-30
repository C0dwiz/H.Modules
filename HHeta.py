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
# Name: HHeta
# Description: search modules hikka
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# scope: HHeta
# scope: HHeta 0.0.1
# ---------------------------------------------------------------------------------

import requests, aiohttp, asyncio, re, os, gdown, inspect, io, ast

from typing import List, Optional
from concurrent.futures import ThreadPoolExecutor

from .. import loader, utils


class Heta:
    def __init__(self):
        self.token = "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"
        self.repos = [
            "hikariatama/ftg",
            "MoriSummerz/ftg-mods",
            "vsecoder/hikka_modules",
            "AmoreForever/amoremods",
            "DziruModules/hikkamods",
            "C0dwiz/H.Modules",
            "coddrago/modules",
            "KorenbZla/HikkaModules",
            "kamolgks/Hikkamods",
            "thomasmod/hikkamods",
            "sqlmerr/hikka_mods",
            "N3rcy/modules",
            "dorotorothequickend/DorotoroModules",
            "anon97945/hikka-mods",
            "GD-alt/mm-hikka-mods",
            "SkillsAngels/Modules",
            "shadowhikka/sh.modules",
            "Den4ikSuperOstryyPer4ik/Astro-modules",
            "GeekTG/FTG-Modules",
            "SekaiYoneya/Friendly-telegram",
            "iamnalinor/FTG-modules",
            "blazedzn/ftg-modules",
            "skillzmeow/skillzmods_hikka",
            "HitaloSama/FTG-modules-repo",
            "D4n13l3k00/FTG-Modules",
            "Fl1yd/FTG-Modules",
            "Ijidishurka/modules",
            "trololo65/Modules",
            "AlpacaGang/ftg-modules",
            "KeyZenD/modules",
            "Yahikoro/Modules-for-FTG",
            "Sad0ff/modules-ftg",
            "m4xx1m/FTG",
            "CakesTwix/Hikka-Modules",
        ]

    async def search_modules_parallel(self, query: str) -> List[str]:
        """Search for modules in parallel across all repositories."""
        return await self._search_in_repos(query, self.search_repo)

    async def search_modules_by_command_parallel(self, query: str) -> List[str]:
        """Search for modules by command in parallel across all repositories."""
        return await self._search_in_repos(query, self.search_repo_by_command)

    async def _search_in_repos(self, query: str, search_method) -> List[str]:
        """Generic method to search repositories using a specified search method."""
        found_modules = []
        async with aiohttp.ClientSession() as session:
            tasks = [search_method(repo, query, session) for repo in self.repos]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for result in results:
                if isinstance(result, Exception):
                    # Log or handle the exception appropriately
                    print(f"Error occurred: {result}")
                elif result:
                    found_modules.extend(result)
        return found_modules

    async def search_repo(self, repo, query, session):
        url = f"https://api.github.com/repos/{repo}/contents"
        headers = {"Authorization": f"token {self.token}"}
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return [
                    {
                        "name": item["name"],
                        "repo": repo,
                        "commands": await self.get_commands_from_module(
                            item["download_url"], session
                        ),
                        "download_url": item["download_url"],
                    }
                    for item in data
                    if item["name"].endswith(".py")
                    and query.lower() in item["name"].lower()
                ]
            return []

    async def search_repo_by_command(self, repo, query, session):
        url = f"https://api.github.com/repos/{repo}/contents"
        headers = {"Authorization": f"token {self.token}"}
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                result = []
                for item in data:
                    if item["name"].endswith(".py"):
                        commands = await self.get_commands_from_module(
                            item["download_url"], session
                        ) or ["<emoji document_id=5427052514094619126>🙅‍♂️</emoji>"]
                        if any(
                            isinstance(cmd, dict)
                            and "name" in cmd
                            and query.lower() in cmd["name"].lower()
                            for cmd in commands
                        ):
                            result.append(
                                {
                                    "name": item["name"],
                                    "repo": repo,
                                    "commands": commands,
                                    "download_url": item["download_url"],
                                }
                            )
                return result
            return []

    async def get_commands_from_module(self, download_url, session):
        async with session.get(download_url) as response:
            if response.status == 200:
                content = await response.text()
                return self.extract_commands(content)
        return {}

    async def get_author_from_file(self, download_url):
        async with aiohttp.ClientSession() as session:
            async with session.get(download_url) as response:
                if response.status == 200:
                    content = await response.text()
                    author_line = next(
                        (
                            line
                            for line in content.split("\n")
                            if line.startswith("# meta developer:")
                        ),
                        None,
                    )
                    if author_line:
                        return author_line.split(":")[1].strip()
        return "???"

    async def get_module_description(self, download_url):
        async with aiohttp.ClientSession() as session:
            async with session.get(download_url) as response:
                if response.status == 200:
                    content = await response.text()
                    tree = ast.parse(content)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.ClassDef) and any(
                            isinstance(base, ast.Attribute) and base.attr == "Module"
                            for base in node.bases
                        ):
                            return ast.get_docstring(node) or ""
        return ""

    @staticmethod
    def extract_commands(content):
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return []

        commands = []

        def get_decorator_names(decorator_list):
            return [ast.unparse(decorator) for decorator in decorator_list]

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                for class_body_node in node.body:
                    if isinstance(
                        class_body_node, (ast.FunctionDef, ast.AsyncFunctionDef)
                    ):
                        decorators = get_decorator_names(class_body_node.decorator_list)
                        is_loader_command = any(
                            "command" in decorator for decorator in decorators
                        )

                        if is_loader_command or class_body_node.name.endswith("cmd"):
                            method_docstring = ast.get_docstring(class_body_node)
                            command_name = class_body_node.name
                            if command_name.endswith("cmd"):
                                command_name = command_name[:-3]

                            command_info = {
                                "name": command_name,
                                "description": method_docstring or "",
                            }
                            commands.append(command_info)

        return commands


@loader.tds
class HHeta(loader.Module):
    """search modules hikka"""

    strings = {
        "name": "HHeta",
        "no_args": "⚠️ <b>Enter a query to search.</b>",
        "search": "🔎 <b>Searching...</b>",
        "no_modules": "❌ <b>No modules found.</b>",
        "commands_section": "\n<emoji document_id=5787544344906959608>ℹ️</emoji> <b>Commands:</b>\n{commands_list}",
        "result_done": (
            "<emoji document_id=5785209342986817408>🌎</emoji> <b>Result for {args}:</b>\n"
            "<emoji document_id=5785058280397082578>📂</emoji> <code>{module_name}</code> by <code>{author_info}</code>\n"
            "<emoji document_id=5787547716456287388>❔</emoji> <b>Description</b>: {description}\n"
            "{commands_section}\n\n"
            "<emoji document_id=5784891605601225888>🔵</emoji> <b>Download:</b> <code>{get_prefix}dlm {download_url}</code>"
        ),
    }

    strings_ru = {
        "no_args": "⚠️ <b>Введите запрос для поиска.</b>",
        "search": "🔎 <b>Поиск...</b>",
        "no_modules": "❌ <b>Модуль не найден.</b>",
        "commands_section": "\n<emoji document_id=5787544344906959608>ℹ️</emoji> <b>Командаы:</b>\n{commands_list}",
        "result_done": (
            "<emoji document_id=5785209342986817408>🌎</emoji> <b>Результат для {args}:</b>\n"
            "<emoji document_id=5785058280397082578>📂</emoji> <code>{module_name}</code> by <code>{author_info}</code>\n"
            "<emoji document_id=5787547716456287388>❔</emoji> <b>Описание </b>: {description}\n"
            "{commands_section}\n\n"
            "<emoji document_id=5784891605601225888>🔵</emoji> <b>Установить :</b> <code>{get_prefix}dlm {download_url}</code>"
        ),
    }

    @loader.command(
        ru_doc="<запрос> - поиск модулей.",
        en_doc="<query> - search modules.",
    )
    async def hheta(self, message):
        heta = Heta()
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings("no_args"))
            return

        await utils.answer(message, self.strings("search"))
        modules = await heta.search_modules_parallel(args)

        if not modules:
            args = args.replace(" ", "")
            modules = await heta.search_modules_parallel(args)

        if not modules:
            await utils.answer(message, self.strings("no_modules"))
        else:
            module = modules[0]
            repo_url = f"https://github.com/{module['repo']}"
            download_url = module["download_url"]

            commands_section = ""
            if module["commands"]:
                commands_list = "\n".join(
                    [
                        f"<emoji document_id=5787543653417225686>⏺</emoji> <code>{self.get_prefix()}{cmd['name']}</code> - {cmd['description']}"
                        for cmd in module["commands"]
                    ]
                )
                commands_section = self.strings("commands_section").format(
                    commands_list=commands_list
                )

            description = ""
            description = await heta.get_module_description(download_url)

            author_info = await heta.get_author_from_file(download_url)
            module_name = module["name"].replace(".py", "")
            result_index = 1

            result = self.strings("result_done").format(
                result_index=result_index,
                args=args,
                module_name=module_name,
                author_info=author_info,
                download_url=download_url,
                description=description,
                commands_section=commands_section,
                get_prefix=self.get_prefix(),
            )

            await utils.answer(message, result)
