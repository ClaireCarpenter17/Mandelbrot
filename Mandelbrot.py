from time import process_time
import multiprocessing as mp
import newProcess as np
import pyglet

def map(rangeLow, rangeHigh, newRangeLow, newRangeHigh, measure):
    num = ((measure-rangeLow)/(rangeHigh-rangeLow))*(newRangeHigh-newRangeLow)+newRangeLow
    return num

def computeSet(pX, pY, limX1, limX2, limY1, limY2):
    #c = complex(map(0, w, -2.00, 0.47, pX), map(0, h, -1.12, 1.12, pY))
    c = complex(map(0, w, limX1, limX2, pX), map(0, h, limY1, limY2, pY))
    complexFunc = lambda z : z**2 + c
    res = 0 
    iterMax = 64
    iteration = 0
    while iteration < iterMax and abs(res) <= 2.0: 
        res = complexFunc(res)
        iteration += 1
    color = map(0, iterMax, 0, 255, iteration)
    return color

def runSubset(batch, xSubset):
    processTime = process_time()
    for pX in range(int(((xSubset*w)/4)), int(((xSubset+1)*w)/4)):
        for pY in range(0, h):
            col = int(computeSet(pX, pY, x1, x2, y1, y2))
            #arr.append((pX, pY, col))
            batch.add(1, pyglet.gl.GL_POINTS, None, ('v2f', (pX, pY)), ('c3B', (abs(col-255),20,20)))
    processTime = process_time()-processTime
    print('Process', xSubset, ':', processTime)


w = 500
h = 500
x1 = -2.00
x2 = 0.47
y1 = -1.12
y2 = 1.12
x1Int = x1
x2Int = x2
y1Int = y1
y2Int = y2
crosshairLength = 10
if __name__ == '__main__':
    window = pyglet.window.Window()
    window.set_size(w, h)

    @window.event
    def on_draw():
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2f', (x1-crosshairLength, y1, x1+crosshairLength, y2)))
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2f', (x1, y1-crosshairLength, x1, y1+crosshairLength)))

        pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2f', (x2-crosshairLength, y2, x2+crosshairLength, y2)))
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2f', (x2, y2-crosshairLength, x2, y2+crosshairLength)))


    @window.event
    def on_key_press(symb, modif):
        global x1
        global y1
        global x2
        global y2
        if(chr(symb) == 'q'):
            timeStart = process_time()
            x1 = x1Int
            y1 = y1Int
            x2 = x2Int
            y2 = y2Int
            batch = pyglet.graphics.Batch()

            if __name__ == '__main__':
                p0 = mp.Process(target=runSubset(batch, 0))
                p1 = mp.Process(target=runSubset(batch, 1))
                p2 = mp.Process(target=runSubset(batch, 2))
                p3 = mp.Process(target=runSubset(batch, 3))

                p0.daemon = True
                p1.daemon = True
                p2.daemon = True
                p3.daemon = True

                p0.start()
                p1.start()
                p2.start()
                p3.start()

                p0.join()
                p1.join()
                p2.join()
                p3.join()

                p0.terminate()
                p1.terminate()
                p2.terminate()
                p3.terminate()
                
                
            '''for pX in range(0, w):
                print('progress: ', round((pX/w)*100, 1), '%')
                for pY in range(0, h):
                    computeTime = process_time()
                    col = int(computeSet(pX, pY, x1, x2, y1, y2))
                    computeTime = process_time() - computeTime
                    batch.add(1, pyglet.gl.GL_POINTS, None, ('v2f', (pX, pY)), ('c3B', (abs(col-255),20,20)))'''


            batch.draw()
            timeEnd = process_time() - timeStart
            print('Elapsed time: ', timeEnd)
            #print('Elapsed time for computation: ', sumSetComputeTime)
    @window.event
    def on_mouse_press(x, y, button, modif):
        global x1Int
        global y1Int
        x1Int = map(0, w, x1, x2, x)
        y1Int = map(0, h, y1, y2, y)


    @window.event
    def on_mouse_release(x, y, button, modif):
        global x2Int
        global y2Int
        x2Int = map(0, w, x1, x2, x)
        y2Int = map(0, h, y1, y2, y)


    pyglet.app.run()
