from Threads.ImageInfo import ImageInfo
from Threads.Handler import runThreads, runRaku
from Threads.Util import *

def defaultImageChecks(values):
    results = runThreads(checkImage, values)
    return results

def checkForStages():
    dataAra = ['StageSelect1',
            'StageSelect2',
            'StageSelect3',
            'StageSelect4'
            ]
    return runThreads(checkImage, dataAra, .95)
   
def checkForRaku():
    return runRaku(checkImage, ['RakuClose', 'Victory', 'Defeat'], .7, True)

def handleImgLogic(results):
    for result in results:
        if result.key == 'Begin' or result.key == 'Battle':
            print(True)
