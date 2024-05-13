from convert_dict import convert

list_of_dictionaries = ["dictionaries/sa-ru-antonova.dsl", "dictionaries/sa-ru-kert.dsl", "dictionaries/sa-ru-kuruch.dsl"]
convert(list_of_dictionaries)

import customtkinter
import customtkinter_ext as cus_ext
from mix_ups_parser import possible_words_from_input_word
from utils import apply_arguments
import json
from markup_parser import parse_dsl

with open("klever_dict.json", encoding="utf8") as f:
    dictionaries = json.load(f)


class Possible_words(customtkinter.CTkFrame):
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
            word_button = customtkinter.CTkButton(self, text=word, fg_color="#E7ECEF", hover_color="#E7ECEF", border_width=0, command=apply_arguments(self.display_article, word))
            word_button.grid(row=i+1, column=0, padx=10, pady=10, sticky="nesw")
            self.grid_rowconfigure((i+1), weight=0)
            self.variants.append(word_button)

    def display_article(self, word: str):
        textbox_contents = []
        for article in dictionaries[word]:
            textbox_contents += parse_dsl(article["contents"], self.display_article)
            textbox_contents += parse_dsl(article["source"], self.display_article)
            textbox_contents += [cus_ext.FormattedString("\n")]
        self.master.textbox.force_edit(textbox_contents)
        print(word)


class App(customtkinter.CTk):
    customtkinter.set_default_color_theme("style.json")

    words = []
    def __init__(self):
        super().__init__()

        ## параметры окна
        self.title("Klever")
        self.geometry("700x500")
        self.grid_columnconfigure((1), weight=1)
        self.grid_rowconfigure((1), weight=1)
        self.after(0, lambda: self.state('zoomed'))

        ## варианты
        self.possible_words = Possible_words(self)
        self.possible_words.grid(row=0, column=0, sticky="nesw", rowspan=2, padx=(20, 10), pady=20)

        ## строка поиска
        self.text_var = customtkinter.StringVar(value="")

        self.entry = customtkinter.CTkEntry(self, placeholder_text="что поищем в этот раз?")
        self.entry.grid(row=0, column=1, sticky="nsew", padx=10, pady=(20, 10))
        self.entry.bind("<KeyPress-Return>", command=self.enter_pressed)

        ## поисковые параметры
        self.button_search = customtkinter.CTkButton(self, text="искать!", command=self.button_search_event)
        self.button_search.grid(row=0, column=2, sticky="nsew", padx=(10, 20), pady=(20, 10))

        ##вывод
        self.textbox = cus_ext.CTkPrettyTextbox(self)
        self.textbox.grid(row=1, column=1, columnspan=11, rowspan=2, sticky="nesw", padx=(10, 20), pady=(10, 20))

    def button_search_event(self):
        self.res = possible_words_from_input_word(self.entry.get().lower())
        self.possible_words.populate(self.res)
        if self.res != []:
            self.possible_words.display_article(self.res[0])
        else:
            self.textbox.force_edit([])

    def enter_pressed(self, event):
        self.button_search_event()

app = App()
app.mainloop()