import time
import sys
import FDprocess as fdp
import FDparams as fdparams
import FDcorrectnesschecker as fdcc

#VERY IMPORTANT THAT THESE CONSTANTS ARE SET CORRECTLY OTHERWISE PROGRAM WON'T WORK PROPERLY
initHeight=500
initWidth=1000

#scale, window, and step paramaters. these parameters are taken in as command line arguments
#values should be > 0. should also be <= 1 for reasonable applications, but technically doesn't have to be
scale = float(sys.argv[1])
percentageOrSet = float(sys.argv[2]) #0|1 flag that checks whether to have a set window size or a percentage. 0 is percentage, 1 is set

winWidth = None
winHeight = None
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

outputFilename = str(scale)+"-"+("%d" % percentageOrSet)+"-{}-{}-{}-{}.txt".format(winWidth,winHeight,stepWidthp,stepHeightp)
writeFile = open("./output/"+outputFilename,'w')
writeFile.write("original image height: {}, original image width: {}\n".format(initHeight,initWidth))

scaledHeight = (int)(initHeight*scale)
scaledWidth = (int)(initWidth*scale)
writeFile.write("scaled height: {}, scaled width: {}\n".format(scaledHeight,scaledWidth))

if percentageOrSet == 0:
    windowHeight = (int)(winHeight*scaledHeight)
    windowWidth = (int)(winWidth*scaledWidth)
else:
    windowWidth = winWidth
    windowHeight = winHeight
writeFile.write("windowHeight: {}, windowWidth: {}\n".format(windowHeight,windowWidth))

stepHeight = (int)(windowHeight*stepHeightp)
stepWidth = (int)(windowWidth*stepWidthp)
writeFile.write("stepHeight: {}, stepWidth: {}\n".format(stepHeight,stepWidth))

pixelThreshold = (int)((scaledHeight*scaledWidth)/10000) #0.01% of the image
writeFile.write("pixel threshold: {}\n".format(pixelThreshold))

numCorrect = 0

writeFile.write("--------------------------------------------------------\n")
writeFile.write("--------------------------------------------------------\n")

params = fdparams.FDparams(writeFile,scale,scaledHeight,scaledWidth,windowWidth,windowHeight,stepWidth,stepHeight,pixelThreshold)
imageProcessor = fdp.FDProcess(params)

images = ["sf6-resized1000,500.jpeg", "sf6.2.jpg", "sf6.3.jpg", "sf6.5.jpg", "sf6-no fire.jpg", "sf6-no smoke.jpg", "sf6-no water.jpg", "sf6-very small fire.jpg"]
# images = ["hazmonDB/hazmonDB1.jpeg","hazmonDB/hazmonDB2.jpeg","hazmonDB/hazmonDB3.jpeg","hazmonDB/hazmonDB4.jpeg","hazmonDB/hazmonDB5.jpeg","hazmonDB/hazmonDB6.jpeg","hazmonDB/hazmonDB7.jpeg",
#           "hazmonDB/hazmonDB8.jpeg","hazmonDB/hazmonDB9.jpeg","hazmonDB/hazmonDB10.jpeg","hazmonDB/hazmonDB11.jpeg","hazmonDB/hazmonDB12.jpeg",]
numImages = len(images)
numIterationsPerImage=100
#apparently should use python 'timeit' module to measure program execution duration
start = time.time()
for i in range(numIterationsPerImage):
    sum=0
    for j in range(numImages): #do each image five times, print each time and then print the average
        image = images[j]
        start2 = time.time()
        detected = imageProcessor.processImage(image)
        end2 = time.time()
        elapsed = end2-start2
        writeFile.write(("%.7f" % elapsed)+" seconds\n")
        sum+=elapsed
        correctness = fdcc.checkCorrectness(image,detected)
        if correctness == 1: writeFile.write("Correctly processed\n"); numCorrect+=1
        elif correctness == 0: writeFile.write("Incorrectly processsed\n")
        else: writeFile.write("Fire detection accuracy unknown\n")
        writeFile.write("-------\n")
    avg=sum/numImages
    writeFile.write("Average time for {} images: ".format(numImages)+("%.7f"%avg)+"\n")
    writeFile.write("-------------------------------------------------\n")
end = time.time()
writeFile.write("--------------------------------------------------------\n")
numAllDetections = numIterationsPerImage*numImages

#not a completely correct time cause there is overhead of checking processing accuracy that would not happen in a real situation
writeFile.write("Total time to process all {} images: ".format(numAllDetections)+("%.7f" % (end-start))+" seconds\n")

writeFile.write("Accuracy: {}/{} = ".format(numCorrect,numAllDetections)+("%.0f"%((numCorrect/numAllDetections)*100))+"%\n") 
writeFile.close()