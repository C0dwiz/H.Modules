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
# Name: UserbotAvast
# Description: A module for checking modules for security.
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# scope: UserbotAvast
# scope: UserbotAvast 0.0.1
# ---------------------------------------------------------------------------------

import logging
import ast
import astor
import requests
import base64
import zlib
import re
import urllib.parse

from .. import loader, utils

logger = logging.getLogger(__name__)

try:
    import g4f

    G4F_AVAILABLE = True
except ImportError:
    G4F_AVAILABLE = False
    logger.warning("g4f is not installed. AI analysis will be disabled.")


class SecurityAnalyzer:
    """
    Продвинутый анализатор безопасности Python-кода с эвристическим анализом.
    """

    SECURITY_KEYWORDS = {
        "critical": [
            {
                "keyword": "DeleteAccountRequest",
                "description": "Удаление аккаунта",
                "relevance": "Высокая",
            },
            {
                "keyword": "ResetAuthorizationRequest",
                "description": "Сброс авторизации",
                "relevance": "Высокая",
            },
            {
                "keyword": "client.export_session_string",
                "description": "Экспорт сессии",
                "relevance": "Высокая",
            },
            {
                "keyword": "edit_2fa",
                "description": "Изменение 2FA",
                "relevance": "Высокая",
            },
            {
                "keyword": "os.system",
                "description": "Системные команды",
                "relevance": "Высокая",
            },
            {
                "keyword": "subprocess.Popen",
                "description": "Внешние процессы",
                "relevance": "Высокая",
            },
            {
                "keyword": "eval",
                "description": "Выполнение кода (eval)",
                "relevance": "Критическая",
            },
            {
                "keyword": "exec",
                "description": "Выполнение кода (exec)",
                "relevance": "Критическая",
            },
            {
                "keyword": "MessagePacker.append",
                "description": "Патч MessagePacker",
                "relevance": "Средняя",
            },
            {
                "keyword": "MessagePacker.extend",
                "description": "Патч MessagePacker",
                "relevance": "Средняя",
            },
            {
                "keyword": "Scrypt",
                "description": "Класс Scrypt (подозрительно)",
                "relevance": "Высокая",
            },
            {
                "keyword": "socket.socket",
                "description": "Создание сокета",
                "relevance": "Высокая",
            },
            {
                "keyword": "shell=True",
                "description": "Использование shell=True в subprocess",
                "relevance": "Критическая",
            },
            {
                "keyword": "codecs.decode",
                "description": "Декодирование с использованием codecs",
                "relevance": "Средняя",
            },
            {
                "keyword": "pickle.loads",
                "description": "Десериализация (pickle)",
                "relevance": "Высокая",
            },
            {
                "keyword": "marshal.loads",
                "description": "Десериализация (marshal)",
                "relevance": "Высокая",
            },
            {
                "keyword": "__import__",
                "description": "Динамический импорт",
                "relevance": "Средняя",
            },
            {
                "keyword": "ctypes.CDLL",
                "description": "Загрузка динамической библиотеки",
                "relevance": "Высокая",
            },
            {
                "keyword": "create_connection",
                "description": "Установка соединения",
                "relevance": "Высокая",
            },
            {
                "keyword": "http.server",
                "description": "Запуск веб-сервера",
                "relevance": "Средняя",
            },
            {
                "keyword": "asyncio.create_subprocess_shell",
                "description": "Асинхронный запуск процесса через shell",
                "relevance": "Критическая",
            },
        ],
        "warning": [
            {
                "keyword": "requests",
                "description": "HTTP-запросы",
                "relevance": "Средняя",
            },
            {
                "keyword": "aiohttp",
                "description": "Асинхронные HTTP-запросы",
                "relevance": "Средняя",
            },
            {
                "keyword": "os.remove",
                "description": "Удаление файлов",
                "relevance": "Средняя",
            },
            {
                "keyword": "os.mkdir",
                "description": "Создание каталогов",
                "relevance": "Низкая",
            },
            {
                "keyword": "json.loads",
                "description": "Парсинг JSON",
                "relevance": "Низкая",
            },
            {
                "keyword": "open(..., 'w')",
                "description": "Открытие файла на запись",
                "relevance": "Средняя",
            },
            {
                "keyword": "open(..., 'a')",
                "description": "Открытие файла на добавление",
                "relevance": "Средняя",
            },
            {
                "keyword": "telnetlib.Telnet",
                "description": "Telnet соединение",
                "relevance": "Средняя",
            },
            {
                "keyword": "ftplib.FTP",
                "description": "FTP соединение",
                "relevance": "Средняя",
            },
            {
                "keyword": "shutil.move",
                "description": "Перемещение файлов",
                "relevance": "Средняя",
            },
            {
                "keyword": "shutil.copy",
                "description": "Копирование файлов",
                "relevance": "Средняя",
            },
            {
                "keyword": "threading.Thread",
                "description": "Создание потока",
                "relevance": "Низкая",
            },
            {
                "keyword": "multiprocessing.Process",
                "description": "Создание процесса",
                "relevance": "Низкая",
            },
            {
                "keyword": "queue.Queue",
                "description": "Использование очереди",
                "relevance": "Низкая",
            },
            {
                "keyword": "subprocess.check_output",
                "description": "Запуск процесса с захватом вывода",
                "relevance": "Средняя",
            },
            {
                "keyword": "subprocess.run",
                "description": "Запуск процесса",
                "relevance": "Средняя",
            },
            {
                "keyword": "codecs.encode",
                "description": "Кодирование с использованием codecs",
                "relevance": "Средняя",
            },
        ],
        "info": [
            {
                "keyword": "telethon",
                "description": "Использование Telethon",
                "relevance": "Низкая",
            },
            {
                "keyword": "pyrogram",
                "description": "Использование Pyrogram",
                "relevance": "Низкая",
            },
            {
                "keyword": "import",
                "description": "Импорт модулей",
                "relevance": "Низкая",
            },
            {
                "keyword": "print",
                "description": "Вывод в консоль",
                "relevance": "Низкая",
            },
            {
                "keyword": "logging.info",
                "description": "Логирование",
                "relevance": "Низкая",
            },
        ],
    }

    def __init__(self, ai_enabled: bool = False):
        """Инициализация анализатора."""
        self.results = {"critical": [], "warning": [], "info": []}
        self.reported_issues = set()
        self.code_lines = []
        self.is_decoded = False
        self.ai_enabled = ai_enabled

    def reset(self):
        """Сброс результатов анализа."""
        self.results = {"critical": [], "warning": [], "info": []}
        self.reported_issues = set()
        self.code_lines = []
        self.is_decoded = False

    async def analyze(self, code: str, strings: dict) -> str:
        """
        Выполняет анализ предоставленного Python-кода.

        Args:
            code: Python-код для анализа.
            strings: Словарь строк для локализации.

        Returns:
            Форматированный отчет об анализе.
        """
        self.reset()
        original_code = code

        try:
            code = self._try_decode(code)
            self.is_decoded = True
        except Exception:
            logger.warning("Не удалось расшифровать код, анализ как есть.")

        self.code_lines = code.splitlines()
        try:
            tree = ast.parse(code)
            self._visit_tree(tree)
            self._heuristic_analysis(code, tree)

            if self.ai_enabled and G4F_AVAILABLE:
                ai_analysis_result = await self._ai_analysis(code)
                if ai_analysis_result:
                    self.results["critical"].append(
                        {
                            "keyword": "AI Analysis",
                            "description": ai_analysis_result,
                            "relevance": "Критическая",
                            "line": 0,
                            "col": 0,
                        }
                    )

        except SyntaxError as e:
            logger.error(f"Ошибка синтаксиса в коде: {e}")
            return strings["syntax_error"].format(error=e)
        except Exception as e:
            logger.exception("Unexpected error during analysis")
            return strings["syntax_error"].format(error=str(e))

        return self._format_report(
            strings, original_code
        )

    async def _ai_analysis(self, code: str) -> str or None:
        """
        Использует g4f для анализа кода и выявления потенциальных угроз.
        """
        try:
            prompt = f"Проанализируйте следующий Python-код на предмет потенциальных угроз безопасности, уязвимостей и вредоносных действий.  Предоставьте подробное объяснение, если что-то будет обнаружено:\n\n{code}"
            response = await utils.run_sync(
                g4f.ChatCompletion.create,
                model=g4f.models.default,
                messages=[{"role": "user", "content": prompt}],
            )
            return str(response)
        except Exception as e:
            logger.error(f"Ошибка при анализе с помощью g4f: {e}")
            return None

    def _try_decode(self, code):
        """Попытка расшифровать base64 + zlib код."""
        if re.search(r"__import__\('zlib'\).decompress\(", code) and re.search(
            r"__import__\('base64'\).b64decode\(", code
        ):
            try:
                match = re.search(r"b'([A-Za-z0-9+/=]+)'", code)
                if match:
                    encoded_string = match.group(1)
                    decoded_code = self._decode_base64_zlib(encoded_string)
                    logger.info("Код успешно расшифрован.")
                    return decoded_code
            except Exception as e:
                logger.error(f"Ошибка при расшифровке кода: {e}")
                raise
        return code

    def _decode_base64_zlib(self, encoded_string):
        """Расшифровывает base64 + zlib код."""
        try:
            decoded_bytes = base64.b64decode(encoded_string)
            decompressed_bytes = zlib.decompress(decoded_bytes)
            return decompressed_bytes.decode("utf-8")
        except Exception as e:
            logger.error(f"Ошибка при расшифровке base64+zlib: {e}")
            raise

    def _get_line_from_code(self, lineno):
        """Получает строку кода по номеру строки."""
        try:
            return self.code_lines[lineno - 1]
        except IndexError:
            return ""

    def _visit_tree(self, tree):
        """Рекурсивно обходит AST-дерево."""
        for node in ast.walk(tree):
            self._analyze_node(node)

    def _analyze_node(self, node):
        """Анализирует отдельный узел AST."""
        if isinstance(node, ast.Name):
            self._check_keyword(node.id, node)
        elif isinstance(node, ast.Call):
            self._check_call(node)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            self._check_import(node)
        elif isinstance(node, ast.FunctionDef):
            self._check_function_def(node)
        elif isinstance(node, ast.ClassDef):
            self._check_class_def(node)
        elif isinstance(node, ast.Assign):
            self._check_assign(node)

    def _check_keyword(self, keyword, node):
        """Проверяет ключевые слова."""
        for severity, keywords in self.SECURITY_KEYWORDS.items():
            for item in keywords:
                if item["keyword"] == keyword:
                    issue_key = (
                        item["keyword"],
                        node.lineno,
                        node.col_offset,
                    )
                    if issue_key not in self.reported_issues:
                        self.results[severity].append(
                            {
                                "keyword": item["keyword"],
                                "description": item["description"],
                                "relevance": item["relevance"],
                                "line": node.lineno,
                                "col": node.col_offset,
                            }
                        )
                        self.reported_issues.add(issue_key)

    def _check_call(self, node):
        """Анализирует вызовы функций."""
        if isinstance(node.func, ast.Name):
            self._check_keyword(node.func.id, node)
        elif isinstance(node.func, ast.Attribute):
            full_attr = ""
            if isinstance(node.func.value, ast.Name):
                full_attr = node.func.value.id + "." + node.func.attr
                self._check_keyword(full_attr, node)
            else:
                self._check_keyword(node.func.attr, node)
        elif isinstance(
            node.func, ast.Subscript
        ):
            if isinstance(node.func.value, ast.Attribute):
                full_attr = ""
                if isinstance(node.func.value.value, ast.Name):
                    full_attr = node.func.value.value.id + "." + node.func.value.attr
                    self._check_keyword(full_attr, node)

    def _check_function_def(self, node):
        self._check_keyword(node.name, node)

    def _check_class_def(self, node):
        self._check_keyword(node.name, node)

    def _check_import(self, node):
        """Анализирует импорты."""
        if isinstance(node, ast.Import):
            for alias in node.names:
                self._check_keyword(alias.name, node)
        elif isinstance(node, ast.ImportFrom):
            self._check_keyword(node.module, node)
            for alias in node.names:
                self._check_keyword(alias.name, node)

    def _check_assign(self, node):
        """Анализирует присваивания."""
        for target in node.targets:
            if isinstance(target, ast.Name):
                self._check_keyword(target.id, node)

    def _heuristic_analysis(self, code: str, tree: ast.AST):
        """
        Эвристический анализ для обнаружения подозрительного кода.
        """
        self._check_obfuscation(code, tree)
        self._check_dynamic_code_generation(code, tree)
        self._check_url_patterns(code)
        self._check_api_abuse(tree)
        self._check_reverse_shell(code)
        self._check_file_operations(code)

    def _check_obfuscation(self, code: str, tree: ast.AST):
        """Обнаружение обфускации кода."""
        if len(re.findall(r"[A-Za-z0-9+/]{30,}", code)) > 2:
            issue_key = ("Base64", 1, 1)
            if issue_key not in self.reported_issues:
                self.results["warning"].append(
                    {
                        "keyword": "Base64",
                        "description": "Подозрительные строки Base64",
                        "relevance": "Средняя",
                        "line": 1,
                        "col": 1,
                    }
                )
                self.reported_issues.add(issue_key)

        if "zlib.decompress" in code:
            issue_key = ("zlib.decompress", 1, 1)
            if issue_key not in self.reported_issues:
                self.results["warning"].append(
                    {
                        "keyword": "zlib.decompress",
                        "description": "Использование zlib декомпрессии",
                        "relevance": "Средняя",
                        "line": 1,
                        "col": 1,
                    }
                )
                self.reported_issues.add(issue_key)

        for node in ast.walk(tree):
            if isinstance(node, (ast.Call)):
                if isinstance(node.func, ast.Name) and node.func.id in ("eval", "exec"):
                    if len(node.args) > 0 and isinstance(node.args[0], ast.Str):
                        obfuscated_string = node.args[0].s
                        if (
                            len(re.findall(r"[A-Za-z0-9+/]{30,}", obfuscated_string))
                            > 0
                        ):
                            issue_key = (
                                "eval/exec+Base64",
                                node.lineno,
                                node.col_offset,
                            )
                            if issue_key not in self.reported_issues:
                                self.results["critical"].append(
                                    {
                                        "keyword": "eval/exec+Base64",
                                        "description": "eval/exec с обфускацией Base64",
                                        "relevance": "Критическая",
                                        "line": node.lineno,
                                        "col": node.col_offset,
                                    }
                                )
                                self.reported_issues.add(issue_key)
                elif isinstance(node.func, ast.Name) and node.func.id in (
                    "eval",
                    "exec",
                ):
                    if len(node.args) > 0 and isinstance(node.args[0], ast.Name):
                        issue_key = ("eval/exec+Variable", node.lineno, node.col_offset)
                        if issue_key not in self.reported_issues:
                            self.results["critical"].append(
                                {
                                    "keyword": "eval/exec+Variable",
                                    "description": "eval/exec с переменной",
                                    "relevance": "Критическая",
                                    "line": node.lineno,
                                    "col": node.col_offset,
                                }
                            )
                            self.reported_issues.add(issue_key)

        hash_functions = ["md5", "sha1", "sha256", "sha512"]
        for hash_func in hash_functions:
            if f"hashlib.{hash_func}" in code:
                issue_key = (f"hashlib.{hash_func}", 1, 1)
                if issue_key not in self.reported_issues:
                    self.results["info"].append(
                        {
                            "keyword": f"hashlib.{hash_func}",
                            "description": f"Использование {hash_func} хеширования",
                            "relevance": "Низкая",
                            "line": 1,
                            "col": 1,
                        }
                    )
                    self.reported_issues.add(issue_key)

        if any(
            x in code
            for x in [
                "hashlib.md5(password.encode()).hexdigest()",
                "hashlib.sha256(password.encode()).hexdigest()",
            ]
        ):
            issue_key = ("Weak Hashing", 1, 1)
            if issue_key not in self.reported_issues:
                self.results["warning"].append(
                    {
                        "keyword": "Weak Hashing",
                        "description": "Использование хеширования без соли",
                        "relevance": "Средняя",
                        "line": 1,
                        "col": 1,
                    }
                )
                self.reported_issues.add(issue_key)

    def _check_dynamic_code_generation(self, code, tree: ast.AST):
        """Обнаружение динамической генерации кода."""
        if "compile(" in code:
            issue_key = ("compile", 1, 1)
            if issue_key not in self.reported_issues:
                self.results["warning"].append(
                    {
                        "keyword": "compile",
                        "description": "Использование compile() для генерации кода",
                        "relevance": "Средняя",
                        "line": 1,
                        "col": 1,
                    }
                )
                self.reported_issues.add(issue_key)

        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "type"
            ):
                if (
                    len(node.args) == 3
                    and isinstance(node.args[0], ast.Str)
                    and isinstance(node.args[1], ast.Tuple)
                    and isinstance(node.args[2], ast.Dict)
                ):
                    issue_key = ("type() class", node.lineno, node.col_offset)
                    if issue_key not in self.reported_issues:
                        self.results["warning"].append(
                            {
                                "keyword": "type() class",
                                "description": "Динамическое создание классов через type()",
                                "relevance": "Средняя",
                                "line": node.lineno,
                                "col": node.col_offset,
                            }
                        )
                        self.reported_issues.add(issue_key)

    def _check_url_patterns(self, code: str):
        """Обнаружение подозрительных URL-паттернов."""
        short_url_domains = [
            "bit.ly",
            "goo.gl",
            "t.co",
            "tinyurl.com",
            "is.gd",
            "ow.ly",
            "github.com",
            "raw.githubusercontent.com",
        ]
        for domain in short_url_domains:
            if domain in code:
                issue_key = (f"Short URL ({domain})", 1, 1)
                if issue_key not in self.reported_issues:
                    line = self._get_line_from_code(
                        1
                    )
                    match = re.search(r"(https?://\S+)", line)
                    url = (
                        match.group(1)
                        if match
                        else f"Не удалось извлечь URL ({domain})"
                    )
                    self.results["warning"].append(
                        {
                            "keyword": f"Short URL ({domain})",
                            "description": f"Обнаружен сокращенный URL: {url}",
                            "relevance": "Низкая",
                            "line": 1,
                            "col": 1,
                        }
                    )
                    self.reported_issues.add(issue_key)

        webhook_patterns = ["discord.com/api/webhooks", "api.telegram.org/bot"]
        for pattern in webhook_patterns:
            if pattern in code:
                issue_key = (f"Webhook ({pattern})", 1, 1)
                if issue_key not in self.reported_issues:
                    line = self._get_line_from_code(
                        1
                    )
                    match = re.search(pattern, line)
                    url = (
                        match.group(0)
                        if match
                        else f"Не удалось извлечь Webhook ({pattern})"
                    )

                    self.results["critical"].append(
                        {
                            "keyword": f"Webhook ({pattern})",
                            "description": f"Обнаружен Webhook: {url}",
                            "relevance": "Критическая",
                            "line": 1,
                            "col": 1,
                        }
                    )
                    self.reported_issues.add(issue_key)

    def _check_api_abuse(self, tree: ast.AST):
        """Обнаружение потенциального злоупотребления Telegram API."""
        send_methods = ["send_message", "send_file", "send_photo"]
        for node in ast.walk(tree):
            if isinstance(node, ast.For):
                for send_method in send_methods:
                    if send_method in astor.to_source(node):
                        issue_key = (
                            f"Mass {send_method}",
                            node.lineno,
                            node.col_offset,
                        )
                        if issue_key not in self.reported_issues:
                            self.results["warning"].append(
                                {
                                    "keyword": f"Mass {send_method}",
                                    "description": f"Подозрение на массовую рассылку ({send_method})",
                                    "relevance": "Средняя",
                                    "line": node.lineno,
                                    "col": node.col_offset,
                                }
                            )
                            self.reported_issues.add(issue_key)

        if "time.sleep(" in astor.to_source(tree):
            sleep_calls = re.findall(r"time\.sleep\((.*?)\)", astor.to_source(tree))
            for sleep_time in sleep_calls:
                try:
                    sleep_value = float(sleep_time)
                    if sleep_value < 1:
                        issue_key = ("Short Sleep Time", 1, 1)
                        if issue_key not in self.reported_issues:
                            self.results["warning"].append(
                                {
                                    "keyword": "Short Sleep Time",
                                    "description": "Обнаружена короткая задержка (менее 1 секунды)",
                                    "relevance": "Средняя",
                                    "line": 1,
                                    "col": 1,
                                }
                            )
                            self.reported_issues.add(issue_key)
                except ValueError:
                    pass

    def _check_reverse_shell(self, code: str):
        """Обнаружение попыток создания обратного шелла."""
        try:
            reverse_shell_patterns = [
                r"socket\.socket\(\s*socket\.AF_INET",
                r"os\.dup2\(",
                r"subprocess\.Popen\(\s*\[.+?\]\s*,\s*shell=True",
                r"/bin/bash -i",
                r"/bin/sh -i",
                r"nc -e /bin/bash",
                r"nc -e /bin/sh",
                r"> /dev/tcp/",
                r"python -c 'import socket,subprocess,os;s=socket.socket",
                r"python3 -c 'import socket,subprocess,os;s=socket.socket",
            ]
            for pattern in reverse_shell_patterns:
                if re.search(pattern, code):
                    issue_key = ("Reverse Shell", 1, 1)
                    if issue_key not in self.reported_issues:
                        self.results["critical"].append(
                            {
                                "keyword": "Reverse Shell",
                                "description": "Обнаружена попытка создания обратного шелла",
                                "relevance": "Критическая",
                                "line": 1,
                                "col": 1,
                            }
                        )
                        self.reported_issues.add(issue_key)
        except Exception as e:
            logger.error(f"Error in _check_reverse_shell: {e}")

    def _check_file_operations(self, code: str):
        """Обнаружение потенциально опасных операций с файлами."""
        dangerous_file_paths = [
            "/etc/passwd",
            "/etc/shadow",
            "/etc/hosts",
            "/etc/sudoers",
        ]
        for file_path in dangerous_file_paths:
            if file_path in code:
                issue_key = ("File Override", 1, 1)
                if issue_key not in self.reported_issues:
                    self.results["critical"].append(
                        {
                            "keyword": "File Override",
                            "description": f"Попытка записи в критический файл: {file_path}",
                            "relevance": "Критическая",
                            "line": 1,
                            "col": 1,
                        }
                    )
                    self.reported_issues.add(issue_key)

        if "shutil.rmtree" in code:
            issue_key = ("Recursive Delete", 1, 1)
            if issue_key not in self.reported_issues:
                self.results["warning"].append(
                    {
                        "keyword": "Recursive Delete",
                        "description": "Обнаружено рекурсивное удаление каталога",
                        "relevance": "Средняя",
                        "line": 1,
                        "col": 1,
                    }
                )
                self.reported_issues.add(issue_key)

        executable_extensions = [".py", ".sh", ".bat", ".exe"]
        for ext in executable_extensions:
            if f"open(..., '{ext}'" in code or f"open(... + '{ext}'" in code:
                issue_key = ("Executable File Creation", 1, 1)
                if issue_key not in self.reported_issues:
                    self.results["warning"].append(
                        {
                            "keyword": "Executable File Creation",
                            "description": f"Обнаружено создание файла с расширением {ext}",
                            "relevance": "Средняя",
                            "line": 1,
                            "col": 1,
                        }
                    )
                    self.reported_issues.add(issue_key)

    def _format_report(self, strings: dict, original_code: str) -> str:
        """Форматирует отчет об анализе."""
        report = strings["report_header"]

        if self.is_decoded:
            report += "<b>⚠️ Код был расшифрован перед анализом.</b>\n\n"
        else:
            report += "<b>⚠️ Анализ проводился над исходным кодом, расшифровка не удалась.</b>\n\n"

        total_issues = 0
        for severity, issues in self.results.items():
            if issues:
                report += strings[f"{severity}_header"]
                total_issues += len(issues)
                for issue in issues:
                    report += strings["issue_format"].format(
                        keyword=issue["keyword"],
                        description=issue["description"],
                        relevance=issue["relevance"],
                        line=issue["line"],
                        col=issue["col"],
                    )
                report += "\n"

        if total_issues == 0:
            report += strings["no_issues"]
        else:
            report += strings["report_footer"].format(count=total_issues)

        return report


