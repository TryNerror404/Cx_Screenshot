
import tkinter as tk
from tkinter import Label,LEFT,SOLID,Toplevel

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0
        self.timeout_id = None  # Neue Variable für den Timer
        self.delay_id = None  # Neue Variable für den Delay-Timer

    def showtip(self, event):
        "Display text in tooltip window"
        if self.tipwindow:
            return
        self.delay_id = self.widget.after(1000, self._showtip)  # 1 second delay

    def _showtip(self):
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 10
        y = y + self.widget.winfo_rooty() - 20
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)
        self.timeout_id = self.widget.after(5000, self.hidetip)  # Timer für 5 Sekunden

    def hidetip(self, event=None):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()
        if self.timeout_id:
            self.widget.after_cancel(self.timeout_id)  # Timer abbrechen
        if self.delay_id:
            self.widget.after_cancel(self.delay_id)  # Delay-Timer abbrechen