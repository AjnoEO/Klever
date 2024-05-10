import customtkinter
import customtkinter_ext as cus_ext
from mix_ups_parser import possible_words_from_input_word

class App(customtkinter.CTk):
    customtkinter.set_default_color_theme("style.json")

    words = []
    def __init__(self):
        super().__init__()

        self.title("жоско умный словарь")
        self.geometry("700x500")
        self.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11), weight=1)
        self.after(0, lambda: self.state('zoomed'))

        self.text_var = customtkinter.StringVar(value="")

        self.entry = customtkinter.CTkEntry(self, placeholder_text="что поищем в этот раз?")
        self.entry.grid(row=1, column=1, sticky="nsew", columnspan=6, padx=10, pady=10)

        self.button_search = customtkinter.CTkButton(self, text="Искать!", command=self.button_search_event)
        self.button_search.grid(row=1, column=7, sticky="nsew", columnspan=6, padx=10, pady=10)

        ##шестой текстбокс
        self.textbox = customtkinter.CTkTextbox(self)
        self.textbox.grid(row=2, column=1, columnspan=11, rowspan=10, sticky="nesw", padx=10, pady=10)
        ##self.textbox.configure(text = self.entry.get())

    def button_search_event(self):
        textbox_contents = [cus_ext.FormattedString(possible_words_from_input_word(self.entry.get()))]
        self.textbox.insert("0.0", self.textbox.force_edit(textbox_contents))
        ##textbox_contents = [cus_ext.FormattedString(self.entry.get())]
        ##self.textbox.configure(text=textbox_contents)


app = App()
app.mainloop()