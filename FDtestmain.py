import time
import sys
import FDprocess as fdp

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
images = ["sf6-resized1000,500.jpeg", "sf6-no fire.jpg", "sf6-no smoke.jpg", "sf6-no water.jpg", "sf6-very small fire.jpg"]

imageProcessor = fdp.FDProcess(scale,percentageOrSet,winWidth,winHeight,stepWidthp,stepHeightp)

#apparently should use python 'timeit' module to measure program execution duration
start = time.time()
for fn in images:
    numIterationsPerImage=5
    sum=0
    for i in range(numIterationsPerImage): #do each image five times, print each time and then print the average
        start2 = time.time()
        imageProcessor.processImage(fn)
        end2 = time.time()
        elapsed = end2-start2
        print(("%.7f" % elapsed)+" seconds\n-------")
        sum+=elapsed
    avg=sum/numIterationsPerImage
    print(f"Average time for {numIterationsPerImage} iterations: "+("%.7f"%avg))
    print("-------------------------------------------------")
end = time.time()
print(f"Total time to process all {numIterationsPerImage*len(images)} images: "+("%.7f" % (end-start))+" seconds")
