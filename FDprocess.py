# this program is a version of 'firedetection.py' that is intended for performance testing

import cv2
import numpy as np
import FDparams

class FDProcess:
    def __init__(self, parameters):
        self.params = parameters

    def processImage(self, image, numCorrect):
        params = self.params
        
        wfile = params.writeFile
        wfile.write("\"{}\"\n".format(image))
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
        fireDetected = False
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
                    wfile.write("fire detected, numRed={}, range=[{}:{},{}:{}]\n".format(numRed,y,yWinLen,x,xWinLen))
                    fireDetected = True
                    # cv2.imshow("window",window)
                    # cv2.waitKey(0)
                numWindowsProcessed+=1
                if widthOutOfBounds or fireDetected: break
            if heightOutOfBounds or fireDetected: break

        wfile.write("number of windows processed: {}\n".format(numWindowsProcessed))

        #checking if the image was correctly processed
        if image == "sf6-resized1000,500.jpeg": 
            if fireDetected:
                numCorrect+=1
                wfile.write("Correctly Processed\n")
            else: wfile.write("Incorrectly Processed\n")
        elif image == "sf6-no fire.jpg": 
            if not fireDetected:
                numCorrect+=1
                wfile.write("Correctly Processed\n")
            else: wfile.write("Incorrectly Processed\n")
        elif image == "sf6-no smoke.jpg": 
            if fireDetected:
                numCorrect+=1
                wfile.write("Correctly Processed\n")
            else: wfile.write("Incorrectly Processed\n")
        elif image == "sf6-no water.jpg": 
            if fireDetected:
                numCorrect+=1
                wfile.write("Correctly Processed\n")
            else: wfile.write("Incorrectly Processed\n")
        elif image == "sf6-very small fire.jpg":
            if fireDetected:
                numCorrect+=1
                wfile.write("Correctly Processed\n")
            else: wfile.write("Incorrectly Processed\n")
        else: print("{} accuracy unknown".format(image))

        cv2.destroyAllWindows()
        return numCorrect