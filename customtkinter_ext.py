import customtkinter
from customtkinter_formatting_manager import Formatting, FormattedString
from markup_parser import parse_dsl


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
		self.text.tag_config("bold", font=customtkinter.CTkFont(weight='bold'))
		#self.text.tag_config("bold", font=(customtkinter.ThemeManager.theme["CTkFont"]["family"], customtkinter.ThemeManager.theme["CTkFont"]["size"], "bold"))
		self.text.tag_config("italic", font=customtkinter.CTkFont(slant='italic'))
		#self.text.tag_config("italic", font=(customtkinter.ThemeManager.theme["CTkFont"]["family"], customtkinter.ThemeManager.theme["CTkFont"]["size"], "italic"))
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
				#if formatting_option in Formatter.forbidden_formatting:
				#	raise NotImplementedError(f"{str(formatting_option).capitalize()} formatting is not implemented yet.")
				tags.append(str(formatting_option))
		return tuple(tags)


class CTkPrettyTextbox(customtkinter.CTkTextbox):
	"""
	Textbox с более простой настройкой текста и с ссылками с настраиваемыми действиями
	"""
	def __init__(self, master: any, **kwargs):
		super().__init__(master, **kwargs)
		self.configure(state=customtkinter.DISABLED)
	
	def tag_config(self, tagName, **kwargs):
		#if "font" in kwargs:
		#	raise AttributeError("'font' option forbidden, because would be incompatible with scaling")
		if "font" in kwargs:
			font = kwargs["font"]
			if isinstance(font, customtkinter.CTkFont):
				font = self._apply_font_scaling(font)
		return self._textbox.tag_config(tagName, **kwargs)

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
			self.insert(index, chars.string, (self.linker.add(chars.on_click) if chars.on_click else ()) + self.formatter.add(chars.color, chars.formatting) + (tags if tags else ()))
			if not index.endswith("end"):
				index += f" + {len(chars.string)} chars"

def __main() -> None:
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
	
	test_string = "\t[m1][b][c]АББРАЙ [/c][/b][i]прил[/i]. дождливый, дождлив; [b]че̄ххч ли аббрай[/b] осень дождлива[/m]\n\t[m0][c red]•[/c][c green]•[/c][c yellow]•[/c][c blue]•[/c][/m]\n"

	pretty_text = parse_dsl(test_string)
	#pretty_text.append(FormattedString("Тестируем поле текста\n"))
	#pretty_text.append(FormattedString("Этот текст должен быть синим\n", color="dark blue"))
	#pretty_text.append(FormattedString(
	#	"Этот текст должен быть зелёным и подчёркнутым\n", 
	#	color="Dark green",
	#	formatting=Formatting.UNDERLINE))
	#pretty_text.append(FormattedString("Этот текст должен переключать тему\n", on_click=theme_switcher))

	pretty_textbox.force_edit(pretty_text)

	app.mainloop()

if __name__ == "__main__":
	__main()