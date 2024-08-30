
import tkinter as tk
import GLOBAL_VAR
import os

from tkinter import Tk, ttk, Label, Entry, Button, simpledialog

class InputDialog(simpledialog.Dialog):
    def __init__(self, parent, unitname='', testname='', data_file='BestShot_testName', folder_path='.'):
        self.unitname_default = unitname
        self.testname_default = testname
        self.data_file = data_file
        self.folder_path = folder_path
        self.unitname = None
        self.testname = None
        self.test_options = []
        self.folder_options = self.get_folder_names()
        self.data = self.load_data()
        super().__init__(parent)

    def load_data(self):
        data = {}
        with open(self.data_file, 'r') as file:
            for line in file:
                key, value = line.strip().split(':')
                data[key] = value.split(',')
        return data

    def get_folder_names(self):
        return [name for name in os.listdir(self.folder_path) if os.path.isdir(os.path.join(self.folder_path, name))]

    def update_test_options(self, event=None):
        unitname_input = self.unitname_entry.get()
        unitname_keys = [key for key in self.data if key in unitname_input + "GENERAL"]

        self.test_options = []
        for key in unitname_keys:
            self.test_options.extend(self.data[key])

        self.test_options = list(set(self.test_options))  # Remove duplicates
        self.testname_combobox['values'] = self.test_options

    def combobox_selected(self, event):
        selected_test = self.testname_combobox.get()
        self.testname_entry.delete(0, tk.END)
        self.testname_entry.insert(0, selected_test)

    def folder_combobox_selected(self, event):
        selected_folder = self.folder_combobox.get()
        self.unitname_entry.delete(0, tk.END)
        self.unitname_entry.insert(0, selected_folder)
        self.update_test_options()

    def body(self, master):
        self.title("Input Popup")
        self.attributes('-topmost', True)

        self.resizable(False, False)
        #self.geometry("450x150")

        #tk.Label(master, text="Select Unit Folder:").grid(row=0, column=0)
        self.folder_combobox = ttk.Combobox(master, values=self.folder_options)
        self.folder_combobox.grid(row=0, column=2, columnspan=2)
        self.folder_combobox.bind('<<ComboboxSelected>>', self.folder_combobox_selected)

        tk.Label(master, text="Unit Name:").grid(row=0, column=0)
        self.unitname_entry = tk.Entry(master)
        self.unitname_entry.grid(row=0, column=1)
        self.unitname_entry.insert(0, self.unitname_default)
        self.unitname_entry.bind('<KeyRelease>', self.update_test_options)

        tk.Label(master, text="Test Name:").grid(row=1, column=0)
        self.testname_entry = tk.Entry(master)
        self.testname_entry.grid(row=1, column=1)
        self.testname_entry.insert(0, self.testname_default)

        tk.Label(master, text="Select Test:").grid(row=2, column=0)
        self.testname_combobox = ttk.Combobox(master)
        self.testname_combobox.grid(row=2, column=1)
        self.testname_combobox.bind('<<ComboboxSelected>>', self.combobox_selected)

        self.update_test_options()
        return self.unitname_entry  # initial focus

    def apply(self):
        self.unitname = self.unitname_entry.get()
        self.testname = self.testname_entry.get()


def show_input_dialog(unitname='', testname='', data_file='BestShot_testName', folder_path='.'):
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    dialog = InputDialog(root, unitname, testname, data_file, folder_path)

    # Check if the dialog was cancelled
    if dialog.unitname is not None and dialog.testname is not None:
        return dialog.unitname, dialog.testname
    return unitname, testname