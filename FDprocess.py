# this program is a version of 'firedetection.py' that is intended for performance testing

import cv2
import numpy as np

class FDProcess:
    def __init__(self, scale, winWidthp, winHeightp, stepWidthp, stepHeightp):
        self.scale = scale
        self.winWidthp = winWidthp
        self.winHeightp = winHeightp
        self.stepWidthp = stepWidthp
        self.stepHeightp = stepHeightp

    def processImage(self, image):
        print(f"\"{image}\"")
        initFrame = cv2.imread("./input images/"+image)
        print(f"original height: {len(initFrame)}, original width: {len(initFrame[0])}")
        
        #resizing frame based on scale
        scaled = cv2.resize(initFrame, None, fx=self.scale, fy=self.scale)
        frameHeight = len(scaled)
        frameWidth = len(scaled[0])
        print(f"scaled height: {frameHeight}, scaled width:{frameWidth}")
        # cv2.imwrite(f"./scaled images/scale={scale}-{fn}",scaled)

        boundaries = [[0,50,191],[160,220,255]] #fire boundaries
        lower = np.array(boundaries[0])
        upper = np.array(boundaries[1])
        # mask1 = cv2.inRange(frame,lower,upper)
        # cv2.imwrite(f"./masks/{boundaries}{fn}",mask1)

        windowHeight = (int)(self.winHeightp*frameHeight)
        windowWidth = (int)(self.winWidthp*frameWidth)
        stepHeight = (int)(windowHeight*self.stepHeightp)
        stepWidth = (int)(windowWidth*self.stepWidthp)

        numWindowsProcessed=0 #this can be deleted, doesn't affect program functionality
        print(f"winHeight: {windowHeight}, windowWidth: {windowWidth}, stepHeight: {stepHeight}, stepWidth: {stepWidth}")
        pixelThreshold = (int)((frameHeight*frameWidth)/10000) #0.01% of the image
        print(f"pixel threshold: {pixelThreshold}")

        # nested loop reads image left to right and top to bottom
        heightOutOfBounds = False
        fireDetected = False
        for y in range(0,frameHeight,stepHeight):
            yWinLen = y+windowHeight
            yLenNxtWin = yWinLen+stepHeight #height along frame of next window
            if yLenNxtWin>frameHeight: #checking if the window height is out of bounds
                yWinLen+=(windowHeight-(yLenNxtWin-frameHeight)) #adding on to the current window the portion of the next window that's in bounds
                heightOutOfBounds = True
            widthOutOfBounds = False
            for x in range(0,frameWidth,stepWidth):
                xWinLen = x+windowWidth
                xLenNxtWin = xWinLen+stepWidth
                if xLenNxtWin>frameWidth: 
                    xWinLen+=(windowWidth-(xLenNxtWin-frameWidth))
                    widthOutOfBounds = True
                window = scaled[y:(yWinLen),x:(xWinLen)]
                #print(f"height: {len(window)}, width: {len(window[0])}: [{y}:{yWinLen},{x}:{xWinLen}]")
                mask = cv2.inRange(window, lower, upper)
                numRed = cv2.countNonZero(mask)
                if numRed>pixelThreshold:
                    print(f"fire detected, numRed={numRed}, range=[{y}:{yWinLen},{x}:{xWinLen}]")
                    fireDetected = True
                    # cv2.imshow("window",window)
                    # cv2.waitKey(0)
                numWindowsProcessed+=1
                if widthOutOfBounds or fireDetected: break
            if heightOutOfBounds or fireDetected: break

        print(f"number of windows processed: {numWindowsProcessed}")

        #checking if the image was correctly processed
        match image: #this match-case structure won't work on python versions before 3.10
            case "sf6.jpeg":
                if fireDetected: print("Correct Detection")
                else: print("Incorrect Detection")
            case "sf6-no fire.jpg":
                if fireDetected: print("Incorrect Detection")
                else: print("Correct Detection")
            case "sf6-no smoke.jpg":
                if fireDetected: print("Correct Detection")
                else: print("Incorrect Detection")
            case "sf6-no water.jpg":
                if fireDetected: print("Correct Detection")
                else: print("Incorrect Detection")
            case "sf6-very small fire.jpg":
                if fireDetected: print("Correct Detection")
                else: print("Incorrect Detection")
            case _: print("test accuracy unkown") 

        cv2.destroyAllWindows()