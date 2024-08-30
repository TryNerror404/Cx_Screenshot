
import MAIN
import GLOBAL_VAR
import INTRO_DIALOG
import TOOLTIP
import FILE_EDIT
import POP_UP

import sys
import tkinter as tk
#import os
import keyboard
import threading
#import subprocess
#import platform

from MAIN import TestTxtManager
from POP_UP_RENAME import show_input_dialog
from os import listdir, path, startfile
from time import strftime
from tkinter import *
from tkinter import ttk,messagebox,filedialog
from PIL import Image, ImageTk
from subprocess import Popen
from platform import system as psystem
from keyboard import unhook,unhook_key,on_press_key,KEY_DOWN


#TODO: IMPORTEND window screenshot not working on more than 2 monitores, monitor 3 blackscreen

#TODO: small symbol in taskbar like "Bluetooth"
#TODO: icon
#TODO: Genauere Beschreibungen (READ ME)
#TODO: READ ME direkt in den optionen drin; verion log, changes
#TODO: Logdatei
#TODO: dateien deutsch, englisch
#TODO: einstellbar mit stunde, minuten im screenshot
#TODO: Video aufnahme
#TODO: (Mail das screenshots fertig sind)
#TODO: prev_screen_lock mouse click, better options
#TODO: bereich makieren für shot
        #TODO: thread start by start and stop by stop 2024.07.05
        #TODO: seperate TOOLTIP 2024.06.28
        #TODO: Tool tip 2024.06.24
        #TODO: Weiteres Menü bei capchermode, screenlock mode, shot sound, mit hacken 2024.06.25
        #TODO: screenshot key anzeigen welcher aktiv ist im menü 2024.06.24
        #TODO: FOLDER mit bei OPRIONS rein nehmen 2024.06.24
        #TODO: Button to open selectet folder, screenshot folder 2024.06.24
        #TODO: Autoscreenshot anzeige wann die nächste screenshot gemacht wird 2024.06.25
        #TODO: EDITOR um die txt datei direkt zu öffnen 2024.06.24
        #TODO: Liste alphabetisch 2024.06.24
        #TODO: suche ob vorhanden ist in der txt datei 2024.06.28
        #TODO: FILE.txt in to MAIN 2024.06.28
        #TODO: zum namen, entsprechende auswahl zur unit anzeigen, zb TEMP: Feuchte, Temp, Störung, HiHi,LoLo 2024.06.28
        #TODO: menubar anpassen 2024.06.29

###### TODO UI
#TODO: new UI
#TODO: Bezeichnungen in der UI
#TODO: einstellbar wie viele autoshots und die anzeige der zeiten damit ergänzen
#TODO: (Zeit(anzahl shots)), anzahl(zeit wann fertig) einstellen wie viele screenshots über auto gemacht werden sollen
        #TODO: pop-up über key, um den testnamen zu ändern, SHIFT + CTRL" oder sonst ausgehählter name 2024.07.05
        #TODO: für txt editor ein Button anlegen 2024.06.28
        #TODO: add testName mit plus, minus auf der UI 2024.06.28
        #TODO: bessere anzeigt ob autoscreenshot aktiv ist 2024.06.28



