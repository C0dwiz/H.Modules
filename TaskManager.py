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
# Name: TaskManager
# Description: Manages tasks with Telegram commands and inline keyboards.
# Author: @hikka_mods
# ---------------------------------------------------------------------------------
# meta developer: @hikka_mods
# scope: TaskManager
# scope: TaskManager 0.0.1
# ---------------------------------------------------------------------------------

import datetime
import json
import logging
import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .. import loader, utils

logger = logging.getLogger(__name__)


@dataclass
class Task:
    """Represents a task."""

    description: str
    due_date: Optional[datetime.datetime] = None
    completed: bool = False
    created_at: datetime.datetime = field(default_factory=datetime.datetime.now)


class TaskManager:
    """Manages tasks, storing them in a JSON file."""

    def __init__(self, data_file: str):
        self.data_file = data_file
        self.tasks: Dict[int, List[Task]] = {}
        self.load_data()

    def load_data(self):
        """Loads task data from the JSON file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r") as f:
                    data = json.load(f)
                    self.tasks = {
                        int(user_id): [
                            Task(
                                description=task["description"],
                                due_date=datetime.datetime.fromisoformat(
                                    task["due_date"]
                                )
                                if task["due_date"]
                                else None,
                                completed=task["completed"],
                                created_at=datetime.datetime.fromisoformat(
                                    task["created_at"]
                                ),
                            )
                            for task in task_list
                        ]
                        for user_id, task_list in data.items()
                    }
            except (FileNotFoundError, json.JSONDecodeError) as e:
                logger.warning(f"Failed to load task data: {e}. Starting empty.")
                self.tasks = {}
        else:
            self.tasks = {}
            logger.info("Task data file not found. Starting empty.")

    def save_data(self):
        """Saves task data to the JSON file."""
        try:
            with open(self.data_file, "w") as f:
                data = {
                    user_id: [
                        {
                            "description": task.description,
                            "due_date": task.due_date.isoformat()
                            if task.due_date
                            else None,
                            "completed": task.completed,
                            "created_at": task.created_at.isoformat(),
                        }
                        for task in task_list
                    ]
                    for user_id, task_list in self.tasks.items()
                }
                json.dump(data, f, indent=4, default=str)
        except IOError as e:
            logger.error(f"Failed to save task data: {e}")

    def add_task(self, user_id: int, task: Task):
        self.tasks.setdefault(user_id, []).append(task)
        self.save_data()

    def remove_task(self, user_id: int, index: int):
        if user_id in self.tasks and 0 <= index < len(self.tasks[user_id]):
            del self.tasks[user_id][index]
            self.save_data()
        else:
            logger.warning(f"Invalid index for removal: {index}, user: {user_id}")

    def complete_task(self, user_id: int, index: int):
        if user_id in self.tasks and 0 <= index < len(self.tasks[user_id]):
            self.tasks[user_id][index].completed = True
            self.save_data()
        else:
            logger.warning(f"Invalid index for completion: {index}, user: {user_id}")

    def get_tasks(self, user_id: int) -> List[Task]:
        return self.tasks.get(user_id, [])

    def clear_tasks(self, user_id: int):
        if user_id in self.tasks:
            self.tasks[user_id] = []
            self.save_data()
        else:
            logger.info(f"No tasks to clear for user: {user_id}")

    def get_task(self, user_id: int, index: int) -> Optional[Task]:
        return (
            self.tasks[user_id][index]
            if user_id in self.tasks and 0 <= index < len(self.tasks[user_id])
            else None
        )


@loader.tds
class TaskManagerModule(loader.Module):
    """Manages tasks with Telegram commands and inline keyboards."""

    strings = {
        "name": "TaskManager",
        "task_added": "<emoji document_id=5776375003280838798>✅</emoji> Task added.",
        "task_removed": "<emoji document_id=5776375003280838798>✅</emoji> Task removed.",
        "task_completed": "<emoji document_id=5776375003280838798>✅</emoji> Task completed.",
        "task_not_found": "<emoji document_id=5778527486270770928>❌</emoji> Task not found.",
        "no_tasks": "<emoji document_id=5956561916573782596>📄</emoji> No active tasks.",
        "task_list": "<emoji document_id=5956561916573782596>📄</emoji> Your tasks:\n{}",
        "invalid_index": "<emoji document_id=5778527486270770928>❌</emoji> Invalid index. Provide valid integer.",
        "description_required": "<emoji document_id=5879813604068298387>❗️</emoji> Provide task description.",
        "clear_confirmation": "⚠️ Delete all tasks?",
        "tasks_cleared": "✅ All tasks deleted.",
        "due_date_format": "<emoji document_id=5778527486270770928>❌</emoji> Invalid date. Use YYYY-MM-DD HH:MM.",
        "task_info": "<emoji document_id=6028435952299413210>ℹ</emoji> Task: {description}\n<emoji document_id=5967412305338568701>📅</emoji> Due: {due_date}\n<emoji document_id=5825794181183836432>✔️</emoji> Completed: {completed}\n<emoji document_id=5936170807716745162>🎛</emoji> Created: {created_at}",
        "confirm_clear": "Confirm",
        "cancel_clear": "Cancel",
        "clear_cancelled": "❌ Deletion cancelled.",
        "index_required": "⚠️ Provide task index.",
        "clear_confirmation_text": "Are you sure you want to clear all tasks?",
        "confirm": "Confirm",
        "cancel": "Cancel",
    }

    strings_ru = {
        "task_added": "<emoji document_id=5776375003280838798>✅</emoji> Задача добавлена.",
        "task_removed": "<emoji document_id=5776375003280838798>✅</emoji> Задача удалена.",
        "task_completed": "<emoji document_id=5776375003280838798>✅</emoji> Задача выполнена.",
        "task_not_found": "<emoji document_id=5778527486270770928>❌</emoji> Задача не найдена.",
        "no_tasks": "<emoji document_id=5956561916573782596>📄</emoji> Нет активных задач.",
        "task_list": "<emoji document_id=5956561916573782596>📄</emoji> Ваши задачи:\n{}",
        "invalid_index": "<emoji document_id=5778527486270770928>❌</emoji> Неверный индекс. Укажите целое число.",
        "description_required": "<emoji document_id=5879813604068298387>❗️</emoji> Укажите описание задачи.",
        "clear_confirmation": "⚠️ Удалить все задачи?",
        "tasks_cleared": "✅ Все задачи удалены.",
        "due_date_format": "<emoji document_id=5778527486270770928>❌</emoji> Неверный формат даты. Используйте ГГГГ-ММ-ДД ЧЧ:ММ.",
        "task_info": "<emoji document_id=6028435952299413210>ℹ</emoji> Задача: {description}\n<emoji document_id=5967412305338568701>📅</emoji> Срок: {due_date}\n<emoji document_id=5825794181183836432>✔️</emoji> Выполнена: {completed}\n<emoji document_id=5936170807716745162>🎛</emoji> Создана: {created_at}",
        "confirm_clear": "Подтвердить",
        "cancel_clear": "Отменить",
        "clear_cancelled": "❌ Удаление отменено.",
        "index_required": "⚠️ Укажите индекс задачи.",
        "clear_confirmation_text": "Вы уверены, что хотите удалить все задачи?",
        "confirm": "Подтвердить",
        "cancel": "Отменить",
    }

    def __init__(self):
        self.task_manager: Optional[TaskManager] = None

    async def client_ready(self, client, db):
        self.task_manager = TaskManager(os.path.join(os.getcwd(), "tasks.json"))

    @loader.command(
        ru_doc="Добавить задачу:\n.taskadd <описание> | <дата (необязательно)>",
        en_doc="Add task:\n.taskadd <description> | <date (opt)>",
    )
    async def taskadd(self, message):
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings("description_required"))
            return

        try:
            description, due_date_str = (
                args.split("|", 1) if "|" in args else (args, None)
            )
            description = description.strip()
            due_date_str = due_date_str.strip() if due_date_str else None
            due_date = (
                datetime.datetime.fromisoformat(due_date_str) if due_date_str else None
            )
        except ValueError:
            await utils.answer(message, self.strings("due_date_format"))
            return
        except Exception as e:
            logger.error(f"Error adding task: {e}")
            await utils.answer(message, f"<emoji document_id=5778527486270770928>❌</emoji> Error: {e}")
            return

        task = Task(description=description, due_date=due_date)
        self.task_manager.add_task(message.sender_id, task)
        await utils.answer(message, self.strings("task_added"))

    @loader.command(
        ru_doc="[index] - удалить задачу",
        en_doc="[index] - remove task"
    )
    async def taskremove(self, message):
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings("index_required"))
            return

        try:
            index = int(args) - 1
        except ValueError:
            await utils.answer(message, self.strings("invalid_index"))
            return

        if self.task_manager.get_task(message.sender_id, index) is None:
            await utils.answer(message, self.strings("task_not_found"))
            return

        self.task_manager.remove_task(message.sender_id, index)
        await utils.answer(message, self.strings("task_removed"))

    @loader.command(
        ru_doc="[index] - Завершите задачу",
        en_doc="[index] - Complete task"
    )
    async def taskcomplete(self, message):
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings("index_required"))
            return

        try:
            index = int(args) - 1
        except ValueError:
            await utils.answer(message, self.strings("invalid_index"))
            return

        if self.task_manager.get_task(message.sender_id, index) is None:
            await utils.answer(message, self.strings("task_not_found"))
            return

        self.task_manager.complete_task(message.sender_id, index)
        await utils.answer(message, self.strings("task_completed"))

    @loader.command(
        ru_doc="Список задач",
        en_doc="List tasks"
    )
    async def tasklist(self, message):
        tasks = self.task_manager.get_tasks(message.sender_id)

        if not tasks:
            await utils.answer(message, self.strings("no_tasks"))
            return

        task_list_str = "\n".join(
            [
                f"  {i + 1}. {'<emoji document_id=5776375003280838798>✅</emoji>' if task.completed else '<emoji document_id=5778527486270770928>❌</emoji>'} {task.description} (Due: {task.due_date.strftime('%Y-%m-%d %H:%M') if task.due_date else 'None'})"
                for i, task in enumerate(tasks)
            ]
        )
        await utils.answer(message, self.strings("task_list").format(task_list_str))

    @loader.command(
        ru_doc="[index] - Посмотреть информацию о задаче",
        en_doc="[index] - Show task info",
    )
    async def taskinfo(self, message):
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings("index_required"))
            return
        try:
            index = int(args) - 1
        except ValueError:
            await utils.answer(message, self.strings("invalid_index"))
            return

        task = self.task_manager.get_task(message.sender_id, index)
        if not task:
            await utils.answer(message, self.strings("task_not_found"))
            return

        due_date_str = (
            task.due_date.strftime("%Y-%m-%d %H:%M") if task.due_date else "None"
        )
        created_at_str = task.created_at.strftime("%Y-%m-%d %H:%M")

        await utils.answer(
            message,
            self.strings("task_info").format(
                description=task.description,
                due_date=due_date_str,
                completed="Yes" if task.completed else "No",
                created_at=created_at_str,
            ),
        )

    @loader.command(
        ru_doc="Удалить все задачи",
        en_doc="Clear all tasks"
    )
    async def taskclear(self, message):
        await self.inline.form(
            text=self.strings("clear_confirmation_text"),
            message=message,
            reply_markup=[
                [
                    {"text": self.strings("confirm"), "callback": self.clear_confirm},
                    {"text": self.strings("cancel"), "callback": self.clear_cancel},
                ]
            ],
            silent=True,
        )

    async def clear_confirm(self, call):
        """Callback for confirming task clearing."""
        self.task_manager.clear_tasks(call.from_user.id)
        await call.edit(self.strings("tasks_cleared"))

    async def clear_cancel(self, call):
        """Callback for canceling task clearing."""
        await call.edit(self.strings("clear_cancelled"))