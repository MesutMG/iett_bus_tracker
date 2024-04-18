import tkinter
import customtkinter
import busline
import webbrowser

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("720x480")
app.title("Yo")

busline_text = customtkinter.CTkLabel(app, text="Bus Line", fg_color="transparent")
busline_text.pack(padx=10, pady=10)

busline_input = customtkinter.CTkEntry(app, width=50, height=15)
busline_input.pack()

busway_text = customtkinter.CTkLabel(app, text="Way", fg_color="transparent")
busway_text.pack(padx=10, pady=10)

busway_input = customtkinter.CTkEntry(app, width=23, height=15)
busway_input.pack()


def okfunc():
    print(busline.announcements(busline_input.get()))
    busline.live_tracking(busline_input.get(),busway_input.get())
    webbrowser.open('index.html')


button = customtkinter.CTkButton(app, text="OK", command=okfunc)
button.pack(padx=10, pady=10)

app.mainloop()
