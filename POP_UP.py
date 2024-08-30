
import tkinter as tk

def pop_up_ss(label, time):
    win = tk.Toplevel()
    win.geometry("150x50")
    win.attributes('-topmost', True)
    win.overrideredirect(True)
    tk.Label(win, text=str(label), font=('Helvetica 10 bold')).pack(pady=10)
    win.after(int(time), win.destroy)

    # Bring the window to the front
    win.lift()
    win.attributes('-topmost', True)
    win.focus_force()
