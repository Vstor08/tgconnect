from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from itertools import islice

def keyboard_builder_inline(button_texts: list[str], rows: int, cols: int) -> InlineKeyboardMarkup:
    """
    Строит клавиатуру с заданным числом строк и колонн.
    :param button_texts: список подписей кнопок
    :param rows: максимальное количество строк
    :param cols: максимальное количество колонн в каждой строке
    :return: InlineKeyboardMarkup
    """
    keyboard = []
    iterator = iter(button_texts)

    for _ in range(rows):
        row = list(islice(iterator, cols))
        if not row:
            break
        keyboard.append([
            InlineKeyboardButton(text=text, callback_data=text)
            for text in row
        ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def keyboard_builder_reply(button_texts: list[str], rows: int, cols: int) -> ReplyKeyboardMarkup:
    """
    Строит обычную клавиатуру с заданным числом строк и колонн.
    :param button_texts: список подписей кнопок
    :param rows: макс. количество строк
    :param cols: макс. количество колонн в строке
    :return: ReplyKeyboardMarkup
    """
    keyboard = []
    iterator = iter(button_texts)

    for _ in range(rows):
        row = list(islice(iterator, cols))
        if not row:
            break
        keyboard.append([
            KeyboardButton(text=text) for text in row
        ])

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
main_menu = keyboard_builder_reply(["команды","отправить файл","текст в буфер обмена"],rows=3,cols=1)
