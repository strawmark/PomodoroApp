import math
import tkinter
from tkinter import *

PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"

FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

WINDOW_H = 220
WINDOW_W = 200

timer = None
reps = 0
session = False


class HoverButton(Button):
    def __init__(self, master, **kwargs):
        Button.__init__(self, master=master, **kwargs)
        self.default_background = self['background']
        self.bind("<Enter>", self.__on_enter)
        self.bind("<Leave>", self.__on_leave)

    def __on_enter(self, event):
        self['background'] = self['activebackground']

    def __on_leave(self, event):
        self['background'] = self.default_background


def reset_timer():
    global reps, session
    if session:
        window.after_cancel(timer)
        canvas.itemconfig(timer_text, text=f'00:00')
        title_label.config(text='Pomodoro')
        checkmarks_label.config(text=' ')
        reps = 0
        session = False


def count_down(count):
    global reps, timer
    count_min = math.floor(count/60)
    count_sec = count % 60

    if count_sec < 10:
        count_sec = f'0{count_sec}'

    if count_min < 10:
        count_min = f'0{count_min}'

    canvas.itemconfig(timer_text, text=f'{count_min}:{count_sec}')

    if count > 0:
        timer = window.after(1000, count_down, count-1)
    else:
        checkmarks = ''
        work_sessions = math.floor(reps/2)
        for i in range(0, work_sessions):
            checkmarks = checkmarks+'✔ '
        checkmarks_label.config(text=checkmarks)
        start_count_down()


def start_count_down():
    global reps
    reps += 1

    if reps % 8 == 0:
        count_down(LONG_BREAK_MIN * 60)
        title_label.configure(text='Pausa', fg=RED)
    elif reps % 2 == 0:
        count_down(SHORT_BREAK_MIN * 60)
        title_label.config(text='Pausa', fg=PINK)
    else:
        count_down(WORK_MIN * 60)
        title_label.config(text='Lavoro', fg=GREEN)


def start_timer():
    global session
    if not session:
        session = True
        start_count_down()


window = Tk()
window.title('Pomodoro')
window.config(padx=50, pady=25, bg=YELLOW)
window.resizable(False, False)

title_label = Label(text='Pomodoro', fg=GREEN, highlightthickness=0, font=(FONT_NAME, 28), bg=YELLOW)
title_label.grid(column=1, row=0)

canvas = Canvas(width=WINDOW_W, height=WINDOW_H, bg=YELLOW, highlightthickness=0)
background_image = PhotoImage(file='tomato.png')
canvas.create_image(WINDOW_W//2, WINDOW_H//2, image=background_image)
timer_text = canvas.create_text(WINDOW_W//2, WINDOW_H//2 + 20, text='00:00', fill='white', font=(FONT_NAME, 28, 'bold'))
canvas.grid(column=1, row=1)

checkmarks_label = Label(text=' ', font=(FONT_NAME, 10, 'bold'), fg=GREEN, highlightthickness=0, bg=YELLOW)
checkmarks_label.grid(column=1, row=3)


start_button = HoverButton(
    master=window,
    background=GREEN,
    foreground=YELLOW,
    activebackground=RED,
    activeforeground=PINK,
    highlightthickness=0,
    highlightbackground=PINK,
    highlightcolor=RED,
    border=0,
    width=8,
    height=1,
    cursor='hand2',
    font=('Arial', 12, 'bold'),
    text='Avvia',
    command=start_timer
)
start_button.grid(column=0, row=2)

reset_button = HoverButton(
    master=window,
    background=GREEN,
    foreground=YELLOW,
    activebackground=RED,
    activeforeground=PINK,
    highlightthickness=0,
    highlightbackground=PINK,
    highlightcolor=RED,
    border=0,
    width=8,
    height=1,
    cursor='hand2',
    font=('Arial', 12, 'bold'),
    text='Resetta',
    command=reset_timer
)
reset_button.grid(column=2, row=2)

window.mainloop()
