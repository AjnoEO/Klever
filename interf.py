import customtkinter
import customtkinter_ext as cus_ext
from mix_ups_parser import possible_words_from_input_word

class impossible_words(customtkinter.CTkFrame):
    def __init__(self, master, title="Klever", values=[]):
        super().__init__(master)
        self.grid_columnconfigure((0), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), weight=1)
        self.values = values
        self.title = title
        self.variants = []

        self.title = customtkinter.CTkLabel(self, text="возможные варианты:")
        self.title.grid(row=0, column=0, padx=10, pady=10, sticky="nesw")

    ##def populate(self):
        self.values = App.button_search_event(self)
        for i, value in enumerate(self.values):
            self.word = customtkinter.CTkButton(self, text=value)
            self.word.grid(row=i + 1, column=0, padx=10, pady=10, sticky="nesw")
            self.variants.append(self.word)
            print("самсинг из хеппенинг")


class App(customtkinter.CTk):
    customtkinter.set_default_color_theme("style.json")

    words = []
    def __init__(self):
        super().__init__()

        ## параметры окна
        self.title("Klever")
        self.geometry("700x500")
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.after(0, lambda: self.state('zoomed'))

        ## варианты
        self.possible_words = impossible_words(self)
        self.possible_words.grid(row=1, column=0, sticky="nesw", rowspan=2, padx=10, pady=10)

        ## строка поиска
        self.text_var = customtkinter.StringVar(value="")

        self.entry = customtkinter.CTkEntry(self, placeholder_text="что поищем в этот раз?")
        self.entry.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        ## поисковые параметры
        self.button_search = customtkinter.CTkButton(self, text="искать!", command=self.button_search_event)
        self.button_search.grid(row=1, column=2, sticky="nsew", padx=10, pady=10)

        ##вывод
        self.textbox = cus_ext.CTkPrettyTextbox(self)
        self.textbox.grid(row=2, column=1, columnspan=11, rowspan=2, sticky="nesw", padx=10, pady=10)
        ##self.textbox.configure(text = self.entry.get())

    def button_search_event(self):
        self.res = possible_words_from_input_word(self.entry.get())
        print(self.res)
        return self.res
        ##textbox_contents = [cus_ext.FormattedString(str(possible_words_from_input_word(self.entry.get())))]
        ##self.textbox.insert("0.0", self.textbox.force_edit(textbox_contents))
        ##textbox_contents = [cus_ext.FormattedString(self.entry.get())]
        ##self.textbox.configure(text=textbox_contents)


app = App()
app.mainloop()