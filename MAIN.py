import GUI
import GLOBAL_VAR
import POP_UP



#import os
#import tkinter as tk
#from tkinter import ttk
#import time
#import threading
#import win32api     #pip install pywin32
#import win32con
#import pyautogui
#import pygetwindow as gw
#import mss
#import mouse
#import winsound

from os import getcwd, makedirs, path
from threading import Thread
from mss import mss
from mss import tools
from time import sleep
from time import strftime
from pathlib import Path
from tkinter import Tk
from winsound import Beep
from pyautogui import screenshot as pyautoScreenshot
from pygetwindow import getActiveWindow
from mouse import click


#auto-py-to-exe --noconsole --onefile --upx MAIN.py

############# CLASS #############
class Fred(Thread):
    def __init__(self, iD, name):
        Thread.__init__(self)
        self.iD :bool = iD
        self.name :str = name
        self.main_prog :bool = True
        self.counter :int = 0

    def run(self):
        if self.iD == 1:
            print("start initial prevent screen lock thread")
            while not GLOBAL_VAR.fred_kill:     #th_screenshot.is_alive():
                if GLOBAL_VAR.operating and GLOBAL_VAR.prev_screenlock:
                    POP_UP.pop_up_ss("prevert screenlock \n!caution mouse click!", 1000)
                    sleep(3)
                    print("prevent screen lock")
                    click("left")
                    # pyautogui.press("space")
                    # pyautogui.press("volumedown")
                    # pyautogui.press("volumeup")
                sleep(290)
                print(f"lock {GLOBAL_VAR.fred_kill}")
            print("end prevent screen lock thread")

        if self.iD == 2:
            print("start initial screenshots thread")
            while not GLOBAL_VAR.fred_kill:
                sleep(5)     # sleep for the first shot
                if GLOBAL_VAR.operating and not GLOBAL_VAR.fred_kill:
                    self.counter += 1
                    GLOBAL_VAR.shot_count = self.counter
                    save_screenshot(GLOBAL_VAR.shot_name, GLOBAL_VAR.shot_name2, GLOBAL_VAR.shot_nameC)
                elif not GLOBAL_VAR.operating:
                    self.counter = 0
                sleep(GLOBAL_VAR.shot_time - 5)
            print("end screenshot thread")

class TestTxtManager:
    def __init__(self):
        self.device_types = ["GENERAL", "TEHU", "CRAH"]
        self.tests_file = Path("BestShot_testName.txt")
        self.tests = {}

    def read_tests_from_file(self):
        tests = {}
        if self.tests_file.exists():
            with self.tests_file.open("r") as file:
                for line in file:
                    line = line.strip()
                    if ":" in line:
                        unit, test_str = line.split(":")
                        test_list = test_str.split(",") if test_str else []
                        tests[unit] = test_list
                        if unit not in self.device_types and unit != "GENERAL":
                            self.device_types.append(unit)
        return tests

    def write_tests_to_file(self, tests):
        with self.tests_file.open("w") as file:
            for unit, unit_tests in tests.items():
                test_str = ",".join(unit_tests)
                file.write(f"{unit}:{test_str}\n")

    def extract_device_type(self, device_name):
        for device_type in self.device_types:
            if device_type in device_name:
                return device_type
        return None

    def add_test(self, unit, test):
        unit = unit.upper()
        test = test.strip()

        if unit not in self.tests:
            self.tests[unit] = []
            if unit != "GENERAL" and unit not in self.device_types:
                self.device_types.append(unit)

        # Check for case-insensitive duplicates
        if any(t.lower() == test.lower() for t in self.tests[unit]):
            return False, "Der Test existiert bereits (mit anderer Groß-/Kleinschreibung)."

        self.tests[unit].append(test)
        self.write_tests_to_file(self.tests)
        return True, "Der Test wurde erfolgreich hinzugefügt."

    def remove_test(self, unit, test):
        unit = unit.upper()
        test = test.strip()

        if unit in self.tests and test in self.tests[unit]:
            self.tests[unit].remove(test)
            if not self.tests[unit]:
                del self.tests[unit]
            self.write_tests_to_file(self.tests)
            return True, "Der Test wurde erfolgreich entfernt."
        else:
            return False, "Der Test existiert nicht."


############# DEF #############
def change_dir(split_filename):
    dir_Path = ('./' + split_filename)
    dir_newPath = (dir_Path)
    if not path.exists(dir_newPath) and GLOBAL_VAR.folder_mode:
        makedirs(dir_newPath)
    else:
        dir_newPath = GLOBAL_VAR.folder_path


