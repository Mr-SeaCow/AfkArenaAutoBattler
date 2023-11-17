# ./Gui/MainWindow.py
import time
import threading
import math
import PySimpleGUI as sg
import pyautogui as ag

import cv2

from Threads.MainThread import *
from Gui.StitchImageTab import buildStitchLayout, takeScreenshot, openImage, showRuler, hideRuler, showCrop, startStitchImage, startStitchBattle
from Gui.Screenshot import screenshotWindow

BattleSettingsLayout = [
          [ sg.Checkbox('All On/Off', size=(12, 1), enable_events=True, key='Master')],
         ]

DefaultLayout = ['Try Again', 'Battle', 'Challenge', 'Defeat', 'Victory',  'Begin', 'Event Battle', 'Victory (No Screenshot)', 'Manual Raku']

def make_win1():
    layout = [[sg.Text('This is the FIRST WINDOW'), sg.Text('      ', k='-OUTPUT-')],
              [sg.Text('Click Popup anytime to see a modal popup')],
              [sg.Button('Launch 2nd Window'), sg.Button('Popup'), sg.Button('Exit')]]

    return sg.Window('Window Title', layout, location=(800,600), finalize=True)


class MainWindow:
    def __init__(self, lay, widgets):
       
        self.layout = [
            [self._buildMenuBar(widgets)],
            [sg.TabGroup(self._buildTabGroups(lay))],
            #[sg.Frame('Widgets', layout=[[sg.Button('Test')]])],
            #[sg.Frame('Auto Battle Settings', layout=self._buildLayout(lay))],
            #[sg.Frame('Raku Position', layout=self._buildRakuLayout())]
            ]
        self.window = sg.Window(title="AFK ARENA HELPER", layout=self.layout, default_element_size=(12, 1))

        self._runningImgChecks = False
        self._runningVictory = False
        self._nextThreadRun = 0
        self._runningManualRaku = False
        self._currentRound = -1

        self._retryCount = 0
        self._prevKeys = []

        self._mainEventLoop()
    

    def _buildTabGroups(self, lay):
        returnAra = []
        returnAra.append(
            [sg.Tab('AutoBattle', layout=self._buildAutoBattle(lay))],
        )
        returnAra.append(
            [sg.Tab('Upload', layout=[[sg.Button('Test')]])]
        )
        returnAra.append(
            [sg.Tab('Stitch', layout=self._buildStitchLayout())]
        )
        return returnAra

    def _buildAutoBattle(self, lay):
        return [
                    [sg.Frame('Auto Battle Settings', layout=self._buildLayout(lay))],
                    [sg.Frame('Raku Position', layout=self._buildRakuLayout())]
               ]


    def _buildStitchLayout(self):
        #lay = [[ 
        #    sg.Column(
        #        layout=[[
        #            sg.Frame(title='Screenshot', layout=
        #                [[
        #                sg.Input(default_text='Screenshot Name', enable_events=True, key='-STITCH-ScreenShotName'),
        #                sg.Button('Take Screenshot', enable_events=True, key='-STITCH-TakeScreenShot', disabled=True)
        #                ]], 
        #                size=(225, height))
        #        ]],
        #        size=(240,height)
        #    ), 
        #    sg.Column(
        #        layout=[[
        #            sg.Image(data=imgbytes)
        #        ]], 
        #        element_justification='c'
        #    )
        # ]]

        """
            Pick Image
            Pick AutoCrop dimensions
            Preview AutoCropDimensions
            Show Ruler
            Stitch Image Selection
            Flood Fill Image
        """


        return buildStitchLayout()

    def _mainEventLoop(self):
        while True:
            event, values = self.window.read(timeout=10)

            if self._handleWindowEvents(event, values) == False:
                break;
           # self.window['-DEBUG_MOUSEPRINT-'].update(f'{pyautogui.position()}')
    
    def _handleWindowEvents(self, event, values):
            if event == sg.WIN_CLOSED or event == 'Cancel':
                return False;
            elif '-THREAD-' in event:
                self._handleThreadEvents(event, values)
            elif '-MENU-' in event:
                self._handleMenuEvents(event, values)
            elif '-WIDGET-' in event:
                self._handleWidgetEvents(event, values)
            elif '-STITCH-' in event:
                self._handleStitchEvents(event, values)
            elif self._canRunThreads() and values['Master'] == True and math.ceil(time.time()) > self._nextThreadRun:
                threading.Thread(target=mainThread, args=(self.window, self._filteredValues(values)), daemon=True).start()
                self._runningImgChecks = True
           
            return True

    def _handleMenuEvents(self, event, values):
        print(event)
        return

    def _handleWidgetEvents(self, event, values):
        if 'Screenshot' in event:
            screenshotWindow()
        return

    def _handleStitchEvents(self, event, values):
        if 'SubmitFileBrowse' in event:
            openImage(values['-STITCH-FileInputName'], self.window, values)
        elif 'ShowRuler' in event:
            showRuler(self.window, values)
        elif 'HideRuler' in event:
            hideRuler(self.window, values)
        elif 'CropImage' in event:
            showCrop(self.window, values)
        elif 'SubmitStitch' in event:
            startStitchImage(self.window, values)
        elif 'SubmitBattleStitch' in event:
            startStitchBattle(self.window, values)
        return

    def _handleThreadEvents(self, event, values):
            if event == '-THREAD-DefaultImageCheck-':
                for val in values[event]:
                    print(val)
                self._countRetries(values[event])
                self._runningImgChecks = False
                self._nextThreadRun = math.ceil(time.time()) + .5
            elif event == '-THREAD-UpdateCurRound-':
                self._currentRound = values[event]
                print('CurRound', self._currentRound)
            elif event == '-THREAD-HandleVictory-':
                self._runningVictory = values[event]
                if (values[event] == True):
                    threading.Thread(target=handleVictory, args=(self.window, self._currentRound), daemon=True).start()
            elif event == '-THREAD-ManualRaku-':
                self._runningManualRaku = True
                threading.Thread(target=manualRaku, args=(self.window, self._buildRakuValues(values)), daemon=True).start()
            elif event == '-THREAD-ManualRakuDone-':
                 self._runningManualRaku = False
            return
    
    def _buildLayout(self, layout):
        for item in DefaultLayout:
            layout.append([sg.Checkbox(item, size=(20, 1), enable_events=True, key=item.replace(' ', ''))])
        return layout

    def _buildRakuLayout(self):
        layout = []
        for i in range(0, 5):
            layout.append(sg.Radio(f'Position {5-i}', 'RAKU_RADIO', k=f'RAKU_{i}', enable_events=True))
        return [layout]

    def _buildRakuValues(self, values):
        returnValues = []
        for key in values:
            if isinstance(key, str) and key.startswith('RAKU_'):
                returnValues.append(values[key])
        return values    

    def _buildMenuBar(self, widgets):
        menu = [
                 ['File', ['Open::-MENU-', 'Save::-MENU-']],
                 ['Widgets', ['Screenshot::-WIDGET-']]
               ]

        return sg.Menu(menu, tearoff=False)

    def _canRunThreads(self):
        return self._runningImgChecks == False and self._runningVictory == False and self._runningManualRaku == False
    
    def _filteredValues(self, values):

        retVal = []
        for item in values:
            if item == 'Master' or not isinstance(item, str) or item.startswith('RAKU_'):
                continue

            itemKey = item.replace(' ', '')
            if values[itemKey] == True:
                retVal.append(itemKey)

        return retVal

    def _countRetries(self, values):
        if len(values) == 0:
            return
        temp = ''
        for val in values:
            if val.key ==  'TryAgain':
                temp = 'Try Again'
            elif val.key == 'Battle':
                temp = 'Battle'

        if temp == '':
            self._retryCount = 0
            return
        else:
            self._prevKeys.append(temp) 
            if len(self._prevKeys) < 2:
                return

        if len(self._prevKeys) > 2:
            self._prevKeys.pop(0)
        
        if self._prevKeys[0] == 'Try Again' and self._prevKeys[1] == 'Battle':
            self._retryCount = 1 + self._retryCount
            print(f'    Retries: {self._retryCount}')


MainWindow(BattleSettingsLayout, [])