class  App:
        def __init__(self, root):
            self.root = root

            self.setup_variables()
            self.setup_window()

            self.manager = TestTxtManager()
            self.setup_ui()
            self.setup_tooltip()

            #### key monitoring ####
            self.key_p()  # aufruf screenshot key überwachung

            self.start_listening()
            self.screenshot_hotkey = 'shift'
            self.hotkey = f'ctrl+{self.screenshot_hotkey}'
            keyboard.add_hotkey(self.hotkey, self.popup_rename)


            self.manager.tests = self.manager.read_tests_from_file()
            self.update_device_type_dropdown()
            self.load_folder()


        def setup_variables(self):
            self.is_keyboard_active :bool = False
            self.screenshot_key :str = "f9"
            self.running: bool = False
            self.start_stop_auto_toggle: bool = False
            self.extended_mode_var: bool = False
            #self.screenshot_file :str = ""   NOT NEEDED?
            self.auto_interval: int = 15
            self.auto_shotnumb: int = 4
            self.menu_ss_key_lable = tk.StringVar()
            self.menu_ss_key_lable.set(self.screenshot_key)

        def setup_window(self):
            self.root.title("Bestshot")
            self.root.resizable(False, False)
            self.root.configure(background='gray90')
            self.root.columnconfigure(0, weight=1)

            try:
                from ctypes import windll
                windell.shcore.SetProcessDpiAwareness(1)
            except:
                pass

            self.setup_icon()
            self.setup_main_frame(column=0, row=0, columnspan=3, rowspan=5, bg='gray50')
            self.setup_edit_frame(column=3, row=0, columnspan=1, rowspan=6, bg='gray80')

        def setup_icon(self):
            # ICON #
            try:
                if getattr(sys, 'frozen', False):
                    # Running as a frozen executable
                    icon_path = sys._MEIPASS + '/bildschirmfoto_ico.ico'
                    root.iconbitmap(icon_path)
                else:
                    # Running as a regular Python script
                    icon_path = './bildschirmfoto_ico.ico'
                    root.iconbitmap(icon_path)
            except:
                pass

        def setup_main_frame(self, column=1, row=0, columnspan=1, rowspan=1, bg='gray'):
            frame = tk.Frame(self.root, bg=bg)
            frame.grid(row=row, column=column, rowspan=rowspan,
                       columnspan=columnspan, padx=0, pady=0, sticky="nsew")

        def setup_edit_frame(self, column=1, row=0, columnspan=1, rowspan=1, bg='gray'):
            frame = tk.Frame(self.root, bg=bg)
            frame.grid(row=row, column=column, rowspan=rowspan,
                       columnspan=columnspan, padx=0, pady=0, sticky="nsew")

        #### FRAME ####
        def setup_menu(self):
            self.fenster = self.root
            self.menuleiste = Menu(self.fenster)

            self.settings_menu = Menu(self.menuleiste, tearoff=0)
            self.menuleiste.add_cascade(label="Options", menu=self.settings_menu)

            self.setup_menu_options()

            self.help_menu = Menu(self.menuleiste, tearoff=0)
            self.menuleiste.add_cascade(label="Help", menu=self.help_menu)
            self.setup_menu_help()

            # Die Menüleiste mit den Menüeintägen noch dem Fenster übergeben und fertig.
            self.fenster.config(menu=self.menuleiste)

        def setup_menu_options(self):
            self.settings_menu.add_command(label="screenshot key: " + self.menu_ss_key_lable.get(),
                                           command=self.action_get_key_dialog)

            self.check_folder_var = tk.IntVar()
            self.check_folder_var.set(1)
            self.sub_settings_folder = Menu(self.settings_menu, tearoff=0)
            self.sub_settings_folder.add_radiobutton(label="creat folder", variable=self.check_folder_var,
                                                     value=1, command=self.create_folder)
            self.sub_settings_folder.add_radiobutton(label="folder not created", variable=self.check_folder_var,
                                                     value=2, command=self.create_no_folder)
            self.settings_menu.add_cascade(label="folder mode", menu=self.sub_settings_folder)

            self.check_capture_var = tk.IntVar()
            self.check_capture_var.set(1)
            self.sub_settings_capture = Menu(self.settings_menu, tearoff=0)
            self.sub_settings_capture.add_radiobutton(label="capture window", variable=self.check_capture_var,
                                                      value=1, command=self.menu_capture_window)
            self.sub_settings_capture.add_radiobutton(label="capture fullscreen", variable=self.check_capture_var,
                                                      value=2, command=self.menu_capture_fullscreen)
            self.settings_menu.add_cascade(label="capture mode", menu=self.sub_settings_capture)

            self.check_screenlock_var = tk.IntVar()
            self.check_screenlock_var.set(1)
            self.sub_settings_screenlock = Menu(self.settings_menu, tearoff=0)
            self.sub_settings_screenlock.add_radiobutton(label="activ with mouse click", variable=self.check_screenlock_var,
                                                         value=1, command=self.prev_screen_lock)
            self.sub_settings_screenlock.add_radiobutton(label="deactivated", variable=self.check_screenlock_var,
                                                         value=2, command=self.prev_screen_lock)
            self.settings_menu.add_cascade(label="screenlock mode", menu=self.sub_settings_screenlock)

            self.settings_menu.add_checkbutton(label="shot sound", variable=tk.IntVar(), onvalue=1, offvalue=0,
                                               command=self.menu_shot_sound)

            self.settings_menu.add_checkbutton(label="extended mode", variable=tk.IntVar(), onvalue=1, offvalue=0,
                                               command=self.extended_mode)

        def setup_menu_help(self):
            self.help_menu.add_command(label="Intro", command=self.action_get_intro_dialog)
            self.help_menu.add_separator()
            self.help_menu.add_command(label="About", command=self.action_get_info_dialog)

        #### WINDOW ####
        def setup_main_window(self):
            column = 1
            row = 0
            padx = 5
            pady = 5
            sticky = "ew"

            self.name_entry_var = tk.StringVar()
            self.name_entry = tk.Entry(self.root, width=30, textvariable=self.name_entry_var)
            self.name_entry.insert(0, "Instanz_Object Name")
            self.name_entry.grid(column=column, row=row, padx=padx, pady=pady, sticky=sticky)
            self.name_entry_var.trace_add("write", self.update_label)
            self.name_entry.bind("<KeyRelease>", self.update_dropdown)

            self.test_entry_var = tk.StringVar()
            self.test_entry = tk.Entry(self.root, textvariable=self.test_entry_var)
            self.test_entry.insert(0, "Attribute Name")
            self.test_entry_var.trace_add("write", self.update_label)
            self.test_entry.grid(column=column, row=row +1, padx=padx, pady=pady, sticky=sticky)

            self.name_entryC_var = tk.StringVar()
            self.name_entryC = tk.Entry(self.root, textvariable=self.name_entryC_var)
            self.name_entryC.insert(0, "Creator")
            self.name_entryC_var.trace_add("write", self.update_label)
            self.name_entryC.grid(column=column, row=row +2, padx=padx, pady=pady, sticky=sticky)

            # DROPDOWN
            self.line_var = tk.StringVar()
            self.line_var.set("Select Attribute name")
            self.line_dropdown = ttk.Combobox(self.root, textvariable=self.line_var, postcommand=self.show_all_options)
            self.line_dropdown.grid(column=column +1, row=row +1, padx=padx, pady=pady, sticky=sticky)
            # self.line_dropdown = ttk.Combobox(self.root, textvariable=self.line_var)
            self.line_dropdown.bind("<<ComboboxSelected>>",
                                    lambda event: self.line_var.set(""))  # Clear text on dropdown click
            self.line_dropdown.bind("<<ComboboxSelected>>", self.update_test_entry)
            self.line_dropdown.bind("<KeyRelease>", self.update_dropdown)

            # OUTPUT
            self.lbl_path = tk.Label(self.root, text=f"{GLOBAL_VAR.folder_path}\\{self.name_entry.get()}\\...")
            self.lbl_path.grid(column=column - 1, row=row + 3, columnspan=3, padx=padx, pady=pady, sticky=sticky)

            self.lbl_shotname = tk.Label(self.root,
                                         text="...\\Instanz_Object Name-Attribute Name_Creator_01_20240819_16-16-42")
            self.lbl_shotname.grid(column=column-1, row=row+4, columnspan=3, padx=padx, pady=pady, sticky=sticky)

        def setup_folder_window(self):
            column = 0
            row = 0
            padx = 5
            pady = 5
            sticky = "ew"
            bg = "light gray"

            self.folder_var = tk.StringVar()
            self.folder_var.set("Select Folder/Unit name")
            self.folder_var.trace("w", self.update_shot_entry)
            self.folder_dropdown = ttk.OptionMenu(self.root, self.folder_var, "")
            self.folder_dropdown.grid(column=column, row=row, columnspan=1, padx=padx, pady=pady, sticky=sticky)
            #self.folder_dropdown.configure(state="disabled")

            self.load_folder_btn = tk.Button(self.root, text="change folder", command=self.change_folder, bg=bg,
                                             width=10)
            self.load_folder_btn.grid(column=column, row=row + 1, padx=padx, pady=pady, sticky="w")

            self.open_folder_btn = tk.Button(self.root, text="open folder", command=self.open_folder, bg=bg,
                                             width=10)
            self.open_folder_btn.grid(column=column, row=row + 1, padx=padx, pady=pady, sticky="e")
            # self.open_folder_btn.configure(state="disabled")

        def setup_edit_window(self):
            column = 2
            row = 0
            padx = 5
            pady = 5
            sticky = "ew"

            # self.search_entry = tk.Entry(self.root)
            # self.search_entry.grid(column=1, row=3, padx=5, pady=5, sticky="ew")
            # self.search_entry.bind("<KeyRelease>", self.update_dropdown)

            self.device_entry_var = tk.StringVar()
            self.device_entry = tk.Entry(self.root, textvariable=self.device_entry_var)
            self.device_entry.insert(0, "device type")
            #self.device_entry.grid(column=column, row=row+2, padx=padx, pady=pady, sticky=sticky)

            self.edit_test_entry_var = tk.StringVar()
            self.edit_test_entry = tk.Entry(self.root, textvariable=self.edit_test_entry_var)
            self.edit_test_entry.insert(0, "add_del Attribute")
            #self.edit_test_entry_var.trace_add("write", self.update_label)

            ### DROPDOWN
            self.device_type_var = tk.StringVar()
            self.device_type_var.set("device type")
            self.device_type_var.trace('w', self.update_device_entry)
            self.device_type_dropdown = ttk.OptionMenu(self.root, self.device_type_var, "")
            #self.device_type_dropdown.grid(column=column, row=row+2, padx=padx, pady=pady, sticky="e")

            ### BUTTON
            self.edit_file_btn = tk.Button(self.root, text="edit file", command=self.edit_text_file, bg="light gray",
                                           width=22)
            #self.edit_file_btn.grid(column=column, row=row + 1, padx=padx, pady=pady, sticky="ew")

            self.add_testname_btn = tk.Button(self.root, text="+", command=self.add_test, bg="light gray", width=5)
            #self.add_testname_btn.grid(column=column, row=row+1, padx=padx, pady=pady, sticky="w")

            self.remove_testname_btn = tk.Button(self.root, text="-", command=self.remove_test, bg="light gray",
                                                 width=5)
            #self.remove_testname_btn.grid(column=column, row=row+1, padx=padx, pady=pady, sticky="e")

        def setup_auto_window(self):
            column = 0
            row = 5
            padx = 5
            pady = 5
            sticky = "ew"

            self.interval_entry = tk.Entry(self.root)
            self.interval_entry.insert(0, str(self.auto_interval))
            #self.interval_entry.grid(column=column, row=row, padx=padx, pady=pady, sticky="w")

            self.lbl_auto_min = tk.Label(self.root, text="min.")
            #self.lbl_auto_min.grid(column=column, row=row, padx=padx, pady=pady, sticky="e")

            # self.shotnumbers_entry = tk.Entry(self.root)
            # self.shotnumbers_entry.insert(0, self.auto_shotnumb)
            # self.shotnumbers_entry.grid(column=1, row=5, padx=5, pady=5, sticky="ew")

            self.start_button = tk.Button(self.root, text="Start", command=self.start_screenshots,
                                          bg="light gray", width=30)
            #self.start_button.grid(column=column+1, row=row, padx=padx, pady=pady, sticky="ew")


            self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_screenshots, state=tk.DISABLED,
                                         bg="light gray", width=30)
            #self.stop_button.grid(column=1, row=5, padx=5, pady=5)

        def setup_ui(self):
            self.setup_menu()
            self.setup_main_window()
            self.setup_folder_window()
            self.setup_edit_window()
            self.setup_auto_window()

            #### OUTPUT ####
            self.output_text = tk.Text(self.root, height=11, width=60)
            self.output_text.grid(column=0, row=10, rowspan=2, columnspan=4, padx=7, pady=5,sticky="ew")

            self.txt_scroll = ttk.Scrollbar(self.root, orient="vertical", command=self.output_text.yview)
            self.txt_scroll.grid(column=3, row=10, rowspan=2, sticky="nse")
            self.output_text["yscrollcommand"] = self.txt_scroll.set

            self.output_box_input(text=f"Manuel-screenshot via '{self.screenshot_key}'\n\n")
            #self.output_text.insert(tk.END, f"Manuel-screenshot via '{self.screenshot_key}'\n\n")


        def lbl_path_input(self):
            if GLOBAL_VAR.folder_mode:
                self.lbl_path.config(text=f"{GLOBAL_VAR.folder_path.replace("/", "\\")}\\{self.name_entry.get()}\\...")
            else:
                self.lbl_path.config(text=f"{GLOBAL_VAR.folder_path.replace("/", "\\")}\\...")

        def output_box_input(self, index1=tk.END, text=" ", status="w"):
            if status == "w":
                self.output_text.insert(index1, f"{text}")
            elif status == "del":
                self.output_text.delete(1.0, tk.END)

        def setup_tooltip(self):
            #### TOOLTIP ####
            self.tooltip_set(self.folder_dropdown, "Select folder/unit \nload folder first")
            self.tooltip_set(self.line_dropdown, "Select test name")
            self.tooltip_set(self.device_type_dropdown, "Select device for saving test names")

            self.tooltip_set(self.start_button, "Start auto screenshot")
            self.tooltip_set(self.stop_button, "Stop auto screenshot")

            self.tooltip_set(self.name_entry, "Enter the folder/unit name f.e.:\nFR02_001T00_CRAH01")
            self.tooltip_set(self.test_entry, "Enter the test f.e.:\ncommunication_fault")
            self.tooltip_set(self.name_entryC, "Enter your initials f.e.:\nMS")
            self.tooltip_set(self.interval_entry, "Enter auto screenshot interval in min.")
            #self.tooltip_set(self.shotnumbers_entry, "Enter quantity of autoshots\n0 = infinite")
            #self.tooltip_set(self.search_entry, "search test name")
            self.tooltip_set(self.device_entry, "Enter device to save new test name")

            self.tooltip_set(self.load_folder_btn, "Load folder path to saving screenshots")
            self.tooltip_set(self.open_folder_btn, "Open folder")
            self.tooltip_set(self.edit_file_btn, "Edit file with test names "
                                                 "\nuse the structure: Unit:testname1,testname2,...")
            self.tooltip_set(self.add_testname_btn, "Add test name to file")
            self.tooltip_set(self.remove_testname_btn, "Remove test name from file")

        def tooltip_set(self, object, lable):
            ttip = TOOLTIP.ToolTip(object, lable)
            object.bind("<Enter>", ttip.showtip)
            object.bind("<Leave>", ttip.hidetip)


        def show_all_options(self):
            if self.line_var.get() == "Select Attribute name":
                self.line_var.set("")  # Clear the text
            self.update_dropdown()  # Show all options

        def update_dropdown(self, event=None, preserve_test_entry=False, *args):
            self.line_dropdown.configure(state="enable")
            current_test_entry = self.test_entry.get() if preserve_test_entry else None
            device_name = self.name_entry.get().upper()
            device_type = self.manager.extract_device_type(device_name)

            if device_name == "ALL":
                combined_tests = []
                for tests in self.manager.tests.values():
                    combined_tests.extend(tests)
                combined_tests = list(set(combined_tests))
            else:
                unit_tests = self.manager.tests.get(device_type, [])
                general_tests = self.manager.tests.get("GENERAL", [])
                combined_tests = list(set(unit_tests + general_tests))

            search_term = self.line_var.get().lower()
            if search_term == "":
                filtered_tests = combined_tests
            else:
                filtered_tests = [test for test in combined_tests if search_term in test.lower()]

            sorted_filtered_tests = sorted(filtered_tests, key=lambda s: s.lower())
            self.line_dropdown['values'] = sorted_filtered_tests  # Update the Combobox with filtered results
            if preserve_test_entry and current_test_entry is not None:
                self.test_entry.delete(0, tk.END)
                self.test_entry.insert(0, current_test_entry)

        ########    EVENT   ########
        def start_listening(self):
            print("Listening for hotkeys...")
            # Start the hotkey listener in a separate thread to avoid blocking the main thread
            listener_thread = threading.Thread(target=keyboard.wait, daemon=True)
            listener_thread.start()

        def popup_rename(self):
            print(GLOBAL_VAR.folder_path)
            newunit, newtest = show_input_dialog(self.name_entry.get(), self.test_entry.get(), "BestShot_testName.txt",
                                                 ("./" if GLOBAL_VAR.folder_path == "" else GLOBAL_VAR.folder_path))
            self.name_entry_var.set(newunit)
            self.test_entry_var.set(newtest)


        def key_p(self):
            on_press_key(self.screenshot_key, self.capture_manual_screenshot_key) # Überwache die Taste für screenshot
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing) # window observe

        def capture_manual_screenshot_key(self, e):
            if e.event_type == KEY_DOWN:
                shot_name = self.name_entry.get()
                shot_name2 = self.test_entry.get()
                shot_creator = self.name_entryC.get()

                new_name = MAIN.save_screenshot(str(shot_name), str(shot_name2), str(shot_creator))
                self.output_text.insert(tk.END, "manualshot " + str(new_name) + "\n")

        def on_closing(self): # close window
            print("window close")
            GLOBAL_VAR.fred_kill = True
            print(f"Kill fred {GLOBAL_VAR.fred_kill}")
            self.running = False
            self.root.destroy()

        def update_label(self, *args):
            # Holen Sie die Eingaben aus den Feldern
            name = self.name_entry_var.get()
            test = self.test_entry_var.get()
            name_C = self.name_entryC_var.get()

            timestamp = strftime("%y%m%d_%H-%M-%S")

            # Setzen Sie den Text des Labels auf die kombinierten Eingaben
            self.lbl_shotname.config(text=f"{name}-{test}-{name_C}-01-{timestamp}")
            self.lbl_path_input()

        ########    AUTO EVENT   ########
        def start_screenshots(self):
            GLOBAL_VAR.fred_kill = False
            MAIN.Fred(2, "th_screenshot").start()
            MAIN.Fred(1, "th_prev_screen_lock").start()
            self.start_button.grid_remove()
            self.stop_button.grid(column=1, row=5, padx=5, pady=5)
            #self.start_button.config(bg="green4")
            self.stop_button.config(bg="red4")
            GLOBAL_VAR.shot_name = self.name_entry.get()
            GLOBAL_VAR.shot_name2 = self.test_entry.get()
            GLOBAL_VAR.shot_nameC = self.name_entryC.get()

            try:    # deactivated
                GLOBAL_VAR.auto_shotnumbers = int(self.shotnumbers_entry.get())
            except:
                self.output_box_input(status="del")
                self.output_box_input(text="invalid number input, please enter intiger number" + "\n")
                #self.output_text.delete(1.0, tk.END)
                #self.output_text.insert(tk.END, "invalid number input, please enter intiger number" + "\n")


            try:
                shot_time = float(self.interval_entry.get().replace(",", "."))
                GLOBAL_VAR.shot_time = shot_time * 60

                self.start_button.config(state=tk.DISABLED)
                self.stop_button.config(state=tk.NORMAL)
                self.output_box_input(status="del")
                self.output_box_input(text="Autoscreenshot started...\n")

                #self.output_text.delete(1.0, tk.END)
                #self.output_text.insert(tk.END, "Autoscreenshot started...\n")
                GLOBAL_VAR.operating = True
                self.ss_time()
            except:
                self.output_box_input(status="del")
                self.output_box_input(text="invalid time input, please enter float number" + "\n")
                #self.output_text.delete(1.0, tk.END)
                #self.output_text.insert(tk.END, "invalid time input, please enter float number" + "\n")

        def ss_time(self):
            timestamp_H = strftime("%H")
            timestamp_M = strftime("%M")
            for i in range(4 if int(GLOBAL_VAR.auto_shotnumbers) <= 0 else int(GLOBAL_VAR.auto_shotnumbers)):
                timestamp_M = int(timestamp_M) + (int(GLOBAL_VAR.shot_time) / 60)
                if int(timestamp_M) >= 60:
                    timestamp_M = int(timestamp_M) - 60
                    timestamp_H = int(timestamp_H) + 1
                self.output_text.insert(tk.END,
                                        f"{i+1}. autoscreenshot: {timestamp_H}:{timestamp_M:02.0f}\n")

        def stop_screenshots(self):
            self.stop_button.grid_remove()
            self.start_button.grid(column=1, row=5, padx=5, pady=5)

            #self.start_button.config(bg="light gray")
            #self.stop_button.config(bg="light gray")

            GLOBAL_VAR.fred_kill = True
            GLOBAL_VAR.operating = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.output_text.insert(tk.END, f"Autoscreenshot stopped. {GLOBAL_VAR.shot_count} shots captured\n")


        ########    BUTTON EVENT   ########
        def add_test(self):
            unit = self.device_entry.get().upper()
            test = self.edit_test_entry.get()

            if not unit or not test:
                messagebox.showerror("Fehler", "Bitte geben Sie sowohl den Gerätetyp als auch den Testnamen ein.")
                return
            success, message = self.manager.add_test(unit, test)

            if success:
                self.output_text.insert(tk.END, f"Add '{test}' to '{unit}'\n")
                messagebox.showinfo("Erfolg", message)
                self.update_dropdown(preserve_test_entry=True)
            else:
                messagebox.showinfo("Info", message)

        def remove_test(self):
            unit = self.device_entry.get().upper()
            test = self.edit_test_entry.get()

            if not unit or not test:
                messagebox.showerror("Fehler", "Bitte geben Sie sowohl den Gerätetyp als auch den Testnamen ein.")
                return

            success, message = self.manager.remove_test(unit, test)
            if success:
                self.output_text.insert(tk.END, f"Removed '{test}' from '{unit}'\n")
                messagebox.showinfo("Erfolg", message)
                self.update_dropdown(preserve_test_entry=True)
            else:
                messagebox.showinfo("Info", message)


        ########    DROPDOWN EVENT   ########
        def update_shot_entry(self, *args):
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, self.folder_var.get())

        def update_test_entry(self, *args):
            self.test_entry.delete(0, tk.END)
            self.test_entry.insert(0, self.line_var.get())

        def update_device_type_dropdown(self):
            sorted_device_types = sorted(set(self.manager.device_types), key=lambda s: s.lower())
            self.device_type_var.set('')
            self.device_type_dropdown['menu'].delete(0, 'end')
            for device_type in sorted_device_types:
                self.device_type_dropdown['menu'].add_command(label=device_type,
                                                              command=lambda dt=device_type: self.device_type_var.set(dt))

        def update_device_entry(self, *args):
            self.device_entry.delete(0, tk.END)
            self.device_entry.insert(0, self.device_type_var.get())

        ########    MENU EVENT   ########
        ## MENU FILE ##
        def file_load(self):
            #GLOBAL_VAR.file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
            if GLOBAL_VAR.file_path:
                with open(GLOBAL_VAR.file_path, 'r', encoding='utf-8') as file:
                    GLOBAL_VAR.file_cont_testName = file.readlines()
                # Update Dropdown-Liste
                menu = self.line_dropdown["menu"]
                menu.delete(0, "end")
                for line in GLOBAL_VAR.file_cont_testName:
                    menu.add_command(label=line.strip(), command=lambda value=line.strip(): self.line_var.set(value))
                self.line_dropdown.configure(state="normal")

        """def file_add_txt(self):
            new_line = self.test_entry.get()
            if new_line.strip() not in [line.strip() for line in GLOBAL_VAR.file_cont_testName]:
                with open(GLOBAL_VAR.file_path, 'a', encoding='utf-8') as file:
                    file.write(new_line + "\n")
                self.file_load()
    
        def file_del_txt(self):
            line_to_delete = self.test_entry.get()
            if line_to_delete:
                GLOBAL_VAR.file_cont_testName = [line for line in GLOBAL_VAR.file_cont_testName if line.strip() != line_to_delete]
                with open(GLOBAL_VAR.file_path, 'w', encoding='utf-8') as file:
                    file.writelines(GLOBAL_VAR.file_cont_testName)
                self.file_load()"""

        def edit_text_file(self):
            editor_closed = FILE_EDIT.edit_text_file()
            if editor_closed:
                print("Der Editor wurde geschlossen.")
                self.file_load()
            else:
                print("not close")
            print(editor_closed)

        ## MENU FOLDER ##
        def load_folder(self):
            if GLOBAL_VAR.folder_path:
                self.folder_content = [f for f in listdir(GLOBAL_VAR.folder_path)
                                       if path.isdir(path.join(GLOBAL_VAR.folder_path, f))]
                menu = self.folder_dropdown["menu"]
                menu.delete(0, "end")
                for folder in self.folder_content:
                    menu.add_command(label=folder, command=lambda value=folder: self.folder_var.set(value))


        def change_folder(self):
            GLOBAL_VAR.folder_path = filedialog.askdirectory()
            if GLOBAL_VAR.folder_path:
                self.folder_content = [f for f in listdir(GLOBAL_VAR.folder_path)
                                       if path.isdir(path.join(GLOBAL_VAR.folder_path, f))]
                menu = self.folder_dropdown["menu"]
                menu.delete(0, "end")
                for folder in self.folder_content:
                    menu.add_command(label=folder, command=lambda value=folder: self.folder_var.set(value))
                self.folder_dropdown.configure(state="normal")
                self.open_folder_btn.configure(state="normal")

                self.lbl_path_input()

        def open_folder(self):
            if GLOBAL_VAR.folder_path:
                folder_path = path.join(GLOBAL_VAR.folder_path)#, self.folder_var.get()
                if path.isdir(folder_path):
                    if psystem() == "Windows":
                        startfile(folder_path)
                    elif psystem() == "Darwin":  # macOS
                        Popen(["open", folder_path])
                    else:  # Linux
                        Popen(["xdg-open", folder_path])

        """def select_folder(self):
            selected_folder = self.folder_var.get()
            self.selected_line_entry"""

        def create_folder(self):
            GLOBAL_VAR.folder_mode = True
            self.output_box_input(text="create new folder, activated\n")
            #self.output_text.insert(tk.END, "create new folder, activated\n")
            self.lbl_path_input()

        def create_no_folder(self):
            GLOBAL_VAR.folder_mode = False
            self.output_box_input(text="create new folder, deactivated\n")
            #self.output_text.insert(tk.END, "create new folder, deactivated\n")
            self.lbl_path_input()

        ## MENU Options ##
        def action_get_key_dialog(self):
            if not self.is_keyboard_active:
                self.is_keyboard_active = True
                unhook_key(self.screenshot_key)
                self.keyboard_listener = on_press(self.handle_key_press)
                self.output_text.insert(tk.END, f"Keyinput gestartet\n\n")
            else:
                messagebox.showwarning("Warnung", "Tastatureingabe läuft bereits.")

        def handle_key_press(self, event):
            self.screenshot_key = event.name
            unhook(self.keyboard_listener)
            self.is_keyboard_active = False
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f"Manuel-screenshot via '{self.screenshot_key}'\n\n")
            self.output_text.insert(tk.END, f"Keyinput stopped\n\n")
            self.key_p()
            self.menu_ss_key_lable.set(self.screenshot_key)
            self.settings_menu.entryconfig(2, label="screenshot key: " + self.menu_ss_key_lable.get())


        def menu_capture_fullscreen(self):
            GLOBAL_VAR.capture_mode = False
            self.output_text.insert(tk.END, "capture fullscreen, only main screen\n")

        def menu_capture_window(self):
            GLOBAL_VAR.capture_mode = True
            self.output_text.insert(tk.END, "capture window\n")

        def prev_screen_lock(self):
            if GLOBAL_VAR.prev_screenlock:
                GLOBAL_VAR.prev_screenlock = False
                self.output_text.insert(tk.END, "prevent screen lock, deactivated\n")
            else:
                GLOBAL_VAR.prev_screenlock = True
                self.output_text.insert(tk.END, "prevent screen lock, activated\n")

        def menu_shot_sound(self):
            if GLOBAL_VAR.shot_sound:
                GLOBAL_VAR.shot_sound = False
                self.output_text.insert(tk.END, "shot sound, deactivated\n")
            else:
                GLOBAL_VAR.shot_sound = True
                self.output_text.insert(tk.END, "shot sound, activated\n")

        def extended_mode(self):
            if self.extended_mode_var:
                self.extended_mode_var = False
                self.output_box_input(text="extended off\n")
                #self.output_text.insert(tk.END, "extended off\n")

                # self.search_entry.grid_remove()

                #self.line_dropdown.grid_remove()
                self.device_type_dropdown.grid_remove()
                self.device_entry.grid_remove()
                self.edit_test_entry.grid_remove()

                self.edit_file_btn.grid_remove()
                self.add_testname_btn.grid_remove()
                self.remove_testname_btn.grid_remove()

                self.interval_entry.grid_remove()
                self.lbl_auto_min.grid_remove()
                self.start_button.grid_remove()

            else:
                self.extended_mode_var = True
                self.output_box_input(text="extended activ\n")
                #self.output_text.insert(tk.END, "extended activ\n")

                # self.line_dropdown.grid(column=2, row=0, columnspan=1, padx=5, pady=5, sticky="ew")
                self.device_type_dropdown.grid(column=3, row=0, padx=5, pady=5, sticky="e")
                # self.search_entry.grid(column=2, row=0, padx=5, pady=5, sticky="ew")
                self.device_entry.grid(column=3, row=0, padx=5, pady=5, sticky="w")
                self.edit_test_entry.grid(column=3, row=1, padx=5, pady=5, sticky="ew")

                # self.edit_file_btn.grid(column=3, row=2, padx=5, pady=5, sticky="ew") # dont work well
                self.add_testname_btn.grid(column=3, row=2, padx=5, pady=5, sticky="w")
                self.remove_testname_btn.grid(column=3, row=2, padx=5, pady=5, sticky="e")

                self.interval_entry.grid(column=0, row=5, padx=5, pady=5, sticky="w")
                self.lbl_auto_min.grid(column=0, row=5, padx=5, pady=5, sticky="e")
                self.start_button.grid(column=1, row=5, padx=5, pady=5, sticky="ew")

        ## MENU HELP ##
        def action_get_intro_dialog(self):
            messagebox.showinfo(message=INTRO_DIALOG.intro_txt, title="Introduction")

        def action_get_info_dialog(self):
            info_txt = "\
        ************************\n\
        Autor: Schoenenborn\n\
        Version: 0.9.01\n\
        ************************"
            messagebox.showinfo(message=info_txt, title="Infos")