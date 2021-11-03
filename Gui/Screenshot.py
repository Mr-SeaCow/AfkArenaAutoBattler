# ./Gui/Screenshot.py
import time

import PySimpleGUI as sg
import pyautogui
import cv2

from ImageRec.Constants import getScreenRegion


def screenshotWindow():
    layout2 = [
        [sg.Input(key='-Screenshot_Name-')],
        [sg.Button('Cancel', key='-Screenshot_Cancel-', button_color=('White', 'Red')), sg.Button('Confirm', key='-Screenshot_Confirm-')]
        ]
    win = sg.Window('Save Screenshot', layout2);
    win.Finalize()
    win.TKroot.transient()
    win.TKroot.grab_set()
    win.TKroot.focus_force()
    while True:
        events, values = win.read()

        if events in [None, '-Screenshot_Cancel-']:
            win.close()
            break;
        elif events in ['-Screenshot_Confirm-']:
            takeScreenshot(values['-Screenshot_Name-'])
            win.close()
            break;

    
def takeScreenshot(name=None):
    if (name is None):
        name = time.strftime("%Y%m%d-%H%M%S")
    pyautogui.screenshot(f'Images\ScreenShots\{name}.png', region=getScreenRegion())