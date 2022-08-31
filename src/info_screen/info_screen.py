import tkinter as tk
import tkinter.font as tkFont
import time
import os
import configparser
from turtle import width

class App(tk.Tk):
    def __init__(self, font_size):
        super().__init__()

        self.title('Informasjon om kraftnettet')
        self.geometry('1500x300')

        self.frame = tk.Frame(self, bg='black')
        self.frame.pack(fill=tk.BOTH, expand=1)

        self.countdown_time = tk.StringVar()
        self.energy_cost = tk.StringVar()

        self.display_font = tkFont.Font(family='Courier New', size=font_size)
        self.time_label = tk.Label( self.frame,
                                    textvariable=self.countdown_time,
                                    font=self.display_font,
                                    fg='red',
                                    bg='black')

        self.cost_label = tk.Label( self.frame,
                                    textvariable=self.energy_cost,
                                    font=self.display_font,
                                    fg='red',
                                    bg='black')

        self.joker_canvas = tk.Canvas(self.frame, width=100, height=100, bg='black')
        #self.joker_canvas.pack()
        self.joker_picture = tk.PhotoImage(file="src/info_screen/img/joker_symbol.png")
        self.joker_canvas.create_image(20, 20, anchor=tk.NW, image=self.joker_picture)

        #self.approaching_label = tk.Label(self.frame, text='No nærmar da seg!!!')

        self.time_label.grid(row=0, column=0, padx=20, pady=20)
        self.cost_label.grid(row=1, column=0, padx=5, pady=5)
        self.joker_canvas.grid(row=0, column=1)
        #self.approaching_label.pack()

        self.frame.rowconfigure(0, weight=10)
        self.frame.rowconfigure(1, weight=10)
        self.frame.columnconfigure(0, weight=1)

        self.bind('<Configure>', self.resize)

        self.after(20, self.update)

    def update(self) -> None:
        local_time = time.localtime()

        self.countdown_time.set(f"{local_time.tm_hour:02d}:{local_time.tm_min:02d}:{local_time.tm_sec:02d}")

        self.energy_cost.set("396,34 EUR/MWh")

        self.after(500, self.update)

    def resize(self, event=None) -> None:
        new_size = -max(12, int((self.frame.winfo_width() / 10)))
        self.display_font.configure(size=new_size)
        #new_size = -max(12, int((self.frame.winfo_height() / 30)))


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('infoscreen.ini')
    font_size = config['DISPLAY']['FontSize']
    #print("Verdi: ", str(config['DISPLAY']['FontSize']))
    #print(os.getcwd())
    app = App(font_size)
    app.mainloop()
