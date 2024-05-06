import customtkinter
import customtkinter_ext as cus_ext
import json
##fg_color="#E0FFFF", hover_color="#AFEEEE", text_color="black"
class MyCheckboxFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.checkbox_1 = customtkinter.CTkCheckBox(self, text="поспать")
        self.checkbox_1.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.checkbox_2 = customtkinter.CTkCheckBox(self, text="поботать")
        self.checkbox_2.grid(row=1, column=0, padx=10, pady=10, sticky="w")


    def get(self):
        checked_checkboxes = []
        if self.checkbox_1.get() == 1:
            checked_checkboxes.append(self.checkbox_1.cget("text"))
        if self.checkbox_2.get() == 1:
            checked_checkboxes.append(self.checkbox_2.cget("text"))
        return checked_checkboxes

class sel_dict(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        ##self.minsize("100x100")
        self.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11), weight=1)
        self.grid_rowconfigure((1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11), weight=1)
        ##self.state('zoomed')

        self.checkbox_frame = MyCheckboxFrame(self)
        self.checkbox_frame.grid(row=0, column=0, sticky="nsw")

class App(customtkinter.CTk):
    customtkinter.set_default_color_theme("style.json")
    def __init__(self):
        super().__init__()


        ##customtkinter.set_widget_scaling(100)

        self.title("жоско умный словарь")
        self.geometry("700x500")
        ##self.minsize("100x100")
        self.grid_columnconfigure((2, 3, 4, 5, 8, 9, 10, 11), weight=1)
        self.grid_rowconfigure((3, 4, 5, 6, 7, 8, 9, 10, 11), weight=1)
        ##self.state('zoomed')
        self.after(0, lambda: self.state('zoomed'))


        ##self.button = customtkinter.CTkButton(self, text="подтвердить выбор", command=self.button_callback())
        ##self.button.grid(row=2, column=3, padx=0, pady=0)

        self.sel_dict = sel_dict(self)
        self.sel_dict.grid(row=0, column=0, columnspan=6, sticky="nsew", padx=10, pady=10)



        ##первый текстбокс
        ##self.textbox = cus_ext.CTkPrettyTextbox(self)
        ##self.textbox.grid(row=0, column=0, columnspan=6, sticky="nesw", padx=10, pady=10)
        ##textbox_contents = [cus_ext.FormattedString("Тут типа будут какие-нибудь словари и параметры к ним")]
        ##self.textbox.force_edit(textbox_contents)

        ##второй текстбокс
        self.textbox = cus_ext.CTkPrettyTextbox(self)
        self.textbox.grid(row=0, column=6, columnspan=6, sticky="nesw", padx=10, pady=10)
        textbox_contents = [cus_ext.FormattedString("Тут будет что-то про путанницы ")]
        self.textbox.force_edit(textbox_contents)

        ##третий текстбокс
        self.textbox = cus_ext.CTkPrettyTextbox(self)
        self.textbox.grid(row=1, column=0, rowspan=11, sticky="nesw", padx=10, pady=10)
        textbox_contents = [cus_ext.FormattedString("Тут будут появляться похожие слова")]
        self.textbox.force_edit(textbox_contents)

        ##четвёртый текстбокс
        self.textbox = cus_ext.CTkPrettyTextbox(self)
        self.textbox.grid(row=1, column=1, columnspan=6, sticky="nesw", padx=10, pady=10)
        textbox_contents = [cus_ext.FormattedString("Тут будет поисковая строка")]
        self.textbox.force_edit(textbox_contents)

        ##пятый текстбокс
        self.textbox = cus_ext.CTkPrettyTextbox(self)
        self.textbox.grid(row=1, column=7, columnspan=5, sticky="nesw", padx=10, pady=10)
        textbox_contents = [cus_ext.FormattedString("Тут будут параметры поиска видимо")]
        self.textbox.force_edit(textbox_contents)

        ##шестой текстбокс
        self.textbox = cus_ext.CTkPrettyTextbox(self)
        self.textbox.grid(row=2, column=1, columnspan=11, rowspan=10, sticky="nesw", padx=10, pady=10)
        textbox_contents = [cus_ext.FormattedString("Сюда хочу запихать основные подходящие статьи")]
        self.textbox.force_edit(textbox_contents)

        ##def combobox_callback(choice):
            ##print("combobox dropdown clicked:", choice)

        ##self.combobox = customtkinter.CTkComboBox(self, values=["option 1", "option 2"],
                                             ##command=combobox_callback)
        ##self.combobox.set("option 2")

        ##self.frame = customtkinter.CTkFrame(self, width=20, height=7)

        ##self.progressbar = customtkinter.CTkProgressBar(self, orientation="horizontal")

    ##def button_callback(self):
        ##print("чё-то происходит!")
        ##print("checked checkboxes:", self.checkbox_frame.get())


app = App()
app.mainloop()