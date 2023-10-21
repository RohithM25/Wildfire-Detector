# need to change algorithm to better detect grey pixels
# could change the algorithm so that it doesn't process the large amount of black pixels that may be present in the subtracted image?

import cv2

class FDProcess:
    def __init__(self, parameters):
        self.params = parameters

    def processImage(self, baseImage, image):
        params = self.params
        
        wfile = params.writeFile
        wfile.write("\"{}\"\n".format(image))
        initFrame = cv2.imread("./input images/HPWREN/"+image)
        difference = cv2.absdiff(initFrame,baseImage)
        
        #resizing frame based on scale
        scaledOriginal = cv2.resize(initFrame, None, fx=params.scale, fy=params.scale)
        scaledDiff = cv2.resize(difference, None, fx=params.scale, fy=params.scale)
        #cv2.imshow("scaledDiff bottom right",scaledDiff[250:500,500:1000]); cv2.waitKey(0)
        #cv2.imwrite("./subtracted images/"+image,scaledDiff)        

        numWindowsProcessed=0 #this can be deleted, doesn't affect program functionality
        scaledHeight = params.scaledHeight
        scaledWidth = params.scaledWidth
        windowHeight = params.winHeight
        windowWidth = params.winWidth
        stepHeight = params.stepHeight
        stepWidth = params.stepWidth
        pixelThreshold = params.pixelThreshold
        drawBox = params.drawBox

        # nested loop reads image left to right and top to bottom
        heightOutOfBounds = False
        fireDetected = False
        numWinWithFire = 0
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
                diffWindow = scaledDiff[y:(yWinLen),x:(xWinLen)]
                originalWindow = scaledOriginal[y:(yWinLen),x:(xWinLen)]
                fireDetected = self.checkGreyPixels(originalWindow, diffWindow, (yWinLen-y), (xWinLen-x), pixelThreshold)
                if fireDetected: 
                    wfile.write("fire detected, range=[{}:{},{}:{}]\n".format(y,yWinLen,x,xWinLen))
                    numWinWithFire+=1
                    if drawBox: scaledOriginal = cv2.rectangle(scaledOriginal,(x,y),(xWinLen,yWinLen),(0,255,0),1) #drawing box on original scaled image
                numWindowsProcessed+=1
                if widthOutOfBounds or (fireDetected and not drawBox): break
            if heightOutOfBounds or (fireDetected and not drawBox): break

        wfile.write("number of windows processed: {}\n".format(numWindowsProcessed))
        if drawBox: cv2.imwrite("./boxed images/"+image,scaledOriginal)

        cv2.destroyAllWindows()
        return (numWinWithFire>0)
    
    #helper function to check for grey pixels in the subtracted window. returns True if number of grey pixels > than the threshold, returns False otherwise
    #for each pixel in the subtracted image whose RGB values average out to greater than 40 (signfies a signficant difference from the inital image, slightly arbitrary calibration)
        #check that pixel in the initial image to see if it is grey or not
        #"grey" means that the difference between any two channels cannot be greater than 20 and no channel can be less than 100 (slightly arbitrary calibration)
    def checkGreyPixels(self, originalFrame, diffFrame, frameHeight, frameWidth, pixThreshold):
        numGrey = 0
        for y in range(frameHeight):
            for x in range(frameWidth):
                diffPixel = diffFrame[y][x]
                avg = (int)((diffPixel[0]+diffPixel[1]+diffPixel[2])/3)
                if avg>40:
                    originalPixel = originalFrame[y][x]
                    #the following condition checks whether the channles of the pixel are within 20 units of each other and each channel is > 100
                    isGrey = (((abs(originalPixel[0]-originalPixel[1]))<20) and ((abs(originalPixel[0]-originalPixel[2]))<20) and ((abs(originalPixel[1]-originalPixel[2]))<20)
                                 and (originalPixel[0]>100) and (originalPixel[1]>100) and (originalPixel[2]>100))
                    if isGrey: numGrey+=1          
        #print("counter: "+str(counter)+", numGrey: "+str(numGrey))
        #cv2.imshow("masked window",originalFrame); cv2.waitKey(0)
        if numGrey > pixThreshold: return True
        return False