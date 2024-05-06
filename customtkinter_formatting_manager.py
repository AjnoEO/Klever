import customtkinter
from enum import Flag, auto

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
	def __init__(self, string, color: str | None = None, formatting: Formatting | None = None, on_click: None = None):
		self.string = string
		self.color = color
		self.formatting = formatting
		self.on_click = on_click
	
	def __repr__(self):
		repr = f'FormattedString "{self.string}"'
		if self.color:
			repr += f', color: {self.color}'
		if self.formatting:
			repr += f', formatting: {self.formatting}'
		return f"<{repr}>"