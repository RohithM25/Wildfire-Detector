# ideally could have a program where I could load an image and use cursor to hover over each pixel to tell me what color values it has
#     could also zoom in and out on the image to see more detail, gives option to see in BGR, RGB, HSV etc
#     that could also be put on my github
# test different images with and without fires

#this version lets the windows go out of bounds, but after all pixels in a row/column have been captured, it doesn't go further out of bounds

import cv2
import numpy as np

#scale and window paramaters
#values should be > 0. should also be <= 1 for reasonable applications, but technically doesn't have to be
scale = 0.1
winWidthp = 0.25 #percentage of the frame width that window width should be
winHeightp = 0.25 #percentage of the frame height that window height should be
stepWidthp = 1 #percentage of the window width that should be stepped over when moving to the next window
stepHeightp = 1 #percentage of the window height that should be stepped over when moving to the next row of windows

fn = "sf6.jpeg"
frame = cv2.imread('./input images/'+fn)
#print("frame height: "+str(len(frame))+", frame width: "+str(len(frame[0])))

resized = cv2.resize(frame, None, fx=scale, fy=scale)
frameHeight = len(resized)
frameWidth = len(resized[0])
print(f"scaled height: {frameHeight}, scaled width:{frameWidth}")

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

#checking if the window/step sizes fit the scaled image
heightRemainder = ((frameHeight%windowHeight)%stepHeight)
widthRemainder = ((frameWidth%windowWidth)%stepWidth)
print(f"heightRemainder: {heightRemainder}, widhtRemainder: {widthRemainder}")
#if there are remainders, for loops should be modified in most efficient way possible, 
# think of how would do it in C, try to translate to python
#for y in range(0,frameHeight,stepHeight):
#   for x in range(0,frameWidth,stepWidth): 
#       process(window)

numWindowsProcessed=0 #this can be deleted, doesn't affect program functionality
print(f"winHeight: {windowHeight}, windowWidth: {windowWidth}, stepHeight: {stepHeight}, stepWidth: {stepWidth}")
red_threshold = (int)((frameHeight*frameWidth)/10000) #0.01% of the image
print(f"pixel threshold: {red_threshold}")

# loop has conditions that checks whether the window has gone out of bounds. if so, it will break the loop on the next iteration
heightOutOfBounds = False #boolean to check if window height is out of bounds
for y in range(0,frameHeight,stepHeight):
    if heightOutOfBounds: break
    widthOutOfBounds = False #boolean to check if window width is out of bounds
    for x in range(0,frameWidth,stepWidth):
        if widthOutOfBounds: break
        window = resized[y:(y+windowHeight),x:(x+windowWidth)]
        print(f"height: {len(window)}, width: {len(window[0])}: [{y}:{y+windowHeight},{x}:{x+windowWidth}]")
        mask = cv2.inRange(window, lower, upper)
        numRed = cv2.countNonZero(mask)
        if numRed>red_threshold:
            print(f"fire detected, numRed={numRed}, range=[{y}:{y+windowHeight},{x}:{x+windowWidth}]")
            # cv2.imshow("window",window)
            # cv2.waitKey(0)
            # cv2.imshow("masked",mask)
            # cv2.waitKey(0)
        if x+windowWidth>frameWidth: widthOutOfBounds=True
        numWindowsProcessed+=1
    if y+windowHeight>frameHeight: heightOutOfBounds=True

# #numWinsProcessed = (frameWidth*frameHeight)/((windowWidth*windowHeight)/(stepWidth*stepHeight)) #this calculation isn't correct
print(f"number of windows processed: {numWindowsProcessed}")

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