# -*- coding: utf-8 -*-
# Comunicacion serial en python
# se deben instalar las librerias seriales
# con el comando:
# pip install serial y
# pip instal pyserial
# Henry Jimenez Rosero. Tecnoparque  Nodo Cali.2019.
import datetime as dt
import tkinter as tk
import tkinter.font as tkFont

import matplotlib.figure as figure
import matplotlib.animation as animation
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

###############################################################################

update_interval = 100 
max_elements = 1440    

root = None
dfont = None
frame = None
canvas = None
ax1 = None
temp_plot_visible = None



fullscreen = False
temp_plot_visible = True
light_plot_visible = True

###############################################################################



def toggle_fullscreen(event=None):

    global root
    global fullscreen


    fullscreen = not fullscreen
    root.attributes('-fullscreen', fullscreen)
    resize(None)   


def end_fullscreen(event=None):

    global root
    global fullscreen


    fullscreen = False
    root.attributes('-fullscreen', False)
    resize(None)


def resize(event=None):

    global dfont
    global frame


    new_size = -max(12, int((frame.winfo_height() / 15)))
    dfont.configure(size=new_size)


def toggle_temp():

    global canvas
    global ax1
    global temp_plot_visible


    temp_plot_visible = not temp_plot_visible
    ax1.collections[0].set_visible(temp_plot_visible)
    ax1.get_yaxis().set_visible(temp_plot_visible)
    canvas.draw()


def toggle_light():

    global canvas
    global ax2
    global light_plot_visible

 
    light_plot_visible = not light_plot_visible
    ax2.get_lines()[0].set_visible(light_plot_visible)
    ax2.get_yaxis().set_visible(light_plot_visible)
    canvas.draw()


def animate(i, ax1, ax2, xs, temps, lights, temp_c, lux):

  
    try:
        new_temp = round(np.random.randn())#round(np.random.randn(10))
        new_lux = round(np.random.randn())
    except:
        pass


    temp_c.set(new_temp)
    lux.set(new_lux)


    timestamp = mdates.date2num(dt.datetime.now())
    xs.append(timestamp)

   
    temps.append(new_temp)
    lights.append(new_lux)

  
    xs = xs[-max_elements:]
    temps = temps[-max_elements:]
    lights = lights[-max_elements:]

    color = 'tab:red'
    ax1.clear()
    ax1.set_ylabel('Temperatura (C)', color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.fill_between(xs, temps, 0, linewidth=2, color=color, alpha=0.3)

    
    color = 'tab:blue'
    ax2.clear()
    ax2.set_ylabel('Presion (Bar)', color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.plot(xs, lights, linewidth=2, color=color)

    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    fig.autofmt_xdate()


    ax1.collections[0].set_visible(temp_plot_visible)
    ax2.get_lines()[0].set_visible(light_plot_visible)


def _destroy(event):
    pass

#######################################################
## Main
root = tk.Tk()
root.title("Tablero Sensores Tecnoparque")


frame = tk.Frame(root)
frame.configure(bg='white')

frame.pack(fill=tk.BOTH, expand=1)


fig = figure.Figure(figsize=(2, 2))
fig.subplots_adjust(left=0.1, right=0.8)
ax1 = fig.add_subplot(1, 1, 1)


ax2 = ax1.twinx()


xs = []
temps = []
lights = []


temp_c = tk.DoubleVar()
lux = tk.DoubleVar()


dfont = tkFont.Font(size=-24)


canvas = FigureCanvasTkAgg(fig, master=frame)
canvas_plot = canvas.get_tk_widget()


label_temp = tk.Label(frame, text='Temperatura:', font=dfont, bg='white')
label_celsius = tk.Label(frame, textvariable=temp_c, font=dfont, bg='white')
label_unitc = tk.Label(frame, text="C", font=dfont, bg='white')
label_light = tk.Label(frame, text="Presion:", font=dfont, bg='white')
label_lux = tk.Label(frame, textvariable=lux, font=dfont, bg='white')
label_unitlux = tk.Label(frame, text="Bar", font=dfont, bg='white')
button_temp = tk.Button(    frame, 
                            text="Cambia Temperatura", 
                            font=dfont,
                            command=toggle_temp)
button_light = tk.Button(   frame,
                            text="Cambia Presion",
                            font=dfont,
                            command=toggle_light)
button_quit = tk.Button(    frame,
                            text="salir",
                            font=dfont,
                            command=root.destroy)


canvas_plot.grid(   row=0, 
                    column=0, 
                    rowspan=5, 
                    columnspan=4, 
                    sticky=tk.W+tk.E+tk.N+tk.S)
label_temp.grid(row=0, column=4, columnspan=2)
label_celsius.grid(row=1, column=4, sticky=tk.E)
label_unitc.grid(row=1, column=5, sticky=tk.W)
label_light.grid(row=2, column=4, columnspan=2)
label_lux.grid(row=3, column=4, sticky=tk.E)
label_unitlux.grid(row=3, column=5, sticky=tk.W)
button_temp.grid(row=5, column=0, columnspan=2)
button_light.grid(row=5, column=2, columnspan=2)
button_quit.grid(row=5, column=4, columnspan=2)


for w in frame.winfo_children():
    w.grid(padx=5, pady=5)


for i in range(0, 5):
    frame.rowconfigure(i, weight=1)
for i in range(0, 5):
    frame.columnconfigure(i, weight=1)


root.bind('<F11>', toggle_fullscreen)
root.bind('<Escape>', end_fullscreen)
root.bind('<Configure>', resize)


root.bind("<Destroy>", _destroy)




fargs = (ax1, ax2, xs, temps, lights, temp_c, lux)
ani = animation.FuncAnimation(  fig, 
                                animate, 
                                fargs=fargs, 
                                interval=update_interval)               


toggle_fullscreen()
root.mainloop()