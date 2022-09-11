from array import ArrayType
from time import process_time
import multiprocessing as mp
import newProcess as np
from pyglet import image as ImagePyglet
import pyglet
from PIL import Image
import numpy
import time

def newMap(rangeLow, rangeHigh, newRangeLow, newRangeHigh, measure):
    num = ((measure-rangeLow)/(rangeHigh-rangeLow))*(newRangeHigh-newRangeLow)+newRangeLow
    return num

def computeSet(pX, pY, limX1, limX2, limY1, limY2):
    c = complex(newMap(0, w, limX1, limX2, pX), newMap(0, h, limY1, limY2, pY))
    complexFunc = lambda z : z**2 + c
    res = 0 
    iterMax = 64
    iteration = 0
    while iteration < iterMax and abs(res) <= 2.0: 
        res = complexFunc(res)
        iteration += 1
    color = newMap(0, iterMax, 0, 255, iteration)
    return color

def runSubset(xSubset, qu, x1, x2, y1, y2):
    processTime = process_time()
    arr = numpy.zeros((h, int(w/NUM_PROCESSES), 3), dtype=numpy.uint8)
    for pX in range(int(((xSubset*w)/NUM_PROCESSES)), int(((xSubset+1)*w)/NUM_PROCESSES)):
        for pY in range(0, h):
            col = int(computeSet(pX, pY, x1, x2, y1, y2))
            arr[pY, int(newMap(int(((xSubset*w)/NUM_PROCESSES)), int(((xSubset+1)*w)/NUM_PROCESSES), 0, w/NUM_PROCESSES, pX))] = [abs(col-255), 20, 20]
    qu.put([arr, xSubset])
    processTime = process_time()-processTime
    print('Process', xSubset, ':', processTime)

def multiProcess():
    start = time.time()
    global imageArray
    arrStorage = [*range(NUM_PROCESSES)]
    q = mp.JoinableQueue()
    processes = []

    for a in range(0, NUM_PROCESSES):
        p = mp.Process(target=runSubset, args=(a, q, x1, x2, y1, y2))
        processes.append(p)
        p.start()
    time2 = time.time()
    for p in range(NUM_PROCESSES):
        #Take each array slice from queue and store them in appropriate order in arrStorage
        val = q.get()
        q.task_done()
        arrStorage[val[1]] = val[0]
    time2 = time.time() - time2
    for p in processes:
        #Wait for processes to catch up and terminate when complete
        p.join()
        p.terminate()
    for s in arrStorage:
        #Concatenate all arrays in order which they appear in arrStorage
        
        imageArray = numpy.concatenate((imageArray, s), axis=1)

    start = time.time() - start
    print('time for every multiprocessing thing: ', start)
    print('time to process queue:', time2)

def processImage():
            #Saves array d to tempImage using Pillow's .fromarray   
            global imageArray 
            tempImage = Image.fromarray(imageArray, mode='RGB')

            #Turns tempImage to bytes
            raw = tempImage.tobytes()

            #Turns raw into a pyglet image and displays
            window.clear()
            image = ImagePyglet.ImageData(tempImage.width, tempImage.height, 'RGB', raw)
            image.blit(0, 0, 0)
            
            imageArray = numpy.zeros((h, 0, 3), dtype=numpy.uint8)





w = 500
h = 500
x1 = -2.00
x2 = 0.47
y1 = -1.12
y2 = 1.12
NUM_PROCESSES = 8
imageArray = numpy.zeros((h, 0, 3), dtype=numpy.uint8)
x1Int = x1
x2Int = x2
y1Int = y1
y2Int = y2
crosshairLength = 10
if __name__ == '__main__':
    window = pyglet.window.Window()
    window.set_size(w, h)


    # @window.on_show
    # def on_show():
    #     multiProcess()
    #     processImage()

    @window.event
    def on_draw():
        pass


    @window.event
    def on_key_press(symb, modif):
        global x1
        global y1
        global x2
        global y2
        if(chr(symb) == 'q'):
            #sets function limits according to chosen zoom window
            x1 = x1Int
            y1 = y1Int
            x2 = x2Int
            y2 = y2Int

            multiProcess()
            processImage()


    @window.event
    def on_mouse_press(x, y, button, modif):
        global x1Int
        global y1Int
        x1Int = newMap(0, w, x1, x2, x)
        y1Int = newMap(0, h, y1, y2, y)


    @window.event
    def on_mouse_release(x, y, button, modif):
        global x2Int
        global y2Int
        x2Int = newMap(0, w, x1, x2, x)
        y2Int = newMap(0, h, y1, y2, y)


    pyglet.app.run()
