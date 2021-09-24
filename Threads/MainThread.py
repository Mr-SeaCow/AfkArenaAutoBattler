from Threads.Functions import *
from ImageRec.Util import *

UltPosition = [
    (1000, 1260),
    (1125, 1260),
    (1260, 1260),
    (1390, 1260),
    (1520, 1260)]


def mainThread(window, values):
    results = defaultImageChecks(values)
    handleResults(window, results)
    window.write_event_value('-THREAD-DefaultImageCheck-', results)

def manualRaku(window, values):
    start = time.time()

    rakuPosition = None
    print(values)
    for i in range(0, 5):
        if values[f'RAKU_{i}'] == True:
            rakuPosition = i

    if rakuPosition == None:
        window.write_event_value('-THREAD-ManualRakuDone-', 'START')
        return;

    while time.time() < 4+start:
        results = checkForRaku()

        for imgCheck in results:
            if imgCheck.key == 'Victory' or imgCheck.key == 'Defeat':
                if imgCheck.found == True:
                    window.write_event_value('-THREAD-ManualRakuDone-', 'START')
                    return;

            if imgCheck.key == 'RakuClose' and imgCheck.found == False:
                window.write_event_value('-THREAD-ManualRakuDone-', 'START')
                return;
        
        for i in range(0, 5):
            if i == rakuPosition:
                continue;
            pyautogui.click(x=UltPosition[i][0], y=UltPosition[i][1], button='left')

    window.write_event_value('-THREAD-ManualRakuDone-', 'START')
    

def handleVictory(window, currentRound):

    pyautogui.screenshot('Example.png')
    StatsImg = checkImage('RoundStats')

    if StatsImg != None:
       handleClick(StatsImg)
    
    ###############################################
    #   WAS USED TO SCROLL DOWN FOR SCREENSHOTS   #
    ###############################################

    #pyautogui.moveTo(x=screenWidth/2, y=screenHeight/2)
    #pyautogui.drag(yOffset=-200, button='left', duration=0.5, mouseDownUp=True)
    #print(pyautogui.position())
    #time.sleep(.5)

    pyautogui.screenshot('Tempstats.png', region=(910,34,699,1364))
    text = getImageText('Tempstats.png')

    subDir = 'MISC'

    if r'Stage' in text:
        subDir = 'Campaign'
    elif "King's Tower" in text:
        subDir = 'Kings Tower'
        text = 'Floor ' + str(getFloor(text))
    elif 'Tower of Light' in text:
        subDir = 'Lightbearer Tower'
        text = 'Floor ' + str(getFloor(text))
    elif 'Brutal Citadel' in text:
        subDir = 'Mauler Tower'
        text = 'Floor ' + str(getFloor(text))
    elif 'World Tree' in text:
        subDir = 'Wilder Tower'
        text = 'Floor ' + str(getFloor(text))
    elif 'Forsaken' in text:
        subDir = 'Gravebearer Tower'
        text = 'Floor ' +  str(getFloor(text))
    elif 'Infernal Fortress' in text:
        subDir = 'Hypogean Tower'
        text = 'Floor ' +  str(getFloor(text))

    if currentRound != -1:
        os.popen(f'mkdir "Images/BattleStatistics/{subDir}/{text}"').read()
        os.popen(f'mkdir "Images/HeroInfo/{subDir}/{text}"').read()
        subDir += f'/{text}'
        text = f'Round_{currentRound}'


    os.popen(f'cp TempStats.png "Images/BattleStatistics/{subDir}/{text}.png"').read()
    os.remove('TempStats.png');
    HeroInfo = checkImage('HeroInfo')

    if HeroInfo != None:
       handleClick(HeroInfo)
       time.sleep(1)
       pyautogui.screenshot('Tempheroinfo.png', region=(876,34,776,1363))
       os.popen(f'cp Tempheroinfo.png "Images/HeroInfo/{subDir}/{text}.png"').read()
       os.remove('Tempheroinfo.png');

    CloseImg = checkImage('Close')

    if CloseImg != None:
       handleClick(CloseImg)

    time.sleep(.5)
    handleClick(checkImage('Victory'))
    window.write_event_value('-THREAD-UpdateCurRound-', -1)
    window.write_event_value('-THREAD-HandleVictory-', False)

def handleResults(window, results):

    if len(results) == 0:
        return;

    for result in results:
        if result.key == 'Victory':
            window.write_event_value('-THREAD-HandleVictory-', True)
            return

        if result.key == 'Begin' or result.key == 'Battle':
            rounds = checkForStages()
            if (len(rounds) > 1):
                for round in rounds:
                    print(round)

                raise ValueError('Too many rounds were found - MainThreads.py')
            if (len(rounds) == 1):
                curRound = [int(i) for i in ''.join((ch if ch in '0123456789' else ' ') for ch in rounds[0].key).split()][0]
                window.write_event_value('-THREAD-UpdateCurRound-', curRound)
        if result.key == 'ManualRaku':
            window.write_event_value('-THREAD-ManualRaku-', 'START')
            return;
    handleClick(results[0])