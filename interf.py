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
        self.checkbox_2.grid(row=0, column=1, padx=10, pady=10, sticky="w")


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
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((0, 1, 2,), weight=1)
        ##self.state('zoomed')

        self.textbox = cus_ext.CTkPrettyTextbox(self)
        self.textbox.grid(row=0, column=0, columnspan=3, sticky="nesw", padx=10, pady=10)
        textbox_contents = [cus_ext.FormattedString("Всё что внутри фиолетового -- нерабочая шняга")]
        self.textbox.force_edit(textbox_contents)

        self.checkbox_frame = MyCheckboxFrame(self)
        self.checkbox_frame.grid(row=1, column=0, columnspan=3, sticky="nsw")

        self.button1 = customtkinter.CTkButton(self, text="сбросить всё", command=self.button_event1)
        self.button1.grid(row=2, column=0, sticky="nesw", padx=10, pady=10)

        self.button2 = customtkinter.CTkButton(self, text="какая-то ещё полезная кнопка, какая -- забыл", command=self.button_event2)
        self.button2.grid(row=2, column=1, sticky="nesw", padx=10, pady=10)
    def button_event2(self):
        print("пользователь чё-то нажал")
    def button_event1(self):
        checked_checkboxes = []




        ##def radiobutton_event():
            ##print("radiobutton toggled, current value:", radio_var.get())

        ##self.radio_var = tkinter.IntVar(value=0)
        ##radiobutton_1 = customtkinter.CTkRadioButton(App, text="CTkRadioButton 1", command=radiobutton_event, variable=radio_var, value=1)
        ##radiobutton_2 = customtkinter.CTkRadioButton(App, text="CTkRadioButton 2", command=radiobutton_event, variable=radio_var, value=2)

class App(customtkinter.CTk):
    customtkinter.set_default_color_theme("style.json")
    def __init__(self):
        super().__init__()


        ##customtkinter.set_widget_scaling(100)

        self.title("жоско умный словарь")
        self.geometry("700x500")
        ##self.minsize("100x100")
        self.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11), weight=1)
        ##self.state('zoomed')
        self.after(0, lambda: self.state('zoomed'))


        ##self.button = customtkinter.CTkButton(self, text="подтвердить выбор", command=self.button_callback())
        ##self.button.grid(row=2, column=3, padx=0, pady=0)

        self.sel_dict = sel_dict(self)
        self.sel_dict.grid(row=0, column=0, columnspan=6, sticky="nsew", padx=10, pady=10)
        ##self.sel_dict.configure(maxheight=200)



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
        ##self.textbox = cus_ext.CTkPrettyTextbox(self)
        ##self.textbox.grid(row=1, column=1, columnspan=6, sticky="nesw", padx=10, pady=10)
        ##textbox_contents = [cus_ext.FormattedString("Тут будет поисковая строка")]
        ##self.textbox.force_edit(textbox_contents)
        ##tk_textbox = customtkinter.CTkTextbox(self, activate_scrollbars=False)
        ##tk_textbox.grid(row=1, column=1, sticky="nsew", columnspan=6, padx=10, pady=10)

        self.entry = customtkinter.CTkEntry(self, placeholder_text="что поищем в этот раз?")
        self.entry.grid(row=1, column=1, sticky="nsew", columnspan=6, padx=(10, 200), pady=(10, 200))

        self.button_search = customtkinter.CTkButton(self, text="Искать!", command=self.button_search_event)
        self.button_search.grid(row=1, column=1, sticky="nsew", columnspan=6, padx=(200, 10), pady=(200, 10))

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

    def button_search_event(self):
        print(self.entry.get())
    ##def button_callback(self):
        ##print("чё-то происходит!")
        ##print("checked checkboxes:", self.checkbox_frame.get())


app = App()
app.mainloop()