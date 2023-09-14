# this program is a version of 'firedetection.py' that is intended for demoing the image detection capability

import cv2
import numpy as np

class FDboundingbox:
    def __init__(self, parameters):
        self.params = parameters

    def processImage(self, image):
        params = self.params

        initFrame = cv2.imread("./input images/"+image)
        
        #resizing frame based on scale
        scaled = cv2.resize(initFrame, None, fx=params.scale, fy=params.scale)

        boundaries = [[0,50,191],[160,220,255]] #fire boundaries
        lower = np.array(boundaries[0])
        upper = np.array(boundaries[1])
        # mask1 = cv2.inRange(frame,lower,upper)
        # cv2.imwrite(f"./masks/{boundaries}{fn}",mask1)

        numWindowsProcessed=0 #this can be deleted, doesn't affect program functionality
        scaledHeight = params.scaledHeight
        scaledWidth = params.scaledWidth
        windowHeight = params.winHeight
        windowWidth = params.winWidth
        stepHeight = params.stepHeight
        stepWidth = params.stepWidth
        pixelThreshold = params.pixelThreshold

        # nested loop reads image left to right and top to bottom
        heightOutOfBounds = False
        for y in range(0,scaledHeight,stepHeight):
            yWinLen = y+windowHeight
            yLenNxtWin = yWinLen+stepHeight #height along frame of next window
            if yLenNxtWin>scaledHeight: #checking if the window height is out of bounds
                yWinLen+=(windowHeight-(yLenNxtWin-scaledHeight)) #adding on to the current window the portion of the next window that's in bounds
                heightOutOfBounds = True
            widthOutOfBounds = False
            for x in range(0,scaledWidth,stepWidth):
                xWinLen = x+windowWidth
                xLenNxtWin = xWinLen+stepWidth
                if xLenNxtWin>scaledWidth: 
                    xWinLen+=(windowWidth-(xLenNxtWin-scaledWidth))
                    widthOutOfBounds = True
                window = scaled[y:(yWinLen),x:(xWinLen)]
                mask = cv2.inRange(window, lower, upper)
                numRed = cv2.countNonZero(mask)
                if numRed>pixelThreshold:
                    print("fire detected, numRed={}, range=[{}:{},{}:{}]".format(numRed,y,yWinLen,x,xWinLen))
                    scaled = cv2.rectangle(scaled,(x,y),(xWinLen,yWinLen),(0,255,0),1)
                    # cv2.imshow("window",window)
                    # cv2.waitKey(0)
                numWindowsProcessed+=1
                if widthOutOfBounds: break
            if heightOutOfBounds: break

        print("number of windows processed: {}".format(numWindowsProcessed))
        cv2.imshow("boxed",scaled)
        cv2.waitKey(0)

        cv2.destroyAllWindows()