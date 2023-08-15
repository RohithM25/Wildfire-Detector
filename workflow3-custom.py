# ideally could have a program where I could load an image and use cursor to hover over each pixel to tell me what color values it has
#     could also zoom in and out on the image to see more detail, gives option to see in BGR, RGB, HSV etc
#     that could also be put on my github
# test different images with and without fires

import cv2
import numpy as np

fn = "sf6.jpg"
frame = cv2.imread('./input images/'+fn)
#print("height: "+str(len(frame))+", width: "+str(len(frame[0])))

#should set up some rules for what size the window can be based on the initial resizing of the frame
frameWidth=1000
frameHeight=500
resized = cv2.resize(frame, (frameWidth,frameHeight))
#highlighted = resized #this image will be used to highlight the windows of the image where detection occurs
#cv2.imwrite("./sf6-resized1000,500.jpeg",resized)

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
#sliding window, image has total of 500,000 pixels. window size = 1250 pixels. so image has at least 400 windows
windowHeight = 25
windowWidth = 50
heightStep=25
widthStep=25
counter=0
for y in range(0,frameHeight,heightStep):
    for x in range(0,frameWidth,widthStep):
        window = resized[y:(y+windowHeight),x:(x+windowWidth)]
        mask = cv2.inRange(window, lower, upper)
        numRed = cv2.countNonZero(mask)
        if numRed>50:
            print(f"fire detected, numRed={numRed}, range=[{y}:{y+windowHeight},{x}:{x+windowHeight}]")
            # cv2.imshow("window",window)
            # cv2.waitKey(0)
            # cv2.imshow("masked",mask)
            # cv2.waitKey(0)
        counter+=1

# #numWinsProcessed = (frameWidth*frameHeight)/((windowWidth*windowHeight)/(widthStep*heightStep)) #this calculation isn't correct
print(f"number of windows processed: {counter}")

# mask = cv2.inRange(resized, lower, upper)
# numGrey = cv2.countNonZero(mask)

#creating string for write file
wstring = "["
for x in range(0,3):
    wstring+=(str(boundaries[0][x])+",")
wstring+="]"
wstring2 = "["
for x in range(0,3):
    wstring2+=(str(boundaries[1][x])+",")
wstring2+="]"

#cv2.imwrite("./masks/"+wstring+wstring2+fn,mask)

#print("numGrey="+str(numGrey)+", boundaries="+wstring+wstring2)
#print("numRed="+str(numRed)+", boundaries="+wstring+wstring2)

cv2.destroyAllWindows()