import time
import sys
import FDprocess as fdp

#scale, window, and step paramaters. these parameters are taken in as command line arguments
#values should be > 0. should also be <= 1 for reasonable applications, but technically doesn't have to be
scale = float(sys.argv[1])
winWidthp = float(sys.argv[2]) #percentage of the frame width that window width should be
winHeightp = float(sys.argv[3]) #percentage of the frame height that window height should be
stepWidthp = float(sys.argv[4]) #percentage of the window width that should be stepped over when moving to the next window
stepHeightp = float(sys.argv[5]) #percentage of the window height that should be stepped over when moving to the next row of windows
images = ["sf6.jpeg", "sf6-no fire.jpg", "sf6-no smoke.jpg", "sf6-no water.jpg", "sf6-very small fire.jpg"]

imageProcessor = fdp.FDProcess(scale,winWidthp,winHeightp,stepWidthp,stepHeightp)

#apparently should use python 'timeit' module to measure program execution duration
start = time.time()
for fn in images:
    numIterations=5
    sum=0
    for i in range(numIterations): #do each image five times, print each time and then print the average
        start2 = time.time()
        imageProcessor.processImage(fn)
        end2 = time.time()
        elapsed = end2-start2
        print(("%.4f" % elapsed)+" seconds\n-------")
        sum+=elapsed
    avg=sum/numIterations
    print(f"Average time for {numIterations} iterations: "+("%.7f"%avg))
    print("-------------------------------------------------")
end = time.time()
print("Total time to process all images: "+("%.7f" % (end-start))+" seconds")
