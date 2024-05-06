def resize_canvas(event):
    new_width = event.width
    new_height = event.height
    b.config(width=new_width, height=new_height)
    b.itemconfigure(item, image=photob) # Update the image size (optional)

    root = Tk()
    root.title('Érzékek kertje')
    root.attributes('-fullscreen', True)
    b = Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight(), bg='grey', bd=2, relief=SOLID, scrollregion=(0, 0, 0, 0))
    photob = PhotoImage(file='alap.gif')
    item = b.create_image(590, 330, image=photob, tags='ed')
    b.grid(row=1, column=1, rowspan=6, padx=0, pady=0)

    # Bind the canvas to the resizing event of the main window
root.bind('<Configure>', resize_canvas)
    root.mainloop()