@loader.tds
class UserbotAvast(loader.Module):
    """A module for checking modules for security."""

    strings = {
        "name": "UserbotAvast",
        "cfg_ai_enabled": "Включить анализ с помощью AI (g4f)",
        "cfg_lingva_url": "Анализирует Python-код модуля на предмет потенциальных угроз безопасности, включая обфускацию и эвристические признаки.",
        "report_header": "<b>🛡️ Отчет об анализе безопасности модуля:</b>\n\n",
        "critical_header": "<b>🔴 Критические угрозы:</b>\n",
        "warning_header": "<b>🟠 Предупреждения:</b>\n",
        "info_header": "<b>🔵 Информация:</b>\n",
        "issue_format": "  - ⚠️ <code>{keyword}</code>: {description} (Важность: {relevance}, Строка: {line}, Позиция: {col})\n",
        "no_issues": "✅ Не обнаружено проблем безопасности.\n",
        "report_footer": "\nВсего обнаружено {count} проблем.\n",
        "syntax_error": "❌ Ошибка синтаксиса в коде: {error}\n",
        "loading": "⏳ Запуск анализатора безопасности...",
        "no_module": "⚠️ Не удалось получить код модуля. Убедитесь, что ссылка верна или прикрепите файл к сообщению.",
        "decoding_error": "⚠️ Обнаружен зашифрованный код, но не удалось его расшифровать.",
    }

    strings_ru = {
        "cfg_ai_enabled": "Включить анализ с помощью AI (g4f)",
        "cfg_lingva_url": "Анализирует Python-код модуля на предмет потенциальных угроз безопасности, включая обфускацию и эвристические признаки.",
        "report_header": "<b>🛡️ Отчет об анализе безопасности модуля:</b>\n\n",
        "critical_header": "<b>🔴 Критические угрозы:</b>\n",
        "warning_header": "<b>🟠 Предупреждения:</b>\n",
        "info_header": "<b>🔵 Информация:</b>\n",
        "issue_format": "  - ⚠️ <code>{keyword}</code>: {description} (Важность: {relevance}, Строка: {line}, Позиция: {col})\n",
        "no_issues": "✅ Не обнаружено проблем безопасности.\n",
        "report_footer": "\nВсего обнаружено {count} проблем.\n",
        "syntax_error": "❌ Ошибка синтаксиса в коде: {error}\n",
        "loading": "⏳ Запуск анализатора безопасности...",
        "no_module": "⚠️ Не удалось получить код модуля. Убедитесь, что ссылка верна или прикрепите файл к сообщению.",
        "decoding_error": "⚠️ Обнаружен зашифрованный код, но не удалось его расшифровать.",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "ai_enabled",
                False,
                lambda: self.strings["cfg_ai_enabled"],
                validator=loader.validators.Boolean(),
            ),
        )

    async def client_ready(self, client, db):
        """Вызывается при готовности клиента."""
        self.client = client
        self.db = db
        self.security_analyzer = SecurityAnalyzer(self.config["ai_enabled"])

    @loader.unrestricted
    @loader.ratelimit
    async def checkmodcmd(self, message):
        """
        [module_link] или [reply file] или [send file] - выполняет проверку модуля на безопасность.
        """
        await utils.answer(message, self.strings["loading"])
        args = utils.get_args_raw(message)
        code = None

        if args:
            code = await self._get_code_from_url(args)

        if not code:
            code = await self._get_code_from_message(message)

        if not code:
            await utils.answer(message, self.strings["no_module"])
            return

        try:
            result = await self.security_analyzer.analyze(code, self.strings)
            await utils.answer(message, result)
        except Exception as e:
            logger.exception("Error during analysis")
            await utils.answer(message, f"An error occurred during analysis: {e}")

    async def _get_code_from_url(self, url: str) -> str or None:
        """Получает код модуля по URL."""
        try:
            response = await utils.run_sync(requests.get, url)
            response.raise_for_status()
            return response.text

        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при получении кода из URL: {e}")
            return None

    async def _get_code_from_message(self, message) -> str or None:
        """Получает код модуля из прикрепленного файла или ответа на сообщение."""
        try:
            if message.media:
                code = (await self.client.download_file(message.media, bytes)).decode(
                    "utf-8"
                )
                return code

            reply = await message.get_reply_message()
            if reply and reply.media:
                code = (await self.client.download_file(reply.media, bytes)).decode(
                    "utf-8"
                )
                return code
        except Exception as e:
            logger.error(f"Ошибка при получении кода из сообщения: {e}")
            return None
