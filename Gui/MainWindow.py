import PySimpleGUI as sg
import time
import threading
import math
from Threads.MainThread import *

BattleSettingsLayout = [
          [ sg.Checkbox('All On/Off', size=(12, 1), enable_events=True, key='Master')],
         ]

DefaultLayout = ['Try Again', 'Battle', 'Challenge', 'Defeat', 'Victory', 'Begin', 'Manual Raku']


class MainWindow:
    def __init__(self, lay):
       
        self.layout = [
            [self._buildMenuBar()],
            #[sg.Text(size=(10, 2), font=('Helvetica', 20), justification='center', key='-DEBUG_MOUSEPRINT-')],
            [sg.Frame('Auto Battle Settings', layout=self._buildLayout(lay))],
            [sg.Frame('Raku Position', layout=self._buildRakuLayout())]
            ]

        self.window = sg.Window(title="AFK ARENA HELPER", layout=self.layout, margins=(50, 50))
        
        self._runningImgChecks = False
        self._runningVictory = False
        self._nextThreadRun = 0
        self._runningManualRaku = False
        self._currentRound = -1

        self._mainEventLoop()

    def _mainEventLoop(self):
        while True:
            event, values = self.window.read(timeout=10)

            if self._handleWindowEvents(event, values) == False:
                break;
           # self.window['-DEBUG_MOUSEPRINT-'].update(f'{pyautogui.position()}')
    
    def _handleWindowEvents(self, event, values):
            #print(event)
            if event == sg.WIN_CLOSED or event == 'Cancel':
                return False;
            elif '-THREAD-' in event:
                self._handleThreadEvents(event, values)
            elif '-MENU-' in event:
                self._handleMenuEvents(event, values)
            elif self._canRunThreads() and values['Master'] == True and math.ceil(time.time()) > self._nextThreadRun:
                threading.Thread(target=mainThread, args=(self.window, self._filteredValues(values)), daemon=True).start()
                self._runningImgChecks = True
           
            return True

    def _handleMenuEvents(self, event, values):
        print(event)
        return

    def _handleThreadEvents(self, event, values):
            if event == '-THREAD-DefaultImageCheck-':
                for val in values[event]:
                    print(val)
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
            if key.startswith('RAKU_'):
                returnValues.append(values[key])
        return values    

    def _buildMenuBar(self):
        menu = [['File', ['Open::-MENU-', 'Save::-MENU-']]]

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

MainWindow(BattleSettingsLayout)