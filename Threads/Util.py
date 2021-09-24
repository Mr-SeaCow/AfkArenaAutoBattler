import pyautogui
from Threads.ImageInfo import ImageInfo
import time
def checkImage(imageLink, c=.75, g=True):

    img = pyautogui.locateCenterOnScreen('./TemplateImages/'+imageLink + '.png', grayscale=g, confidence=c)
    val = ImageInfo(imageLink)
    if img != None:
        val.setCoords(img)

    return val

def handleClick(imageInfo):
    pyautogui.click(x=imageInfo.x, y = imageInfo.y, button='left')
    time.sleep(.5)
    return

