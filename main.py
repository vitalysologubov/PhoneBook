import argparse
import json
import logging
import sys
from pathlib import Path

import config
from contact import build_contact_data, get_contact_data
from exceptions import IncorrectContactData, PageDoesNotExist
from storage import (JSONFileStorage, delete_contact, edit_contact,
                     find_contact, save_contact, show_contact)


def process_arguments():
    """
    Обработка аргументов из командной строки. Поддерживаются следующие команды:
    - help: вызов справки.
    - add: добавление новой записи.
    - show: постраничный вывод записей. Аргументы:
      --page: номер страницы (по умолчанию используется номер 1).
    - edit: редактирование записи. Аргументы:
      --id: идентификатор записи (обязательный аргумент);
      --surname: фамилия;
      --name: имя;
      --patronymic: отчество;
      --company: наименование организации;
      --work_phone: рабочий номер телефона;
      --personal_phone: личный номер телефона.
    - delete: удаление записи. Аргументы:
      --id: идентификатор записи (обязательный аргумент).
    - find: поиск записей. Аргументы:
      --surname: фамилия;
      --name: имя;
      --patronymic: отчество;
      --company: наименование организации;
      --work_phone: рабочий номер телефона;
      --personal_phone: личный номер телефона.
    """

    if len(sys.argv) == 1:
        print(
            "НЕ УКАЗАНА КОМАНДА С АРГУМЕНТАМИ.\nДля справки введите команду "
            "help."
            )
    else:
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers()

        help_command = subparsers.add_parser("help", help="Справка")
        help_command.set_defaults(func=process_help_command)

        add_command = subparsers.add_parser("add", help="Добавление записи")
        add_command.set_defaults(func=process_add_command)

        show_command = subparsers.add_parser(
            "show", help="Постраничный вывод записей")
        show_command.add_argument('--page', type=int, default=1)
        show_command.set_defaults(func=process_show_command)

        edit_command = subparsers.add_parser(
            "edit", help="Редактирование записи")
        edit_command.add_argument('--id', type=int, required=True)
        edit_command.add_argument('--surname', type=str)
        edit_command.add_argument('--name', type=str)
        edit_command.add_argument('--patronymic', type=str)
        edit_command.add_argument('--company', type=str)
        edit_command.add_argument('--work_phone', type=str)
        edit_command.add_argument('--personal_phone', type=str)
        edit_command.set_defaults(func=process_edit_command)

        delete_command = subparsers.add_parser("delete", help="Удаление записи")
        delete_command.add_argument('--id', type=int, required=True)
        delete_command.set_defaults(func=process_delete_command)

        find_command = subparsers.add_parser("find", help="Поиск записей")
        find_command.add_argument('--surname', type=str)
        find_command.add_argument('--name', type=str)
        find_command.add_argument('--patronymic', type=str)
        find_command.add_argument('--company', type=str)
        find_command.add_argument('--work_phone', type=str)
        find_command.add_argument('--personal_phone', type=str)
        find_command.set_defaults(func=process_find_command)

        args = parser.parse_args()
        args.func(args)


def init_logger() -> None:
    """
    Инициализация логгера. Сохраняет информацию о действиях с записями в файл
    config.LOG_FILE_NAME.
    """

    logging.basicConfig(
        format="%(asctime)s | %(levelname)-8s | %(message)s",
        filename=config.LOG_FILE_NAME,
        level=logging.INFO,
        encoding="UTF-8"
        )


def process_help_command(args: argparse.Namespace) -> None:
    """Обработка команды help. Вывод справочной информации."""

    print(
        "Поддерживаются команды:\n"
        "- help\n"
        "- add\n"
        "- show\n"
        "- edit\n"
        "- delete\n"
        "- find\n"
        "Например:\n"
        "- python main.py help\n"
        "- python main.py add\n"
        "- python main.py show --page 1\n"
        "- python main.py edit --company \"ООО 'Айти компания'\" --work_phone "
        "88121234567\n"
        "- python main.py delete --id 1\n"
        "- python main.py find --name Иван --surname Иванов"
        )


def process_add_command(args: argparse.Namespace) -> None:
    """
    Обработка команды add. Требуется указание всех запрашиваемых данных.
    Указанные данные сохраняются в хранилище данных.
    """

    print("ДОБАВЛЕНИЕ ЗАПИСИ.\nУкажите следующие данные:")

    try:
        contact_data = get_contact_data()
    except IncorrectContactData:
        print(
            "ЗАПИСЬ НЕ ДОБАВЛЕНА.\nНе указаны корректные данные:\n"
            "- Фамилия (например: Иванов)\n"
            "- Имя (например: Иван)\n"
            "- Отчество (например: Иванович)\n"
            "- Организация (например: ООО \"Айти компания\")\n"
            "- Рабочий телефон (например: 81002003040)\n"
            "- Личный телефон (например: +71002003040)"
        )
        exit(1)

    save_contact(
        contact=contact_data,
        storage=JSONFileStorage(Path.cwd() / config.PHONE_BOOK_JSON_FILE_NAME)
        )
    print("ЗАПИСЬ ДОБАВЛЕНА.")


def process_show_command(args: argparse.Namespace) -> None:
    """Обработка команды show. Постраничное отображение записей."""

    try:
        result = show_contact(
            page=args.page,
            storage=JSONFileStorage(
                Path.cwd() / config.PHONE_BOOK_JSON_FILE_NAME)
            )
    except PageDoesNotExist:
        print("СТРАНИЦА НЕ НАЙДЕНА.")
        exit(1)

    print(
        f"СТРАНИЦА {args.page}:\n"
        f"{json.dumps(result, indent=4, ensure_ascii=False)}"
        )


def process_edit_command(args: argparse.Namespace) -> None:
    """
    Обработка команды edit. Редактирование одного или нескольких полей записи.
    """

    contact_data = build_contact_data(contact=vars(args))
    edit_contact(
        contact_id=args.id,
        contact=contact_data,
        storage=JSONFileStorage(Path.cwd() / config.PHONE_BOOK_JSON_FILE_NAME)
        )
    print("ЗАПИСЬ ИЗМЕНЕНА.")


def process_delete_command(args: argparse.Namespace) -> None:
    """Обработка команды delete. Удаление записи из хранилища данных."""

    delete_contact(
        contact_id=args.id,
        storage=JSONFileStorage(Path.cwd() / config.PHONE_BOOK_JSON_FILE_NAME)
        )
    print("ЗАПИСЬ УДАЛЕНА.")


def process_find_command(args: argparse.Namespace) -> None:
    """Обработка команды find. Поиск записей одному или нескольким полям."""

    contact_data = build_contact_data(contact=vars(args))
    result = find_contact(
        contact=contact_data,
        storage=JSONFileStorage(Path.cwd() / config.PHONE_BOOK_JSON_FILE_NAME)
        )
    print(
        "РЕЗУЛЬТАТ ПОИСКА:\n"
        f"{json.dumps(result, indent=4, ensure_ascii=False)}")


if __name__ == "__main__":
    try:
        init_logger()
        process_arguments()
    except KeyboardInterrupt:
        exit(1)
