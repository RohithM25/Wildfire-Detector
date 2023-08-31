import cv2
import numpy as np

#scale, window, and step paramaters
#values should be > 0. should also be <= 1 for reasonable applications, but technically doesn't have to be
scale = 0.1
winWidthp = 0.25 #percentage of the frame width that window width should be
winHeightp = 0.25 #percentage of the frame height that window height should be
stepWidthp = 1 #percentage of the window width that should be stepped over when moving to the next window
stepHeightp = 1 #percentage of the window height that should be stepped over when moving to the next row of windows

fn = "sf6-no water.jpg"
frame = cv2.imread('./input images/'+fn)
print("frame height: "+str(len(frame))+", frame width: "+str(len(frame[0])))

#resizing frame based on scale
resized = cv2.resize(frame, None, fx=scale, fy=scale)
frameHeight = len(resized)
frameWidth = len(resized[0])
print(f"scaled height: {frameHeight}, scaled width:{frameWidth}")
# cv2.imwrite(f"./scaled images/scale={scale}-{fn}",resized)

# #writing all the color values to a txt file
# wfile = open("sf6-croppedsmokecolors.txt",'w')
# for row in cropped:
#     for column in range(len(row)):
#         wfile.write(str(row[column]))
#     wfile.write("\n")

boundaries = [[80,80,80],[130,130,130]] #smoke boundaries
lower = np.array(boundaries[0])
upper = np.array(boundaries[1])
# mask = cv2.inRange(resized, lower, upper)
# cv2.imwrite(f"./masks/{boundaries}{fn}",mask)

windowHeight = (int)(winHeightp*frameHeight)
windowWidth = (int)(winWidthp*frameWidth)
stepHeight = (int)(windowHeight*stepHeightp)
stepWidth = (int)(windowWidth*stepWidthp)

# #checking if the window/step sizes fit the scaled image, this block can be deleted, doesn't affect functionality
# heightRemainder = ((frameHeight%windowHeight)%stepHeight)
# widthRemainder = ((frameWidth%windowWidth)%stepWidth)
# print(f"heightRemainder: {heightRemainder}, widhtRemainder: {widthRemainder}")

numWindowsProcessed=0 #this can be deleted, doesn't affect program functionality
print(f"winHeight: {windowHeight}, windowWidth: {windowWidth}, stepHeight: {stepHeight}, stepWidth: {stepWidth}")
pixelThreshold = (int)((frameHeight*frameWidth)/100) #0.01% of the image
print(f"pixel threshold: {pixelThreshold}")

# nested loop reads image left to right and top to bottom
heightOutOfBounds = False
for y in range(0,frameHeight,stepHeight):
    yWinLen = y+windowHeight
    yLenNxtWin = yWinLen+stepHeight #height along frame of next window
    if yLenNxtWin>frameHeight: #checking if the window height is out of bounds
        yWinLen+=(windowHeight-(yLenNxtWin-frameHeight)) #adding on to the current window the portion of the next window that's in bounds
        heightOutOfBounds = True
    widthOutOfBounds = False
    for x in range(0,frameWidth,stepWidth):
        xWinLen = x+windowWidth
        xLenNxtWin = xWinLen+stepWidth
        if xLenNxtWin>frameWidth: 
            xWinLen+=(windowWidth-(xLenNxtWin-frameWidth))
            widthOutOfBounds = True
        window = resized[y:(yWinLen),x:(xWinLen)]
        print(f"height: {len(window)}, width: {len(window[0])}: [{y}:{yWinLen},{x}:{xWinLen}]")
        mask = cv2.inRange(window, lower, upper)
        numDetected = cv2.countNonZero(mask)
        if numDetected>pixelThreshold:
            print(f"smoke detected, numPixels={numDetected}, range=[{y}:{yWinLen},{x}:{xWinLen}]")
            # cv2.imshow("window",window)
            # cv2.waitKey(0)
        numWindowsProcessed+=1
        if widthOutOfBounds: break
    if heightOutOfBounds: break

print(f"number of windows processed: {numWindowsProcessed}")

#print("numGrey="+str(numGrey)+", boundaries="+wstring+wstring2)
#print("numDetected="+str(numDetected)+", boundaries="+wstring+wstring2)

cv2.destroyAllWindows()