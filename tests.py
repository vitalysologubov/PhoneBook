import json
import os
from pathlib import Path

import config
from contact import Contact, build_contact_data
from storage import JSONFileStorage, delete_contact, edit_contact, save_contact


def test_build_contact_data():
    """
    Тестирование построения объекта на основе словаря с пользовательcкими
    данными
    """

    dict_contact = {
        "surname": "Тестов",
        "name": "Тест",
        "patronymic": "Тестович",
        "company": "ООО \"Тестовая компания\"",
        "work_phone": "+70000000000",
        "personal_phone": "80000000000"
        }

    current_contact = Contact(
        surname = "Тестов",
        name = "Тест",
        patronymic = "Тестович",
        company = "ООО \"Тестовая компания\"",
        work_phone = "+70000000000",
        personal_phone = "80000000000"
    )

    builded_contact = build_contact_data(contact=dict_contact)
    assert current_contact == builded_contact


def test_save_json_file_storage():
    """Тестирование сохранение контакта в хранилище данных"""

    current_contact = Contact(
        surname = "Тестов",
        name = "Тест",
        patronymic = "Тестович",
        company = "ООО \"Тестовая компания\"",
        work_phone = "+70000000000",
        personal_phone = "80000000000"
    )

    save_contact(
        contact=current_contact,
        storage=JSONFileStorage(
            Path.cwd() / config.PHONE_BOOK_JSON_FILE_NAME_TEST)
        )

    with open(
            config.PHONE_BOOK_JSON_FILE_NAME_TEST,
            "r",
            encoding="UTF-8") as file:
        saved_contact = build_contact_data(contact=json.load(file)[-1])

    assert current_contact == saved_contact


def test_edit_json_file_storage():
    """Тестирование редактирования записи в хранилище данных"""

    current_contact = Contact(
        surname = "Тестов 2",
        name = "Тест 2",
        patronymic = "Тестович 2",
        company = "ООО \"Тестовая компания 2\"",
        work_phone = "+70000000002",
        personal_phone = "80000000002"
    )

    edit_contact(
        contact_id=1,
        contact=current_contact,
        storage=JSONFileStorage(
            Path.cwd() / config.PHONE_BOOK_JSON_FILE_NAME_TEST)
        )

    with open(
            config.PHONE_BOOK_JSON_FILE_NAME_TEST,
            "r",
            encoding="UTF-8") as file:
        edited_contact = build_contact_data(contact=json.load(file)[0])

    assert current_contact == edited_contact


def test_delete_json_file_storage():
    """Тестирование удаления записи из хранилища данных"""

    delete_contact(
        contact_id=1,
        storage=JSONFileStorage(
            Path.cwd() / config.PHONE_BOOK_JSON_FILE_NAME_TEST)
        )

    with open(
            config.PHONE_BOOK_JSON_FILE_NAME_TEST,
            "r",
            encoding="UTF-8") as file:
        edited_contact = json.load(file)

    os.remove(config.PHONE_BOOK_JSON_FILE_NAME_TEST)
    assert edited_contact == []
