"""Преобразование markup-а в список форматированных строк"""

from typing import Callable
import re
import inspect
from customtkinter_formatting_manager import Formatting, FormattedString
from utils import apply_arguments

TITLE_COLOR = "#274C77"

def __split_dsl_to_tagged_list(
    string: str, lstrip: bool = True, rstrip: bool = True
) -> list[tuple[str, list[tuple[str, str]]]]:
    """Разбивает строку с тэгами DSL на список кортежей.
     Каждый кортеж — строка символов + список тэгов в виде кортежа (тэг, аргументы тэга)

    :param string: Строка в формате словарной статьи в DSL
    :type string: str
    :param lstrip: Удалять ли пробельные символы в начале строки, `True` по умолчанию
    :type lstrip: bool, optional
    :param rstrip: Удалять ли пробельные символы в конце строки, `True` по умолчанию
    :type rstrip: bool, optional
    :return: Список строк символов и тэгов, которые требуется к ним применить
    :rtype: list[tuple[str, list[tuple[str, str]]]]
    """
    tag_match = re.match(
        r"^((?:.|\n)*?)\[(\w+?)(|[ 0-9].*?)\](.*?)\[/\2\]((?:.|\n)*)$", string
    )
    if not tag_match:
        if lstrip:
            string = string.lstrip()
        if rstrip:
            string = string.rstrip()
        return [(string, [])]
    prefix, tag, tag_attribute, internal, suffix = tag_match.groups()
    prefix = prefix.replace("\\", "")
    internal = internal.replace("\\", "")
    suffix = suffix.replace("\\", "")
    if lstrip:
        prefix = prefix.lstrip()
    if rstrip:
        suffix = suffix.rstrip()
    parsed_prefix = [(prefix, [])]
    parsed_internal = __split_dsl_to_tagged_list(internal, lstrip=False, rstrip=False)
    if tag == "m":
        s, tags = parsed_internal[0]
        parsed_internal = [(s, tags + [(tag, tag_attribute)])] + parsed_internal[1:]
    else:
        parsed_internal = [
            (s, tags + [(tag, tag_attribute)]) for s, tags in parsed_internal
        ]
    if suffix != "" and suffix[0] == "\n":
        parsed_suffix = [("\n", [])] + __split_dsl_to_tagged_list(suffix)
    else:
        parsed_suffix = __split_dsl_to_tagged_list(suffix, lstrip=False)
    list_of_tagged_strings = (
        (parsed_prefix if prefix != "" else [])
        + parsed_internal
        + (parsed_suffix if suffix != "" else [])
    )
    return list_of_tagged_strings

def __adapt_on_click_func(
    on_click: Callable[[str], None] | Callable[[], None] | None,
    substring: str,
    substring_adapter: Callable[[str], str] | None = None,
) -> Callable[[], None] | None:
    """Адаптировать функцию `on_click` для использования в ref-ссылке

    :param on_click: Функция `on_click`
    :type on_click: Callable[[str], None] | Callable[[], None] | None
    :param substring: Строка в тэге [ref]
    :type substring: str
    :param substring_adapter: Функция адаптирующая строку в тэге
     для создания правильной ссылки, None по умолчанию
    :type substring_adapter: Callable[[str], str] | None, optional
    :return: Функция нужного вида
    :rtype: Callable[[], None] | None
    """
    if not on_click:
        return None
    sig = inspect.signature(on_click)
    num_of_parameters = len(sig.parameters)
    if num_of_parameters == 1:
        if substring_adapter:
            return apply_arguments(on_click, substring_adapter(substring))
        else:
            return apply_arguments(on_click, substring)
    else:
        return on_click


def __parse_dsl_tag(
    substring: str,
    tag: str,
    tag_arguments: str,
    tag_info: dict[str],
    on_click: Callable[[str], None] | Callable[[], None] | None,
    substring_adapter: Callable[[str], str] | None = None,
) -> dict[str]:
    """Парсит DSL-тэг и возвращает словарь информации с нужными изменениями

	:param substring: Строка, заключённая в тэг
	:type substring: str
	:param tag: Тэг
	:type tag: str
	:param tag_arguments: Аргументы тэга
	:type tag_arguments: str
	:param tag_info: Начальный словарь информации
	:type tag_info: dict[str]
	:param on_click: Функция, выполняющаяся при нажатии на ref-ссылки
	:type on_click: Callable[[str], None] | Callable[[], None] | None
	:param substring_adapter: Функция адаптирующая строку в тэге для создания правильной ссылки, None по умолчанию
	:type substring_adapter: Callable[[str], str] | None, optional
	:return: Обновлённый словарь информации
	:rtype: dict[str]
	"""
	match tag:
		case 'c':
			if tag_arguments == '':
				tag_info["color"] = TITLE_COLOR
			else:
				tag_info["color"] = tag_arguments
		case 'm':
			if not tag_arguments.isnumeric():
				raise ValueError(f"Invalid tag: {tag, tag_arguments}")
			tag_info["tabs"] = int(tag_arguments)
		case 'u':
			tag_info["formatting"] |= Formatting.UNDERLINE
		case 'b':
			tag_info["formatting"] |= Formatting.BOLD
		case 'i':
			tag_info["formatting"] |= Formatting.ITALIC
		case 'ref':
			tag_info["on_click"] = __adapt_on_click_func(on_click, substring, substring_adapter)
		case _:
			raise ValueError(f"Unknown tag: {tag}")
	return tag_info


def parse_dsl(
    string: str, on_click: Callable[[str], None] | Callable[[], None] | None = None
) -> list[FormattedString]:
    """Преобразовать строку формата DSL в `list[FormattedString]` с нужным форматированием

    :param string: Строка в формате словарной статьи в DSL
    :type string: str
    :param on_click: Функция, которая вызывается по нажатии на ref-ссылки.
     Можно назначить функцию с аргументом типа `str` (текст ref-ссылки)
    :type on_click: Callable[[str], None] | Callable[[], None] | None, optional
    :return: Форматтированная строка для использования в CTkPrettyTextbox
    :rtype: list[FormattedString]
    """
    splitted_string = __split_dsl_to_tagged_list(string)
    list_of_formatted_strings: list[FormattedString] = []
    for substring, tags in splitted_string:
        tag_info = {"color": None, "formatting": Formatting.NONE, "on_click": None}
        for tag, tag_arguments in tags:
            tag_arguments = tag_arguments.lstrip()
            tag_info = __parse_dsl_tag(
                substring,
                tag,
                tag_arguments,
                tag_info,
                on_click,
                lambda string: re.sub(r"[ \d,]+^", "", string.lower()),
            )
        if "tabs" in tag_info:
            list_of_formatted_strings.append(FormattedSString("    " * tag_info["tabs"]))
        formatted_substring = FormattedString(
            substring,
            color=tag_info["color"],
            formatting=tag_info["formatting"],
            on_click=tag_info["on_click"],
        )
        list_of_formatted_strings.append(formatted_substring)
    return list_of_formatted_strings

def main():
    """пеп-8 требует написать что такое main()... дожили"""
    test_string = (
        "    [m1][b][c]АББРАЙ [/c][/b][i]прил[/i]. дождливый, дождлив;"
        "[b][ref]че̄ххч 2[/ref] ли аббрай[/b] осень \\[дождлива\\][/m]"
        "    [m0][c red]•[/c][c green]•[/c][c yellow]•[/c][c blue]•[/c][/m]\n"
    )
    print(parse_dsl(test_string, on_click=lambda text: print(f"REF-ссылка: <{text}>")))


if __name__ == "__main__":
    main()
