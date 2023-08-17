# ideally could have a program where I could load an image and use cursor to hover over each pixel to tell me what color values it has
#     could also zoom in and out on the image to see more detail, gives option to see in BGR, RGB, HSV etc
#     that could also be put on my github
# test different images with and without fires

import cv2
import numpy as np

def ParamsFit():
    
    return False

#scale and window paramaters
#values should be > 0. should also be <= 1 for reasonable applications, but technically doesn't have to be
    #could set up a scale-window system where only certain ratios are allowed
    #OR
    #set up where you don't decide the exact size of the window, you decide its size relative to the whole image
    #ultimately should be able to be set to whatever, but to start off can be set to a discrete range of values
scale = 0.1
winWidthp = 0.5 #percentage of the frame width that window width should be
winHeightp = 0.5 #percentage of the frame height that window height should be
stepWidthp = 1 #percentage of the window width that should be stepped over when moving to the next window
stepHeightp = 1 #percentage of the window height that should be stepped over when moving to the next row of windows


fn = "sf6.jpeg"
frame = cv2.imread('./input images/'+fn)
#print("height: "+str(len(frame))+", width: "+str(len(frame[0])))

#could scale image based on the window parameters that are passed in, but then not a "true" scale
resized = cv2.resize(frame, None, fx=scale, fy=scale)
frameHeight = len(resized)
frameWidth = len(resized[0])
print(f"height:{frameHeight}, width:{frameWidth}")

# #cropping image to get just the fire
# cropped = resized[200:225,675:715] #the resized image is a 25x50x3 3D array
# cv2.imwrite("./sf6-croppedsmoke.jpeg",cropped)

# #writing all the color values to a txt file
# wfile = open("sf6-croppedsmokecolors.txt",'w')
# for row in cropped:
#     for column in range(len(row)):
#         wfile.write(str(row[column]))
#     wfile.write("\n")

boundaries = [[0,50,191],[160,220,255]] #fire boundaries
# boundaries = [[80,80,80],[130,130,130]] #smoke boundaries

lower = np.array(boundaries[0])
upper = np.array(boundaries[1])

#blurring the image before processing it may actually help in detection
windowHeight = (int)(winHeightp*frameHeight)
windowWidth = (int)(winWidthp*frameWidth)
stepHeight = (int)(windowHeight*stepHeightp)
stepWidth = (int)(windowWidth*stepWidthp)
counter=0
print(f"winHeight: {windowHeight}, windowWidth: {windowWidth}, stepHeight: {stepHeight}, stepWidth: {stepWidth}")
red_threshold = (int)((frameHeight*frameWidth)/10000) #0.01% of the image
#need to make sure all pixels are being processed
for y in range(0,frameHeight,stepHeight):
    for x in range(0,frameWidth,stepWidth):
        window = resized[y:(y+windowHeight),x:(x+windowWidth)]
        mask = cv2.inRange(window, lower, upper)
        numRed = cv2.countNonZero(mask)
        if numRed>red_threshold:
            print(f"fire detected, numRed={numRed}, range=[{y}:{y+windowHeight},{x}:{x+windowHeight}]")
            # cv2.imshow("window",window)
            # cv2.waitKey(0)
            # cv2.imshow("masked",mask)
            # cv2.waitKey(0)
        counter+=1

# #numWinsProcessed = (frameWidth*frameHeight)/((windowWidth*windowHeight)/(stepWidth*stepHeight)) #this calculation isn't correct
print(f"number of windows processed: {counter}")

# mask = cv2.inRange(resized, lower, upper)
# numGrey = cv2.countNonZero(mask)

# #creating string for write file
# wstring = "["
# for x in range(0,3):
#     wstring+=(str(boundaries[0][x])+",")
# wstring+="]"
# wstring2 = "["
# for x in range(0,3):
#     wstring2+=(str(boundaries[1][x])+",")
# wstring2+="]"

#cv2.imwrite("./masks/"+wstring+wstring2+fn,mask)

#print("numGrey="+str(numGrey)+", boundaries="+wstring+wstring2)
#print("numRed="+str(numRed)+", boundaries="+wstring+wstring2)

cv2.destroyAllWindows()