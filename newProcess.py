import multiprocessing
import pyglet

class newProcess(multiprocessing.Process):
    #x1, x2, y1, y2, batch, w, h, xSubset = None
    def __init__(self, x1, x2, y1, y2, batch, w, h, xSubset):
        multiprocessing.Process.__init__(self)
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.batch = batch
        self.w = w
        self.h = h
        self.xSubset = xSubset

    def run(self):
        #multiprocessing.Process.run(self)
        #print('progress: ', round((pX/w)*100, 1), '%')
        #global x1, x2, y1, y2, batch, w, h, xSubset
        print('ping')
        for pX in range(int(((self.xSubset*self.w)/4)), int(((self.xSubset+1)*self.w)/4)):
            for pY in range(0, self.h):
                col = int(computeSet(pX, pY, self.x1, self.x2, self.y1, self.y2, self.w, self.h))
                #self.batch.add(1, pyglet.gl.GL_POINTS, None, ('v2f', (pX, pY)), ('c3B', (abs(col-255),20,20)))
        print('ping2')



def map(rangeLow, rangeHigh, newRangeLow, newRangeHigh, measure):
    num = ((measure-rangeLow)/(rangeHigh-rangeLow))*(newRangeHigh-newRangeLow)+newRangeLow
    return num

def computeSet(pX, pY, limX1, limX2, limY1, limY2, w, h):
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
