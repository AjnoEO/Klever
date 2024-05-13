from customtkinter_formatting_manager import Formatting, FormattedString
from typing import Callable
import re
import inspect
from utils import apply_arguments

def __split_dsl_to_tagged_list(string: str, lstrip: bool = True, rstrip: bool = True) -> list[tuple[str, list[tuple[str, str]]]]:
	"""Разбивает строку с тэгами DSL на список кортежей. Каждый кортеж — строка символов + список тэгов в виде кортежа (тэг, аргументы тэга)

	:param string: Строка в формате словарной статьи в DSL
	:type string: str
	:param lstrip: Удалять ли пробельные символы в начале строки, `True` по умолчанию
	:type lstrip: bool, optional
	:param rstrip: Удалять ли пробельные символы в конце строки, `True` по умолчанию
	:type rstrip: bool, optional
	:return: Список строк символов и тэгов, которые требуется к ним применить
	:rtype: list[tuple[str, list[tuple[str, str]]]]
	"""
	re_expression = r"^((?:.|\n)*?)\[(\w+?)(|[ 0-9].*?)\](.*?)\[/\2\]((?:.|\n)*)$"
	tag_match = re.match(re_expression, string)
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
	if tag == 'm':
		s, tags = parsed_internal[0]
		parsed_internal = [(s, tags + [(tag, tag_attribute)])] + parsed_internal[1:]
	else:
		parsed_internal = [(s, tags + [(tag, tag_attribute)]) for s, tags in parsed_internal]
	if suffix != "" and suffix[0] == "\n":
		parsed_suffix = [("\n", [])] + __split_dsl_to_tagged_list(suffix)
	else:
		parsed_suffix = __split_dsl_to_tagged_list(suffix, lstrip=False)
	list_of_tagged_strings = (parsed_prefix if prefix != "" else []) \
		+ parsed_internal \
		+ (parsed_suffix if suffix != "" else [])
	return list_of_tagged_strings

def __adapt_on_click_func(on_click: Callable[[str], None] | Callable[[], None] | None, substring: str):
	if not on_click:
		return None
	sig = inspect.signature(on_click)
	num_of_parameters = len(sig.parameters)
	if num_of_parameters == 1:
		return apply_arguments(on_click, substring.lower())
	else:
		return on_click

def __parse_dsl_tag(
		substring: str,
		tag: str, 
		tag_arguments: str, 
		tag_info: dict[str], 
		on_click: Callable[[str], None] | Callable[[], None] | None
		) -> dict[str]:
	match tag:
		case 'c':
			if tag_arguments == '':
				tag_info["color"] = "Green"
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
			tag_info["on_click"] = __adapt_on_click_func(on_click, substring)
		case _:
			raise ValueError(f"Unknown tag: {tag}")
	return tag_info

def parse_dsl(string: str, on_click: Callable[[str], None] | Callable[[], None] | None = None) -> list[FormattedString]:
	"""Преобразовать строку формата DSL в `list[FormattedString]` с нужным форматированием

	:param string: Строка в формате словарной статьи в DSL
	:type string: str
	:param on_click: Функция, которая вызывается по нажатии на ref-ссылки. Можно назначить функцию с аргументом типа `str` (текст ref-ссылки)
	:type on_click: Callable[[str], None] | Callable[[], None] | None, optional
	:return: Форматтированная строка для использования в CTkPrettyTextbox
	:rtype: list[FormattedString]
	"""
	splitted_string = __split_dsl_to_tagged_list(string)
	list_of_formatted_strings: list[FormattedString] = []
	for substring, tags in splitted_string:
		tag_info = {
			"color": None,
			"formatting": Formatting.NONE,
			"on_click": None
		}
		for tag, tag_arguments in tags:
			tag_arguments = tag_arguments.lstrip()
			tag_info = __parse_dsl_tag(substring, tag, tag_arguments, tag_info, on_click)
		if "tabs" in tag_info:
			list_of_formatted_strings.append(FormattedString('\t' * tag_info["tabs"]))
		formatted_substring = FormattedString(
			substring, 
			color=tag_info["color"], 
			formatting=tag_info["formatting"], 
			on_click=tag_info["on_click"])
		list_of_formatted_strings.append(formatted_substring)
	return list_of_formatted_strings

def main():
	test_string = "\t[m1][b][c]АББРАЙ [/c][/b][i]прил[/i]. дождливый, дождлив; [b][ref]че̄ххч[/ref] ли аббрай[/b] осень \[дождлива\][/m]\n\t[m0][c red]•[/c][c green]•[/c][c yellow]•[/c][c blue]•[/c][/m]\n"
	print(parse_dsl(test_string, on_click=lambda text: print(f"REF-ссылка: <{text}>")))

if __name__ == "__main__":
	main()