"""Основной файл, запускает приложение"""

import json
import customtkinter
import customtkinter_ext as cus_ext
from mix_ups_parser import possible_words_from_input_word
from utils import apply_arguments
from markup_parser import parse_dsl

with open("klever_dict.json", encoding="utf8") as f:
    dictionaries = json.load(f)

with open("info_about_dict.txt", encoding="utf8") as f:
    info_a = f.read()


class Letterpad(customtkinter.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.letters = ["ӓ", "ӭ", "һ", "ј", "ҋ", "ӆ", "ӎ", "ӊ", "ӈ", "ҏ", "ҍ", "¯̄"]

        for i, letter in enumerate(self.letters):
            self.letter_button = customtkinter.CTkButton(
                self,
                text=letter[0],
                command=apply_arguments(self.make_letter_button, letter[-1]),
                width=35,
                height=35
            )
            self.grid_columnconfigure(i, weight=1)
            self.letter_button.grid(row=0, column=i, padx=5, pady=5)

    def make_letter_button(self, letter):
        self.master.entry.insert(len(self.master.entry.get()), letter)


class SearchTools(customtkinter.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1), weight=0)

        self.entry = customtkinter.CTkEntry(self, placeholder_text="введите услышанное")
        self.entry.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=(0, 10))
        self.entry.bind("<KeyRelease-Return>", command=self.enter_pressed)

        self.win_info = None
        self.letterpad = None

        # кнопка поиска
        self.button_search = customtkinter.CTkButton(
            self, text="искать!", command=self.master.button_search_event
        )
        self.button_search.grid(row=0, column=1, sticky="ns", padx=(10, 10), pady=(0, 10))

        self.button_letterpad = customtkinter.CTkButton(
            self, text="букви!", command=self.call_letterpad
        )
        self.button_letterpad.grid(row=0, column=2, sticky="ns", padx=(10, 10), pady=(0, 10))

        # кнопка инфо
        self.button_info = customtkinter.CTkButton(self, text="о проекте")
        self.button_info.grid(
            row=0, column=3, sticky="nsew", padx=(10, 10), pady=(0, 10)
        )
        self.button_info.bind("<ButtonRelease>", command=self.info)

    def call_letterpad(self):
        if self.letterpad is None:
            self.letterpad = Letterpad(self)
            self.letterpad.grid(row=1, column=0, columnspan=4, sticky="w", padx=0, pady=(0, 0))
        else:
            self.letterpad.destroy()
            self.letterpad = None

    def what_enterred(self):
        return self.entry.get()

    def enter_pressed(self, _=None):
        self.master.button_search_event()

    def info(self, _=None):
        if self.win_info is None or not self.win_info.winfo_exists():
            self.win_info = WinAbout(self)
        self.win_info.after(10, self.win_info.focus)


class PossibleWords(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.variants: list[customtkinter.CTkButton] = []

        self.title = customtkinter.CTkLabel(self, text="возможные варианты:")
        self.title.grid(row=0, column=0, padx=10, pady=10, sticky="nesw")

    def populate(self, possible_word_list: list[str]):
        for word_button in self.variants:
            word_button.destroy()
        self.variants.clear()
        for i, word in enumerate(possible_word_list):
            word_button = customtkinter.CTkButton(
                self,
                text=word,
                fg_color="#E7ECEF",
                hover_color="#E7ECEF",
                border_width=0,
                command=apply_arguments(self.display_article, word),
            )
            word_button.grid(row=i + 1, column=0, padx=10, pady=10, sticky="nesw")
            self.grid_rowconfigure((i + 1), weight=0)
            self.variants.append(word_button)

    def display_article(self, word: str):
        textbox_contents = []
        for article in dictionaries[word]:
            textbox_contents += parse_dsl(article["contents"], self.display_article)
            textbox_contents += parse_dsl(article["source"], self.display_article)
            textbox_contents += [cus_ext.FormattedString("\n")]
        self.master.textbox.force_edit(textbox_contents)


class WinAbout(customtkinter.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)

        # параметры окна
        self.title("О словаре")
        self.geometry("700x505")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.minsize(700, 500)

        # информация о словаре
        self.info_about = cus_ext.CTkPrettyTextbox(self)
        self.info_about.grid(row=0, column=0, sticky="nesw", padx=20, pady=20)
        self.info_about.force_edit(parse_dsl(info_a))


class App(customtkinter.CTk):
    customtkinter.set_default_color_theme("style.json")

    def __init__(self):
        super().__init__()

        # параметры окна
        self.title("Klever")
        self.geometry("700x500")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.after(0, lambda: self.state("zoomed"))
        self.minsize(900, 500)

        # варианты
        self.possible_words = PossibleWords(self)
        self.possible_words.grid(
            row=0, column=0, sticky="nesw", rowspan=2, padx=(20, 10), pady=20
        )

        self.search_tools = SearchTools(self)
        self.search_tools.grid(row=0, column=1, sticky="nsew", padx=10, pady=(20, 10))
        self.search_tools.configure(fg_color="transparent", border_width=0)

        # вывод
        self.textbox = cus_ext.CTkPrettyTextbox(self)
        self.textbox.grid(
            row=1,
            column=1,
            columnspan=11,
            rowspan=2,
            sticky="nesw",
            padx=(10, 20),
            pady=(0, 20),
        )

        self.letterpad = None

    def button_search_event(self):
        self.textbox.force_edit(
            [
                cus_ext.FormattedString(
                    "Дорогой пользователь, не пугайтесь! Ничего не сломалось, мы ищем ваши слова и путаемся..."
                )
            ]
        )
        self.after(10, self.find)

    def find(self, _=None):
        res = possible_words_from_input_word(self.search_tools.what_enterred().lower())
        self.possible_words.populate(res)
        if res:
            self.possible_words.display_article(res[0])
        else:
            self.textbox.force_edit(
                [
                    cus_ext.FormattedString(
                        f"\"{self.search_tools.what_enterred().lower()}\" очень старалось, но в словарях не нашлось :("
                    )
                ]
            )


app = App()
app.mainloop()
