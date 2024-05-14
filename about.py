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

class App(customtkinter.CTk):
    customtkinter.set_default_color_theme("style.json")

    words = []
    def __init__(self):
        super().__init__()

        ## параметры окна
        self.title("Klever")
        self.geometry("700x500")
        self.grid_columnconfigure((0), weight=1)
        self.grid_rowconfigure((0), weight=1)
        #self.after(0, lambda: self.state('zoomed'))

        ##вывод
        self.textbox = cus_ext.CTkPrettyTextbox(self)
        self.textbox.grid(row=0, column=0, sticky="nesw", padx=20, pady=20)

        self.button_search = customtkinter.CTkButton(self, text="искать!", command=self.about_all)
        self.button_search.grid(row=0, column=2, sticky="nsew", padx=(10, 20), pady=(20, 10))

    def about_all(self):
        self.textbox.force_edit([cus_ext.FormattedString("Скорее всего вы Вика и ищете несуществующее слово")])



app = App()
app.mainloop()