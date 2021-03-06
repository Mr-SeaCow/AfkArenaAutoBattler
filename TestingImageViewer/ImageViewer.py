
import PySimpleGUI as sg
from PIL import Image
import cv2 as cv
import io

"""
Demo program to open and play a file using OpenCV
It's main purpose is to show you:
1. How to get a frame at a time from a video file using OpenCV
2. How to display an image in a PySimpleGUI Window

For added fun, you can reposition the video using the slider.
"""

col = [[sg.Text('OpenCV Demo', size=(15, 1), font='Helvetica 20')],
       [sg.Image(filename='', key='-image-', background_color="#082567")]]


def main():
    # ---===--- Get the filename --- #
    filename = sg.popup_get_file('Filename to play')
    if filename is None:
        return
    vidFile = cv.imread(filename)
    cv.imwrite('testing.png', vidFile)

    sg.theme('Black')



    layout = [[sg.Column(col),
              sg.Column([[sg.Button('Exit', size=(7, 1), pad=((600, 0), 3), font='Helvetica 14')]])]]

    # create the window and show it without the plot
    window = sg.Window('Demo Application - OpenCV Integration', layout, no_titlebar=False, location=(0, 0))

    # locate the elements we'll be updating. Does the search only 1 time
    image_elem = window['-image-']

    # ---===--- LOOP through video file by frame --- #
    cur_frame = 0

    scale_percent = 50 # percent of original size
    width = int(vidFile.shape[1] * scale_percent / 100)
    height = int(vidFile.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv.resize(vidFile, dim, interpolation = cv.INTER_AREA)

    while True:
        event, values = window.read(timeout=0)
        if event in ('Exit', None):
            break
           
        if cur_frame == 0:
            imgbytes = cv.imencode('.png', resized)[1].tobytes()  

            image_elem.update(data=imgbytes)

        cur_frame += 1
       #ret, frame = vidFile.read()
       #if not ret:  # if out of data stop looping
       #    break
       ## if someone moved the slider manually, the jump to that frame
       #if int(values['-slider-']) != cur_frame-1:
       #    cur_frame = int(values['-slider-'])
       #    vidFile.set(cv.CAP_PROP_POS_FRAMES, cur_frame)
       #slider_elem.update(cur_frame)
       #cur_frame += 1
       #
       #imgbytes = cv.imencode('.png', frame)[1].tobytes()  # ditto
       #image_elem.update(data=imgbytes)

            #############
            #    | |    #
            #    | |    #
            #    |_|    #
            #  __   __  #
            #  \ \ / /  #
            #   \ V /   #
            #    \_/    #
"""         #############
        # This was another way updates were being done, but seems slower than the above
        img = Image.fromarray(frame)    # create PIL image from frame
        bio = io.BytesIO()              # a binary memory resident stream
        img.save(bio, format= 'PNG')    # save image as png to it
        imgbytes = bio.getvalue()       # this can be used by OpenCV hopefully
        image_elem.update(data=imgbytes)
"""

main()