import customtkinter

class InlineLinker:
	"""
	Настройка действий по нажатию на ссылки в CTkTextbox
	"""
	def __init__(self,
				 master,
				 text_color: str | tuple[str, str] = ("dark blue", "blue"),
				 bold: bool = False,
				 italic: bool = False,
				 underline: bool = True):
		self.text: customtkinter.CTkTextbox = master

		self.text.tag_config(
			"link", 
			foreground=text_color, 
			underline=underline
		)
		self.text.tag_bind("link", "<Enter>", self._enter)
		self.text.tag_bind("link", "<Leave>", self._leave)
		self.text.tag_bind("link", "<Button-1>", self._click)

		self.click_events = {}

	def add(self, on_click):
		"""
		Создаёт и имплементирует тэг для ссылки с выполнением функции `on_click` при нажатии
		"""
		tag = f"link-{len(self.click_events)}"
		self.click_events[tag] = on_click
		return "link", tag

	def _enter(self, event):
		self.text.configure(cursor="hand2")

	def _leave(self, event):
		self.text.configure(cursor="xterm")

	def _click(self, event):
		for tag in self.text.tag_names(customtkinter.CURRENT):
			if tag.startswith("link-"):
				self.click_events[tag]()
				return

class FormattedString:
	"""
	Форматированная строка для использования в `CTkPrettyTextbox`
	"""
	def __init__(self, text, color = None, bold: bool = False, italic: bool = False, underline: bool = False, on_click: None = None):
		self.text = text
		self.color = color
		self.bold = bold
		self.italic = italic
		self.underline = underline
		self.on_click = on_click

class CTkPrettyTextbox(customtkinter.CTkTextbox):
	"""
	Textbox с более простой настройкой текста и с ссылками с настраиваемыми действиями
	"""
	def __init__(self, master: any, **kwargs):
		super().__init__(master, **kwargs)
		self.configure(state=customtkinter.DISABLED)

	def force_edit(self, new_text: list[FormattedString]):
		"""
		Заменить весь текст на `new_text`
		"""
		self.configure(state = customtkinter.NORMAL)
		self.delete("0.0", "end")
		self._pretty_insert("end", new_text)
		self.configure(state = customtkinter.DISABLED)

	def _pretty_insert(self, index: str, text: list[FormattedString], tags: None = None):
		linker = InlineLinker(self)
		index = index.lower()
		for chars in text:
			self.insert(index, chars.text, linker.add(chars.on_click) if chars.on_click else None)
			if not index.endswith("end"):
				index += f" + {len(chars.text)} chars"