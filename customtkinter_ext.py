import customtkinter
from enum import Flag, auto


class Formatting(Flag):
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


class InlineLinker:
	"""
	Настройка действий по нажатию на ссылки в CTkTextbox или CTkPrettyTextbox
	"""
	def __init__(self,
				 master,
				 text_color: str | tuple[str, str] = "dark blue",
				 formatting: Formatting = Formatting.UNDERLINE):
		self.text: customtkinter.CTkTextbox = master

		self.text.tag_config(
			"link", 
			foreground = text_color, 
			underline = 1 if Formatting.UNDERLINE in formatting else 0
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


class Formatter:
	"""
	Настройка цвета и форматирования текста в CTkTextbox или CTkPrettyTextbox
	"""
	forbidden_formatting = [Formatting.BOLD, Formatting.ITALIC]

	def __init__(self, master):
		self.text: customtkinter.CTkTextbox = master

		self.tag_list = ["bold", "italic", "underline", "overstrike"]
		# self.tag_list = ["underline", "overstrike"]
		# self.text.tag_config("bold", font=customtkinter.CTkFont(weight='bold'))
		# self.text.tag_config("italic", font=customtkinter.CTkFont(slant='italic'))
		self.text.tag_config("underline", underline=1)
		self.text.tag_config("overstrike", overstrike=1)
	
	def add(self, color: str | None = None, formatting: Formatting | None = None):
		tags = []
		if color:
			tag_name = f"color-{color}"
			tags.append(tag_name)
			if tag_name not in self.tag_list:
				self.text.tag_config(tag_name, foreground=color)
				self.tag_list.append(tag_name)
		if formatting:
			for formatting_option in formatting:
				if formatting_option in Formatter.forbidden_formatting:
					raise NotImplementedError(f"{str(formatting_option).capitalize()} formatting is not implemented yet.")
				tags.append(str(formatting_option))
		return tuple(tags)


class FormattedString:
	"""
	Форматированная строка для использования в `CTkPrettyTextbox`
	"""
	def __init__(self, text, color: str | None = None, formatting: Formatting | None = None, on_click: None = None):
		self.text = text
		self.color = color
		self.formatting = formatting
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
		self.linker = InlineLinker(self)
		self.formatter = Formatter(self)
		self._pretty_insert("end", new_text)
		self.configure(state = customtkinter.DISABLED)

	def _pretty_insert(self, index: str, text: list[FormattedString], tags: None = None):
		index = index.lower()
		for chars in text:
			self.insert(index, chars.text, (self.linker.add(chars.on_click) if chars.on_click else ()) + self.formatter.add(chars.color, chars.formatting) + (tags if tags else ()))
			if not index.endswith("end"):
				index += f" + {len(chars.text)} chars"

def main() -> None:
	def theme_switcher():
		mode = customtkinter.get_appearance_mode()
		match mode:
			case "Light": new_mode = "Dark"
			case "Dark": new_mode = "Light"
		customtkinter.set_appearance_mode(new_mode)

	app = customtkinter.CTk()
	app.title("customtkinter_ext — тест")
	app.geometry("500x500")
	app.rowconfigure(index=0, weight=1)
	app.columnconfigure(index=0, weight=1)

	pretty_textbox = CTkPrettyTextbox(app)
	pretty_textbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
	
	pretty_text = []
	pretty_text.append(FormattedString("Тестируем поле текста\n"))
	pretty_text.append(FormattedString("Этот текст должен быть синим\n", color="dark blue"))
	pretty_text.append(FormattedString(
		"Этот текст должен быть зелёным и подчёркнутым\n", 
		color="Dark green",
		formatting=Formatting.UNDERLINE))
	pretty_text.append(FormattedString("Этот текст должен переключать тему\n", on_click=theme_switcher))

	pretty_textbox.force_edit(pretty_text)

	app.mainloop()

if __name__ == "__main__":
	main()