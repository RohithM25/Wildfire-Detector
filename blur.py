import cv2
import numpy as np

fn = "sf6.jpeg"
frame = cv2.imread('./input images/'+fn)
print("height: "+str(len(frame))+", width: "+str(len(frame[0])))

# frameWidth=1000
# frameHeight=500
scale = 0.1
resized = cv2.resize(frame, None, fx=scale, fy=scale)
print("height: "+str(len(resized))+", width: "+str(len(resized[0])))
cv2.imwrite(f"./scale={scale}-{fn}",resized)
#cv2.imshow("resized", resized)
cv2.waitKey(0)

cv2.destroyAllWindows()