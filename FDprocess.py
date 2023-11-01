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
        
        #resizing frame based on scale
        scaledOriginal = cv2.resize(initFrame, None, fx=params.scale, fy=params.scale)
        #cv2.imwrite("./scaled images/scale={}-{}".format(params.scale,image),scaledOriginal)

        scaledDiff = cv2.absdiff(scaledOriginal,baseImage)
        #cv2.imshow("scaledDiff bottom right",scaledDiff[250:500,500:1000]); cv2.waitKey(0)
        #cv2.imwrite("./subtracted images/"+image,scaledDiff)        

        numWindowsProcessed=0 #this can be deleted, doesn't affect program functionality
        scaledHeight = params.scaledHeight
        scaledWidth = params.scaledWidth
        windowHeight = params.winHeight
        windowWidth = params.winWidth
        stepHeight = params.stepHeight
        stepWidth = params.stepWidth
        args = params.argsStr
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
                #change this ^^ method signature to take y, yWinLen, x, xWinLen and the baseImage
                if fireDetected: 
                    wfile.write("fire detected, range=[{}:{},{}:{}]\n".format(y,yWinLen,x,xWinLen))
                    numWinWithFire+=1
                    if drawBox: scaledOriginal = cv2.rectangle(scaledOriginal,(x,y),(xWinLen,yWinLen),(0,255,0),1) #drawing box on original scaled image
                numWindowsProcessed+=1
                if widthOutOfBounds or (fireDetected and not drawBox): break
            if heightOutOfBounds or (fireDetected and not drawBox): break

        wfile.write("number of windows processed: {}\n".format(numWindowsProcessed))
        if drawBox: 
            imageSplit = (image.split(".")) #splitting the image into its name and file extension
            cv2.imwrite("./boxed images/{}/'{}'.{}".format(args,imageSplit[0],imageSplit[1]),scaledOriginal)

        cv2.destroyAllWindows()
        return (numWinWithFire>0)
    
    #helper function to check for grey pixels in the subtracted window. returns True if number of grey pixels > than the threshold, returns False otherwise
    #for each pixel in the subtracted image whose RGB values average out to greater than 40 (signfies a signficant difference from the inital image, slightly arbitrary calibration)
        #check that pixel in the initial image to see if it is grey or not
        #"grey" means that the difference between any two channels cannot be greater than 20 and no channel can be less than 100 (slightly arbitrary calibration)
        #blue color range for [R,G,B]: [0-180,100-200,140-255]
    def checkGreyPixels(self, originalFrame, diffFrame, frameHeight, frameWidth, pixThreshold):
        numGrey = 0
        darkCalib = 100 #"darkness calibration": slightly arbitrary value used to exclude pixels that are below a certain pixel channel value (pixels that are too dark/black)
        pvt = 20 #"pixel variability threshold": slightly arbitrary value used to exclude pixels that are "not grey enough"
        for y in range(frameHeight):
            for x in range(frameWidth):
                diffPixel = diffFrame[y][x]
                avg = (int)((diffPixel[0]+diffPixel[1]+diffPixel[2])/3)
                if avg>30:
                    originalPixel = originalFrame[y][x]
                    #the following condition checks whether the channles of the pixel are within 20 units of each other and each channel is > 100
                    isGrey = (((abs(originalPixel[0]-originalPixel[1]))<pvt) and ((abs(originalPixel[0]-originalPixel[2]))<pvt) and ((abs(originalPixel[1]-originalPixel[2]))<pvt)
                                 and (originalPixel[0]>darkCalib) and (originalPixel[1]>darkCalib) and (originalPixel[2]>darkCalib))
                    if isGrey: numGrey+=1   
                    else: #check if it's a "greyed blue"
                        #is greyed blue means for the BGR channels: the B value has dropped by at least 20, G fell by at least 10, R value doesn't matter
                        
                        pass       
        #print("counter: "+str(counter)+", numGrey: "+str(numGrey))
        #cv2.imshow("masked window",originalFrame); cv2.waitKey(0)
        if numGrey > pixThreshold: return True
        return False