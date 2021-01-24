from tkinter import *
import math


class UI(Tk):
    def __init__(self):
        super().__init__()

        self._PINK = "#e2979c"
        self._RED = "#e7305b"
        self._GREEN = "#9bdeac"
        self._YELLOW = "#f7f5dd"
        self._FONT_NAME = "Courier"

        self._WORK_MIN = 25
        self._SHORT_BREAK_MIN = 5
        self._LONG_BREAK_MIN = 20

        self._reps = 0
        self._count = 0
        self._count_min = 0
        self._count_sec = 0
        self._current_type = ""
        self._time_tracker = None

        self.title("Pomodoro")
        self.config(padx=100, pady=50, bg=self._YELLOW)

        self._draw()

    # DRAW METHODS
    def _draw(self):
        self._draw_canvas()
        self._draw_timer_label()
        self._draw_check_label()
        self._draw_start_button()
        self._draw_reset_button()

    def _draw_canvas(self):
        self.canvas = Canvas(width=200, height=224, bg=self._YELLOW, highlightthickness=0)
        self.tomato_img = PhotoImage(file="./images/tomato.png")
        self.canvas.create_image(100, 112, image=self.tomato_img)
        self.timer_text = self.canvas.create_text(
            100, 130, text="00:00", fill="white", font=(self._FONT_NAME, 34, "bold")
        )
        self.canvas.grid(column=1, row=1)

    def _draw_timer_label(self):
        self.timer_label = Label(text="Timer", font=(self._FONT_NAME, 40, "bold"), bg=self._YELLOW, fg=self._GREEN)
        self.timer_label.grid(column=1, row=0)

    def _draw_check_label(self):
        self.check_label = Label(font=(self._FONT_NAME, 40, "bold"), bg=self._YELLOW, fg=self._GREEN)
        self.check_label.grid(column=1, row=3)

    def _draw_start_button(self):
        start_button = Button(text="Start", command=self._start_button_clicked, highlightthickness=0)
        start_button.config(padx=12, pady=6)
        start_button.grid(column=0, row=2)

    def _draw_reset_button(self):
        reset_button = Button(text="Reset", command=self._reset_button_clicked, highlightthickness=0)
        reset_button.config(padx=12, pady=6)
        reset_button.grid(column=2, row=2)

    def _draw_checkmarks(self):
        work_sessions = math.floor(self._reps / 2)
        marks = ""

        for _ in range(work_sessions):
            marks += "✔"

        self.check_label.config(text=marks)

    # REDRAW METHODS
    def _redraw_timer_text(self):
        self.canvas.itemconfig(self.timer_text, text=f"{self._count_min}:{self._count_sec}")

    # SET METHODS
    def _set_timer_label(self):
        if self._current_type == "long_break":
            self.timer_label.config(text="Break", fg=self._RED)
        elif self._current_type == "short_break":
            self.timer_label.config(text="Break", fg=self._PINK)
        else:
            self.timer_label.config(text="Work", fg=self._GREEN)

    # RESET METHODS
    def _reset_screen(self):
        self.canvas.itemconfig(self.timer_text, text="00:00")
        self.timer_label.config(text="Timer", fg=self._GREEN)
        self.check_label.config(text="")

    def _reset_time_tracker(self):
        if self._time_tracker is not None:
            self.after_cancel(self._time_tracker)

    # TIMER METHODS
    def _start_timer(self):
        self._reps += 1

        work_sec = self._WORK_MIN * 60
        short_break_sec = self._SHORT_BREAK_MIN * 60
        long_break_sec = self._LONG_BREAK_MIN * 60

        if self._reps % 8 == 0:
            self._current_type = "long_break"
            self._count_down(long_break_sec)
        elif self._reps % 2 == 0:
            self._current_type = "short_break"
            self._count_down(short_break_sec)
        else:
            self._current_type = "work"
            self._count_down(work_sec)

    def _count_down(self, count):
        self._count = count
        self._count_min = math.floor(self._count / 60)
        self._count_sec = self._count % 60

        if self._count_sec < 10:
            self._count_sec = f"0{self._count_sec}"

        if self._count > 0:
            self._time_tracker = self.after(1000, self._count_down, self._count - 1)
            self._redraw_timer_text()
        else:
            self._start_timer()

    # EVENTS
    def _start_button_clicked(self):
        self._start_timer()
        self._draw_checkmarks()
        self._set_timer_label()

    def _reset_button_clicked(self):
        self._reps = 0
        self._reset_screen()
        self._reset_time_tracker()
