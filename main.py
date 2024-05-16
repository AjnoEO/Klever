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

class Letterpad(customtkinter.CTk):

    def __init__(self):
        super().__init__()

        ## параметры окна
        self.title("letterpad")
        self.geometry("220x170")
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        ##self.after(0, lambda: self.state("zoomed"))
        ##self.minsize(900, 500)

        ## ӓ ӭ һ ј ҋ ӆ ӎ ӊ ӈ ҏ ҍ
        self.dotted_a = customtkinter.CTkButton(
            self, text="ӓ", command=self.button_dotted_a
        )
        self.dotted_a.grid(row=0, column=0, sticky="nsew", padx=(20, 10), pady=(20, 10))

        self.dotted_e = customtkinter.CTkButton(
            self, text="ӭ", command=self.button_dotted_e
        )
        self.dotted_e.grid(row=0, column=1, sticky="nsew", padx=10, pady=(20, 10))

        self.h = customtkinter.CTkButton(
            self, text="һ", command=self.button_h
        )
        self.h.grid(row=0, column=2, sticky="nsew", padx=10, pady=(20, 10))

        self.j = customtkinter.CTkButton(
            self, text="ј", command=self.button_j
        )
        self.j.grid(row=0, column=3, sticky="nsew", padx=(10, 20), pady=(20, 10))

        self.cyrillic_j = customtkinter.CTkButton(
            self, text="ҋ", command=self.button_cyrillic_j
        )
        self.cyrillic_j.grid(row=1, column=0, sticky="nsew", padx=(20, 10), pady=10)

        self.deaf_l = customtkinter.CTkButton(
            self, text="ӆ", command=self.button_deaf_l
        )
        self.deaf_l.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        self.deaf_m = customtkinter.CTkButton(
            self, text="ӎ", command=self.button_deaf_m
        )
        self.deaf_m.grid(row=1, column=2, sticky="nsew", padx=10, pady=10)

        self.deaf_n = customtkinter.CTkButton(
            self, text="ӊ", command=self.button_deaf_n
        )
        self.deaf_n.grid(row=1, column=3, sticky="nsew", padx=(10, 20), pady=10)

        self.n_with_tail = customtkinter.CTkButton(
            self, text="ӈ", command=self.button_n_with_tail
        )
        self.n_with_tail.grid(row=2, column=0, sticky="nsew", padx=(20, 10), pady=(10, 20))

        self.deaf_r = customtkinter.CTkButton(
            self, text="ҏ", command=self.button_deaf_r
        )
        self.deaf_r.grid(row=2, column=1, sticky="nsew", padx=10, pady=(10, 20))

        self.semi_soft_sign = customtkinter.CTkButton(
            self, text="ҍ", command=self.button_semi_soft_sign
        )
        self.semi_soft_sign.grid(row=2, column=2, sticky="nsew", padx=10, pady=(10, 20))

    def button_dotted_a(self):
        print("ӓ", end="")

    def button_dotted_e(self):
        print("ӭ",  end="")

    def button_h(self):
        print("һ",  end="")

    def button_j(self):
        print("ј",  end="")

    def button_cyrillic_j(self):
        print("ҋ", end="")

    def button_deaf_l(self):
        print("ӆ", end="")

    def button_deaf_m(self):
        print("ӎ", end="")

    def button_deaf_n(self):
        print("ӊ", end="")

    def button_n_with_tail(self):
        print("ӈ", end="")

    def button_deaf_r(self):
        print("ҏ", end="")

    def button_semi_soft_sign(self):
        print("ҍ", end="")
class Search_tools(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.entry = customtkinter.CTkEntry(self, placeholder_text="введите услышанное")
        self.entry.grid(row=0, column=1, sticky="nsew", padx=10, pady=(20, 10))
        self.entry.bind("<KeyRelease-Return>", command = self.enter_pressed)
        ##command = self.enter_pressed

        ## кнопка поиска
        self.button_search = customtkinter.CTkButton(
            self, text="искать!", command = self.master.button_search_event
        )
        self.button_search.grid(row=0, column=2, sticky="nsew", padx=10, pady=(20, 10))
        ##command = self.button_search_event


    def what_enterred(self):
        return self.entry.get()
    def enter_pressed(self, _=None):
        self.master.button_search_event()


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
        ##print(word)


class WinAbout(customtkinter.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)

        ## параметры окна
        self.title("О словаре")
        self.geometry("700x505")
        self.grid_columnconfigure((0), weight=1)
        self.grid_rowconfigure((0), weight=1)
        self.minsize(700, 500)

        ##информация о словаре
        self.info_about = cus_ext.CTkPrettyTextbox(self)
        self.info_about.grid(row=0, column=0, sticky="nesw", padx=20, pady=20)
        self.info_about.force_edit(parse_dsl(info_a))


class App(customtkinter.CTk):
    customtkinter.set_default_color_theme("style.json")

    def __init__(self):
        super().__init__()

        ## параметры окна
        self.title("Klever")
        self.geometry("700x500")
        self.grid_columnconfigure((1), weight=1)
        self.grid_rowconfigure((1), weight=1)
        self.after(0, lambda: self.state("zoomed"))
        self.minsize(900, 500)

        ## варианты
        self.possible_words = PossibleWords(self)
        self.possible_words.grid(
            row=0, column=0, sticky="nesw", rowspan=2, padx=(20, 10), pady=20
        )

        self.search_tools = Search_tools(self)
        self.search_tools.grid(row=0, column=1, sticky="nsew", padx=10, pady=(20, 10))

        ## строка поиска
        ##self.entry.bind("<KeyPress-Return>", command=self.info_waite)

        ##self.button_search.bind("<Button>", command=self.info_waite)

        ## кнопка инфо
        self.button_info = customtkinter.CTkButton(self, text="о проекте")
        self.button_info.grid(
            row=0, column=3, sticky="nsew", padx=(10, 20), pady=(20, 10)
        )
        self.button_info.bind("<ButtonRelease>", command=self.info)

        ##вывод
        self.textbox = cus_ext.CTkPrettyTextbox(self)
        self.textbox.grid(
            row=1,
            column=1,
            columnspan=11,
            rowspan=2,
            sticky="nesw",
            padx=(10, 20),
            pady=(10, 20),
        )

        self.win_info = None
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

    def info(self, _=None):
        if self.win_info is None or not self.win_info.winfo_exists():
            self.win_info = WinAbout(self)
        self.win_info.after(10, self.win_info.focus)

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
