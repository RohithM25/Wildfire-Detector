import time
import sys
import cv2
import FDprocess as fdp
import FDparams as fdparams
import FDcorrectnesschecker as fdcc

#scale, window, and step paramaters. these parameters are taken in as command line arguments
#values should be > 0. should also be <= 1 for reasonable applications, but technically doesn't have to be
scale = float(sys.argv[1])
percentageOrSet = float(sys.argv[2]) #0|1 flag that checks whether to have a set window size or a percentage. 0 is percentage, 1 is set

if percentageOrSet == 0:
    winWidth = float(sys.argv[3]) #percentage of the frame width that window width should be
    winHeight = float(sys.argv[4]) #percentage of the frame height that window height should be
elif percentageOrSet == 1:
    winWidth = int(sys.argv[3])
    winHeight = int(sys.argv[4])
else:
    print("Input format error: window size flag invalid")
    quit()

stepWidthp = float(sys.argv[5]) #percentage of the window width that should be stepped over when moving to the next window
stepHeightp = float(sys.argv[6]) #percentage of the window height that should be stepped over when moving to the next row of windows

drawBoxes = int(sys.argv[7]) #boolean to decide whether to draw boxes or not. '0' means no boxes, '1' means draw boxes
if drawBoxes==0: drawBoxes=False
elif drawBoxes==1: drawBoxes=True
else: 
    print("Input format error: drawBoxes flag invalid"); 
    quit()

outputFilename = str(scale)+"-"+("%d" % percentageOrSet)+"-{}-{}-{}-{}.txt".format(winWidth,winHeight,stepWidthp,stepHeightp)
writeFile = open("./output/"+outputFilename,'w')

baseImages = [("1-2400.jpg",4),("2-2400.jpg",4),("3-2400.jpg",4),("4-2400.jpg",4),("5-2400.jpg",4),("7-2400.jpg",4),("8-2400.jpg",4)
              ,("9-2400.jpg",4),("10-2400.jpg",4)]
images = ["1-1200.jpg","1+0000.jpg","1+1200.jpg","1+2400.jpg","2-1200.jpg","2+0000.jpg","2+1200.jpg","2+2400.jpg",
          "3-1200.jpg","3+0000.jpg","3+1200.jpg","3+2400.jpg","4-1200.jpg","4-0420.jpg","4+1200.jpg","4+2400.jpg",
          "5-1200.jpg","5+0000.jpg","5+1200.jpg","5+2400.jpg","7-1200.jpg","7+0000.jpg","7+1200.jpg","7+2400.jpg",
          "8-1200.jpg","8+0000.jpg","8+1200.jpg","8+2400.jpg","9-1200.jpg","9+0000.jpg","9+1200.jpg","9+2400.jpg",
          "10-1200.jpg","10+0000.jpg","10+1200.jpg","10+2400.jpg",]

numImages = len(images)
numIterationsPerImage=1
numCorrect = 0
imageArrOffset=0
incorrectlyProcessedImages = set()
start = time.time()
for h in range(len(baseImages)):
    baseImageName = baseImages[h][0]
    writeFile.write(baseImageName+"\n")
    baseImage = cv2.imread("./input images/HPWREN/"+baseImages[h][0])
    baseImageHeight = len(baseImage)
    baseImageWidth = len(baseImage[0])
    writeFile.write("Image height: {}, Image width: {}\n".format(baseImageHeight, baseImageWidth))

    scaledHeight = (int)(baseImageHeight*scale)
    scaledWidth = (int)(baseImageWidth*scale)
    writeFile.write("scaled height: {}, scaled width: {}\n".format(scaledHeight,scaledWidth))

    if percentageOrSet == 0:
        windowHeight = (int)(winHeight*scaledHeight)
        windowWidth = (int)(winWidth*scaledWidth)
    writeFile.write("winHeight: {}, winWidth: {}\n".format(windowHeight,windowWidth))

    stepHeight = (int)(windowHeight*stepHeightp)
    stepWidth = (int)(windowWidth*stepWidthp)
    writeFile.write("stepHeight: {}, stepWidth: {}\n".format(stepHeight,stepWidth))

    pixelThreshold = (int)((scaledHeight*scaledWidth)/10000) #0.01% of the image
    writeFile.write("pixel threshold: {}\n".format(pixelThreshold))

    writeFile.write("-------------------------------------------------\n")

    params = fdparams.FDparams(writeFile,scale,scaledHeight,scaledWidth,windowWidth,windowHeight,stepWidth,stepHeight,pixelThreshold,drawBoxes)
    imageProcessor = fdp.FDProcess(params)

    #apparently should use python 'timeit' module to measure program execution duration
    for i in range(numIterationsPerImage):
        sum=0
        numChildren = baseImages[h][1]
        for k in range(numChildren):
            image = images[imageArrOffset+k]
            start2 = time.time()
            detected = imageProcessor.processImage(baseImage, image)
            end2 = time.time()
            elapsed = end2-start2
            writeFile.write(("%.7f" % elapsed)+" seconds\n")
            sum+=elapsed
            correctness = fdcc.checkCorrectness(image,detected)
            if correctness[0] == 1: writeFile.write("Correctly processed\n"); numCorrect+=1
            elif correctness[0]==0:
                errorType = correctness[1]
                if errorType==0: writeFile.write("Incorrectly processed, false positive\n")
                elif errorType==1: writeFile.write("Incorrectly processed, false negative\n")
                incorrectlyProcessedImages.add((image,errorType))
            else: writeFile.write("Fire detection accuracy unknown\n")
            writeFile.write("-------\n")
        imageArrOffset+=numChildren
        avg=sum/numChildren
        writeFile.write("Average time for {} images: ".format(numChildren)+("%.7f"%avg)+"\n")
    writeFile.write("--------------------------------------------------------\n")
    writeFile.write("--------------------------------------------------------\n")

end = time.time()
writeFile.write("--------------------------------------------------------\n")
numAllDetections = numIterationsPerImage*numImages
incorrectlyProcessedImages = sorted(incorrectlyProcessedImages)

#not a completely correct time cause there is overhead of checking processing accuracy that would not happen in a real situation
if not drawBoxes: writeFile.write("Total time to process all {} images: ".format(numAllDetections)+("%.7f" % (end-start))+" seconds\n")
else: writeFile.write("Total time to process all {} images (while drawing boxes): ".format(numAllDetections)+("%.7f" % (end-start))+" seconds\n")

writeFile.write("{} incorrectly processed images:\n".format(len(incorrectlyProcessedImages)))
numFalseNeg=0
for image in incorrectlyProcessedImages: 
    writeFile.write(image[0])
    if image[1]==0: writeFile.write(", false positive\n")
    else: 
        writeFile.write(", false negative\n")
        numFalseNeg+=1
writeFile.write("Accuracy: {}/{} = ".format(numCorrect,numAllDetections)+("%.0f"%((numCorrect/numAllDetections)*100))+"%, ") 
writeFile.write("Number of fires missed (number of false negatives): {}/{} = ".format(numFalseNeg,numAllDetections)+("%.0f"%((numFalseNeg/numAllDetections)*100))+"%\n") 
writeFile.close()