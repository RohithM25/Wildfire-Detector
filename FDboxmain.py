import sys
import FDboundingbox as fdb
import FDparams as fdparams

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

initHeight=500
initWidth=1000

scaledHeight = (int)(initHeight*scale)
scaledWidth = (int)(initWidth*scale)

if percentageOrSet == 0:
    windowHeight = (int)(winHeight*scaledHeight)
    windowWidth = (int)(winWidth*scaledWidth)
else:
    windowWidth = winWidth
    windowHeight = winHeight

stepHeight = (int)(windowHeight*stepHeightp)
stepWidth = (int)(windowWidth*stepWidthp)

pixelThreshold = (int)((scaledHeight*scaledWidth)/10000) #0.01% of the image

params = fdparams.FDparams(None,scale,scaledHeight,scaledWidth,windowWidth,windowHeight,stepWidth,stepHeight,pixelThreshold)
imageProcessor = fdb.FDboundingbox(params)

image = "sf6-resized1000,500.jpeg"
imageProcessor.processImage(image)