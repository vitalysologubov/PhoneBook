import json
import logging
from datetime import datetime
from math import ceil
from pathlib import Path
from typing import TypedDict

import config
from contact import Contact
from exceptions import PageDoesNotExist


class HistoryContact(TypedDict):
    """Определение типа данных для записи контакта"""

    id: int
    date: str
    surname: str
    name: str
    patronymic: str
    company: str
    work_phone: str
    personal_phone: str


class PhoneBookStorage:
    """Интерфейс для создания любого хранилища данных телефонного справочника"""

    def save(self, contact: Contact) -> None:
        """Запись контакта"""

        raise NotImplementedError

    def show(self, page: int) -> list[HistoryContact]:
        """Постраничный вывод записей"""

        raise NotImplementedError

    def edit(self, contact_id: int, contact: Contact) -> None:
        """Редактирование записи"""

        raise NotImplementedError

    def delete(self, contact_id: int) -> None:
        """Удаление записи"""

        raise NotImplementedError

    def find(self, contact: Contact) -> list[HistoryContact]:
        """Поиск записей """

        raise NotImplementedError


class JSONFileStorage(PhoneBookStorage):
    """Реализация интерфейса хранилища данных в JSON формате"""

    def __init__(self, file: Path):
        self._file = file
        self._init_storage()

    def save(self, contact: Contact) -> None:
        """Запись контакта"""

        now = datetime.now()
        history = self._read_history()
        contact_id = 1

        if history:
            contact_id = history[-1]["id"] + 1

        history.append(
            {
                "id": contact_id,
                "date": str(now),
                "surname": contact.surname,
                "name": contact.name,
                "patronymic": contact.patronymic,
                "company": contact.company,
                "work_phone": contact.work_phone,
                "personal_phone": contact.personal_phone
            }
        )

        self._write_history(history)
        logging.info(f"Добавлен контакт с ID {contact_id}.")

    def show(self, page: int) -> list[HistoryContact]:
        """Постраничный вывод записей"""

        per_page = config.NUMBER_OF_ENTRIES_PER_PAGE
        history = self._read_history()
        total_pages = ceil(len(history) / per_page)

        if page < 1 or page > total_pages:
            raise PageDoesNotExist

        start = (page - 1) * per_page
        end = start + per_page
        return history[start:end]

    def edit(self, contact_id: int, contact: Contact) -> None:
        """Редактирование записи"""

        now = datetime.now()
        history = self._read_history()

        for record in history:
            if record["id"] == contact_id:
                record["date"] = str(now)

                if contact.surname:
                    record["surname"] = contact.surname
                if contact.name:
                    record["name"] = contact.name
                if contact.patronymic:
                    record["patronymic"] = contact.patronymic
                if contact.patronymic:
                    record["company"] = contact.company
                if contact.patronymic:
                    record["work_phone"] = contact.work_phone
                if contact.patronymic:
                    record["personal_phone"] = contact.personal_phone
                break

        self._write_history(history)
        logging.info(f"Изменён контакт с ID {contact_id}.")

    def delete(self, contact_id: int) -> None:
        """Удаление записи"""

        history = self._read_history()

        for index, record in enumerate(history):
            if record["id"] == contact_id:
                del history[index]

        self._write_history(history)
        logging.info(f"Удалён контакт с ID {contact_id}.")

    def find(self, contact: Contact) -> list[HistoryContact]:
        """Поиск записей """

        history = self._read_history()

        result = [
            record for record in history
            if record["surname"] == contact.surname or
            record["name"] == contact.name or
            record["patronymic"] == contact.patronymic or
            record["company"] == contact.company or
            record["work_phone"] == contact.work_phone or
            record["personal_phone"] == contact.personal_phone
            ]

        return result

    def _init_storage(self) -> None:
        """Инициализация хранилища данных"""

        if not self._file.exists():
            self._file.write_text("[]")

    def _read_history(self) -> list[HistoryContact]:
        """Чтение записей из файла"""

        with open(self._file, "r", encoding="UTF-8") as file:
            return json.load(file)

    def _write_history(self, history: list[HistoryContact]) -> None:
        """Сохранение записей в файл"""

        with open(self._file, "w", encoding="UTF-8") as file:
            json.dump(history, file, ensure_ascii=False, indent=4)


def save_contact(contact: Contact, storage: JSONFileStorage) -> None:
    """Сохранение контакта в хранилище данных"""

    storage.save(contact)


def show_contact(page, storage: JSONFileStorage) -> list[HistoryContact]:
    """Постраничное отображение записей из хранилища данных"""

    return storage.show(page)

def edit_contact(
        contact_id: int, contact: Contact, storage: JSONFileStorage) -> None:
    """Редактирование и сохранение записи в хранилище данных"""

    storage.edit(contact_id, contact)


def delete_contact(contact_id: int, storage: JSONFileStorage) -> None:
    """Удаление записи из хранилища данных"""

    storage.delete(contact_id)


def find_contact(
        contact: Contact, storage: JSONFileStorage) -> list[HistoryContact]:
    """Поиск записей в хранилище данных"""

    return storage.find(contact)
