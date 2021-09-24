
from pynput import mouse, keyboard
from ImageRec.ImageRec import getImageText
import PySimpleGUI as sg
import pyautogui
import time
import os
import concurrent.futures
#{'Master': True, 'TryAgain': False, 'Battle': False, 'Challenge': False, 'Defeat': False, 'Victory': False, 'Begin': False}


LayoutTemp = [
           'TryAgain',
           'Battle',
           'Challenge',
           'Defeat',
           'Victory',   
           'Begin' 
          ]

def runThreads(func, dataAra, confidence=.75):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        results = []
        for data in dataAra:
            futures.append(executor.submit(func, data, confidence))
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result.found == True:
                results.append(result)
        return results

def runRaku(func, dataAra, confidence=.75, grayscale=True):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        results = []
        for data in dataAra:
            futures.append(executor.submit(func, data, confidence, grayscale))
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
        return results
    
