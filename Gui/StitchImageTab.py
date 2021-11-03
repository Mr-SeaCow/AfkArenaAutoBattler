# ./Gui/StitchImageTab.py
import math
import time

import PySimpleGUI as sg
import pyautogui
import cv2

from ImageRec.Constants import getScreenRegion
from ImageRec.ImageStitch import stitchImages, battleStitch


def buildStitchLayout():
    height = 400
    lay = [
        [
            sg.Column(layout=[
                [
                    sg.Frame('Image Viewer', layout=[
                        [
                            sg.Text('Choose a file: '), 
                            sg.Input(key='-STITCH-FileInputName'), 
                            sg.FileBrowse(key='-STITCH-FileBrowse', file_types=(('*.png *', '*.jpg *')))
                        ],
                        [
                            sg.Button('Submit', key='-STITCH-SubmitFileBrowse')
                        ]
                    ]),
                ],
                [
                    sg.Frame('Stitch Heroes', layout=[
                        [
                            sg.Text('Choose files: '), 
                            sg.Input(key='-STITCH-StitchInput'), 
                            sg.FilesBrowse(key='-STITCH-StitchBrowse', file_types=(('*.png *', '*.jpg *')))
                        ],
                        [
                            sg.Button('Stitch', key='-STITCH-SubmitStitch')
                        ]
                    ]),
                ],
                [
                    sg.Frame('Stitch Battles', layout=[
                        [
                            sg.Text('Choose files: '), 
                            sg.Input(key='-STITCH-StitchBattleInput'), 
                            sg.FilesBrowse(key='-STITCH-StitchBattleBrowse', file_types=(('*.png *', '*.jpg *')))
                        ],
                        [
                            sg.Button('Stitch', key='-STITCH-SubmitBattleStitch')
                        ]
                    ]),
                ]
            ]),
            sg.Column(layout=[[
                sg.Frame('Settings', layout=[
                    [
                        sg.Frame('Image Scale', [[
                            sg.Slider(range=(1, 100), default_value=30, resolution=1, orientation='h', key='-STITCH-ImageScale', change_submits=True)
                        ]])
                    
                    ], 
                    [
                        sg.Frame('Crop in Pixels', [
                            [
                                sg.Input('125', key='-STITCH-TopCrop'),
                                sg.Text('Top')
                            ],
                            [
                                sg.Input('325', key='-STITCH-BottomCrop'),
                                sg.Text('Bottom'),
                            ]
                        ])
                    ]

                ])
            ]])
        ],
        [ 
         sg.Image(data='', key='-STITCH-DisplayImage', metadata='', right_click_menu=[[''], ['Show Ruler::-STITCH-ShowRuler', 'Hide Ruler::-STITCH-HideRuler', 'Crop Image::-STITCH-CropImage']])
        ]
    ]

    """
    TODO

    G = Interface
    F = Function
    I = Implemented
     G  F  I   
    [X][X][X] Take Screenshot
    [X][X][X] Pick Image
    [X][X][X] Pick AutoCrop dimensions
    [X][X][X] Preview AutoCropDimensions
    [X][X][X] Show Ruler
    [X][X][X] Show Crop 
    [X][ ][ ] Stitch Image Selection
    [ ][ ][ ] Flood Fill Image
    """
    return lay

def takeScreenshot(name=None):
    if (name is None):
        name = time.strftime("%Y%m%d-%H%M%S")
    pyautogui.screenshot(f'Images\ScreenShots\{name}.png', region=getScreenRegion())

def openImage(fileName, window, values, selection='SHOW'):
    img = cv2.imread(fileName)
    imgData = showImageWithFunction(img, selection, window=window, values=values)
    window['-STITCH-DisplayImage'].update(data=imgData)
    window['-STITCH-DisplayImage'].metadata = fileName
    print(window['-STITCH-DisplayImage'].metadata)
    return;

def showRuler(window, values):
    fileName = getFileName(window)
    openImage(fileName, window, values, 'RULER')
    return

def showCrop(window, values):
    fileName = getFileName(window)
    openImage(fileName, window, values, 'CROP')
    return

def hideRuler(window, values):
    fileName = getFileName(window)
    openImage(fileName, window, values, 'SHOW')
    return

def startStitchImage(window, values):
    imgAra = values['-STITCH-StitchBrowse'].split(';')
    topCrop = int(values['-STITCH-TopCrop'])
    bottomCrop = int(values['-STITCH-BottomCrop'])
    stitchImages(imgAra, topCrop, bottomCrop)
    return

def startStitchBattle(window, values):

    imgAra = values['-STITCH-StitchBattleBrowse'].split(';')
    battleStitch(imgAra)
    return;

def getFileName(window):
    return window['-STITCH-DisplayImage'].metadata

def showImageWithFunction(img, selection, params=None, window=None, values=None):
    if selection == 'SHOW':
        return showImage(img, window=window, values=values)
    elif selection == 'RULER':
        return showImage(img, buildRuler, window=window, values=values)
    elif selection == 'CROP':
        return showImage(img, cropImg, window=window, values=values)
    
def showImage(img, func=None, p1=None, p2=None, window=None, values=None):
    postImg = img
    if (p1 is None and func is not None):
        postImg = func(img, values=values)
    elif (p2 == None and func is not None):
        postImg = func(img, p1)
    elif (func is not None):
        postImg = func(img, p1, p2)
    return encodeImageToPreview(scaleImage(postImg, values=values))

def encodeImageToPreview(img, values=None):
    return cv2.imencode('.png', img)[1].tobytes()  

def cropImg(img, yTop=220, yBottom=600, values=None):
    print(values)
    if validateCropSize(img, values):
        print('here')
        yTop = int(values['-STITCH-TopCrop'])
        yBottom = int(values['-STITCH-BottomCrop'])

    return img[yTop:img.shape[0]-yBottom :].copy()

def validateCropSize(img, values):
    if values == None:
        return False
    top = int(values['-STITCH-TopCrop'])
    bottom = int(values['-STITCH-BottomCrop'])
    print(top, bottom)

    if top+bottom > img.shape[0] or top < 0:
        return False

    return True

def buildRuler(img, values=None):
    heightMarker = 0
    cv2.rectangle(img, (0, 0), (200, img.shape[0]), (0, 0, 0), -1)
    while (heightMarker < img.shape[0]):
        lineLength = 20
        thickness = 3
        if (heightMarker % 50 == 0):
            lineLength = 40
            thickness = 4
        if (heightMarker % 100 == 0):
            thickness = 6
            lineLength = 60
            img = cv2.putText(img, str(heightMarker).rjust(4, '0'), (0, heightMarker + 10), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 4)
        print((200-lineLength, heightMarker), (lineLength, heightMarker))
        img = cv2.line(img, (200-lineLength, heightMarker), (200, heightMarker), (255, 255, 255), thickness);
        heightMarker += 10
    return img

def scaleImage(img, scale=30, values=None):
    if values is not None:
        scale = values['-STITCH-ImageScale']

    width = int(img.shape[1] * scale / 100)
    height = int(img.shape[0] * scale / 100)
    return cv2.resize(img, (width, height), interpolation = cv2.INTER_AREA)