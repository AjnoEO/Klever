from customtkinter_formatting_manager import Formatting, FormattedString
from typing import Callable
import re
import inspect

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
	parsed_suffix = __split_dsl_to_tagged_list(suffix, lstrip=False)
	list_of_tagged_strings = (parsed_prefix if prefix != "" else []) \
		+ parsed_internal \
		+ (parsed_suffix if suffix != "" else [])
	return list_of_tagged_strings

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
	list_of_formatted_strings = []
	for substring, tags in splitted_string:
		color = None
		formatting = Formatting.NONE
		on_click_action = None
		for tag, tag_arguments in tags:
			tag_arguments = tag_arguments.lstrip()
			match tag:
				case 'c':
					if tag_arguments == '':
						color = "Green"
					else:
						color = tag_arguments
				case 'm':
					if not tag_arguments.isnumeric():
						raise ValueError(f"Invalid tag: {tag, tag_arguments}")
					list_of_formatted_strings.append(FormattedString('\t' * int(tag_arguments)))
				case 'u':
					formatting |= Formatting.UNDERLINE
				case 'b':
					formatting |= Formatting.BOLD
				case 'i':
					formatting |= Formatting.ITALIC
				case 'ref':
					if on_click:
						sig = inspect.signature(on_click)
						num_of_parameters = len(sig.parameters)
						if num_of_parameters == 1:
							def on_click_action():
								on_click(substring)
						else:
							on_click_action = on_click
				case _:
					raise ValueError(f"Unknown tag: {tag}")
		formatted_substring = FormattedString(substring, color=color, formatting=formatting, on_click=on_click_action)
		list_of_formatted_strings.append(formatted_substring)
	return list_of_formatted_strings

def main():
	test_string = "\t[m1][b][c]АББРАЙ [/c][/b][i]прил[/i]. дождливый, дождлив; [b][ref]че̄ххч[/ref] ли аббрай[/b] осень дождлива[/m]\n\t[m0][c red]•[/c][c green]•[/c][c yellow]•[/c][c blue]•[/c][/m]\n"
	print(parse_dsl(test_string, on_click=lambda text: print(f"REF-ссылка: <{text}>")))

if __name__ == "__main__":
	main()