#!/usr/bin/python
# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.font as tkFont
import time
from datetime import datetime, timedelta
import os
import configparser

import energy_cost

#from turtle import width

##from dataclasses import dataclass
##
##@dataclass
##class :
##    x: float
##    y: float
##    z: float = 0.0


config_file = "infoscreen.ini"

class App(tk.Tk):
    def __init__(self, config):
        super().__init__()

        self.font_size = config['DISPLAY']['FontSize']
        self.enable_count_down_timer = config['DISPLAY']['CountDownTimer']

        self.prev_price_nok_kwh = 0

        exchange_rate = 9.96
        self.cost = energy_cost.EnergyCost(exchange_rate)

        #print("Pris: ", self.cost.GetCurrentCost())

        self.title('Informasjon om kraftnettet')
        self.geometry('1600x300')

        self.frame = tk.Frame(self, bg='black')
        self.frame.pack(fill=tk.BOTH, expand=1)

        self.countdown_time = tk.StringVar()
        self.energy_cost = tk.StringVar()

        self.display_font = tkFont.Font(family='Courier New', size=self.font_size)
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

        self.after(20, self.update_price)
        self.after(20, self.update)

    def update_price(self) -> None:
        # Store the previous price if it has changed
        #if(self.price_nok_kwh != self.prev_price_nok_kwh):
        #    self.prev_price_nok_kwh = self.price_nok_kwh

        self.price_nok_kwh = self.cost.GetCurrentCost()
        self.after(20000, self.update_price)

    def update(self) -> None:

        #countdown_limit.h = 13

        if(self.enable_count_down_timer == "True"):

            now = datetime.today()

            seconds = (timedelta(hours=24) - (now - now.replace(hour=13, minute=0, second=0, microsecond=0))).total_seconds() % (24 * 3600)
            delta = timedelta(seconds = seconds)
            # TODO: Change to work for any date
            #later = datetime.fromisoformat('2022-09-13 13:00:00')
            #delta = later - now
            
            days, hours, minutes, seconds = self.td_to_days_hours_minutes_seconds(delta)
            self.countdown_time.set(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        else:
            local_time = time.localtime()
            self.countdown_time.set(f"{local_time.tm_hour:02d}:{local_time.tm_min:02d}:{local_time.tm_sec:02d}")

        #direction_arrow = "⇅"

        #self.energy_cost.set("396,34 EUR/MWh")
        if self.price_nok_kwh > self.prev_price_nok_kwh:
            direction_arrow = "↑"
        elif self.price_nok_kwh < self.prev_price_nok_kwh:
            direction_arrow = "↓"
        else: # In the unlikely case that the price has not changed.
            direction_arrow = "⇅"

        self.energy_cost.set(f"{self.price_nok_kwh*100:.2f} øre/kWh " + direction_arrow)

        self.after(500, self.update)

    def resize(self, event=None) -> None:
        new_size = -max(12, int((self.frame.winfo_width() / 10)))
        self.display_font.configure(size=new_size)
        #new_size = -max(12, int((self.frame.winfo_height() / 30)))

    def td_to_days_hours_minutes_seconds(self, td):
        days, hours, minutes  = td.days, td.seconds // 3600, td.seconds %3600//60
        seconds = td.seconds - hours*3600 - minutes*60
        return days, hours, minutes, seconds
        #return td.days, td.seconds//3600, (td.seconds//60)%60, 0


if __name__ == "__main__":
    config = configparser.ConfigParser()

    if not os.path.exists(config_file):
        with open(config_file, "w") as f:
            config.write(f)


    config.read(config_file)

    #print("Verdi: ", str(config['DISPLAY']['FontSize']))
    #print(os.getcwd())
    app = App(config) #font_size)
    app.wm_attributes('-fullscreen', 'True')
    app.mainloop()