def create_shot_name(name_entry, name_entry2, name_entryC, timestamp, index):
    shot_name = name_entry
    if ((name_entry2 != "test name" and name_entry2 != "") and (name_entryC != "creator" and name_entryC != "")):
        shot_name_long = (name_entry + "-" + name_entry2)
        screenshot_file = f"{shot_name_long}-{str(index).zfill(2)}-{timestamp}-{name_entryC}.png"

    elif ((name_entry2 != "test name" and name_entry2 != "") and (name_entryC == "creator" or name_entryC == "")):
        shot_name_long = (name_entry + "-" + name_entry2)
        screenshot_file = f"{shot_name_long}-{str(index).zfill(2)}-{timestamp}.png"

    elif ((name_entry2 == "test name" or name_entry2 == "") and (name_entryC != "creator" and name_entryC != "")):
        screenshot_file = f"{shot_name}-{str(index).zfill(2)}-{timestamp}-{name_entryC}.png"
    else:
        screenshot_file = f"{shot_name}-{str(index).zfill(2)}-{timestamp}.png"
    return screenshot_file

def save_screenshot(name_entry, name_entry2, name_entryC):
    global screenshot_path
    index = 1
    shot_name = name_entry
    timestamp = strftime("%y%m%d_%H-%M-%S")

    screenshot_file = create_shot_name(name_entry, name_entry2, name_entryC, timestamp, index)
    change_dir(shot_name)

    if GLOBAL_VAR.folder_mode:
        print(f"{GLOBAL_VAR.folder_mode} true")
        if not Path(shot_name, screenshot_file).is_file():
            screenshot_path = path.join(getcwd(), shot_name, screenshot_file)
        else:
            while  Path(shot_name, screenshot_file).is_file():
                index += 1
                screenshot_file = create_shot_name(name_entry, name_entry2, name_entryC, timestamp, index)
                if  not Path(shot_name, screenshot_file).is_file():
                    screenshot_path = path.join(getcwd(), shot_name, screenshot_file)
                    index = 1
    else:
        print(f"{GLOBAL_VAR.folder_mode} false")
        if not Path(shot_name, screenshot_file).is_file():
            screenshot_path = path.join(GLOBAL_VAR.folder_path, screenshot_file)
        else:
            while  Path(shot_name, screenshot_file).is_file():
                index += 1
                screenshot_file = create_shot_name(name_entry, name_entry2, name_entryC, timestamp, index)
                if  not Path(shot_name, screenshot_file).is_file():
                    screenshot_path = path.join(GLOBAL_VAR.folder_path, screenshot_file)
                    index = 1

    #TODO shots on other windows/monitor with visiualisation with monitor
    active_window = getActiveWindow()        # Überprüfe, ob ein Fenster ausgewählt ist
    if active_window and GLOBAL_VAR.capture_mode:   # selected_window = gw.getWindowsWithTitle(gw.getActiveWindowTitle())
        #selected_window[0].activate()  # Aktiviere das ausgewählte Fenster
        #pyautogui.screenshot(screenshot_path, region=(active_window.left, active_window.top, active_window.width, active_window.height))

        left, top, width, height = active_window.left, active_window.top, active_window.width, active_window.height
        monitor = {"left": left, "top": top, "width": width, "height": height}
        with mss() as sct:
            screenshot = sct.grab(monitor)
            tools.to_png(screenshot.rgb, screenshot.size, output=screenshot_path)

            print(f"Screenshot saved as {shot_name}")
    else:
        pyautoScreenshot(screenshot_path)  # Screenshot des gesamten Bildschirms
    if GLOBAL_VAR.shot_sound:
        freq = 500
        dur = 200
        Beep(freq, dur)

    POP_UP.pop_up_ss("screenshot", 500)
    return screenshot_file



def set_path():
    GLOBAL_VAR.folder_path = path.join(getcwd())
    print(GLOBAL_VAR.folder_path)

############# MAIN #############
if __name__ == "__main__":
    #th_screenshot = Fred(2, "th_screenshot")
    #th_screenshot.start()
    #th_prev_screen_lock = Fred(1, "th_prev_screen_lock")
    #th_prev_screen_lock.start()

    set_path()
    root = Tk()
    app = GUI.App(root)
    root.mainloop()