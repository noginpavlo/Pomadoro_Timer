from tkinter import *


PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

working_sessions = 1
timer = 0
time_to_work = True
# -------------------------------- TIMER RESET ----------------------------------- #


def reset_time():
    global working_sessions, timer, time_to_work
    working_sessions = 0
    time_to_work = True
    if timer != 0:
        window.after_cancel(timer)
        timer = 0
    canvas.itemconfig(text, text="00:00")
    canvas.itemconfig(status, text="Press start")
# ------------------------------ TIMER MECHANISM --------------------------------- #


def start_time():
    global working_sessions, time_to_work
    if working_sessions < 4:
        if time_to_work:
            canvas.itemconfig(status, text="Work")
            count_down(WORK_MIN * 60)
            time_to_work = False
        else:
            count_down(SHORT_BREAK_MIN * 60)
            canvas.itemconfig(status, text="Short break")
            time_to_work = True
            working_sessions += 1
            print(working_sessions)
    elif working_sessions == 4:
        if time_to_work:
            canvas.itemconfig(status, text="Work")
            count_down(WORK_MIN * 60)
            time_to_work = False
        else:
            count_down(LONG_BREAK_MIN * 60)
            canvas.itemconfig(status, text="Long break")
            time_to_work = True
            working_sessions = 1
# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #


def count_down(count):
    global time_to_work, working_sessions
    minutes, seconds = divmod(count, 60)
    canvas.itemconfig(text, text=f"{minutes:02}:{seconds:02}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        if working_sessions < 4:
            if time_to_work:
                canvas.itemconfig(status, text="Work")
                canvas.itemconfig(text, text="25:00")
            else:
                count_down(SHORT_BREAK_MIN * 60)
                canvas.itemconfig(status, text="Short break")
                canvas.itemconfig(text, text="5:00")
        elif working_sessions == 4:
            if time_to_work:
                canvas.itemconfig(status, text="Work")
                canvas.itemconfig(text, text="25:00")
            else:
                count_down(LONG_BREAK_MIN * 60)
                canvas.itemconfig(status, text="Long break")
                canvas.itemconfig(text, text="20:00")
        window.after_cancel(timer)
# ---------------------------------- UI SETUP ------------------------------------- #


window = Tk()

window.title("Pomodoro Timer")
window.geometry("600x500")
window.configure(bg=YELLOW)

menu_frame = Frame(bg=YELLOW)

canvas = Canvas(menu_frame, width=200, height=350, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 212, image=tomato_img)
text = canvas.create_text(103, 230, text="00:00", fill=YELLOW, font=(FONT_NAME, 24))
status = canvas.create_text(103, 60, text="Press start", fill=PINK, font=(FONT_NAME, 20, "bold"))
canvas.grid(row=1, column=1, padx=10, pady=10)

start_button = Button(menu_frame, text="Start", command=start_time, bg=PINK, font=(FONT_NAME, 24))
start_button.grid(row=2, column=0, padx=20, pady=20, sticky="w")

reset_button = Button(menu_frame, text="Reset", command=reset_time, bg=PINK, font=(FONT_NAME, 24))
reset_button.grid(row=2, column=2, padx=10, pady=10, sticky="e")

menu_frame.pack()

window.mainloop()
