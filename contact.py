import re
from typing import NamedTuple

from exceptions import IncorrectContactData


class Contact(NamedTuple):
    """Определение типа данных для контакта"""

    surname: str
    name: str
    patronymic: str
    company: str
    work_phone: str
    personal_phone: str


def get_contact_data() -> Contact:
    """Запрос данных у пользователя, их проверка и форматирование"""

    surname = input("Фамилия: ").strip()
    name = input("Имя: ").strip()
    patronymic = input("Отчество: ").strip()

    company = re.sub(" +", " ", input("Организация: "))
    company = " ".join([company.strip() for company in company.split()])

    work_phone = re.sub("[^0-9\+]", "", input("Рабочий телефон: ")).strip()
    if not work_phone or len(work_phone) > 12:
        work_phone = ""

    personal_phone = re.sub(
        "[^0-9\+]", "", input("Личный телефон: ")).strip()
    if not personal_phone or len(personal_phone) > 12:
        personal_phone = ""

    if not all(
            [surname, name, patronymic, company, work_phone, personal_phone]
            ):
        raise IncorrectContactData

    return Contact(
        surname=surname,
        name=name,
        patronymic=patronymic,
        company=company,
        work_phone=work_phone,
        personal_phone=personal_phone
    )


def build_contact_data(contact: dict) -> Contact:
    """Построение объекта на основе словаря с пользовательcкими данными"""

    return Contact(
        surname=contact["surname"],
        name=contact["name"],
        patronymic=contact["patronymic"],
        company=contact["company"],
        work_phone=contact["work_phone"],
        personal_phone=contact["personal_phone"]
    )
