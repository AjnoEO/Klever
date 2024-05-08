from enum import Flag, auto
from typing import Callable

class Formatting(Flag):
	NONE = 0
	BOLD = auto()
	ITALIC = auto()
	UNDERLINE = auto()
	OVERSTRIKE = auto()

	def __str__(self):
		match self:
			case Formatting.BOLD: return "bold"
			case Formatting.ITALIC: return "italic"
			case Formatting.UNDERLINE: return "underline"
			case Formatting.OVERSTRIKE: return "overstrike"
			
			
class FormattedString:
	"""
	Форматированная строка для использования в `CTkPrettyTextbox`
	"""
	def __init__(self, string: str, color: str | None = None, formatting: Formatting | None = None, on_click: Callable[[], None] | None = None):
		"""Форматированная строка для использования в `CTkPrettyTextbox`

		:param string: Строка текста
		:type string: str
		:param color: Цвет, None по умолчанию
		:type color: str | None, optional
		:param formatting: Форматирование, None по умолчанию
		:type formatting: Formatting | None, optional
		:param on_click: Функция, исполняемая по нажатию на ссылку (удобно для создания ref-ссылок), None по умолчанию
		:type on_click: Callable[[], None] | None, optional
		"""
		self.string = string
		self.color = color
		self.formatting = formatting
		self.on_click = on_click
	
	def __repr__(self):
		repr = f'FormattedString "{self.string}"'
		if self.color:
			repr += f', цвет: {self.color}'
		if self.formatting:
			repr += f', форматирование: {self.formatting}'
		if self.on_click:
			repr += f', с ref-ссылкой'
		return f"<{repr}>"