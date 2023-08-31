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
#cv2.imwrite(f"./scale={scale}-{fn}",resized)
cv2.imshow("resized", resized)
cv2.waitKey(0)
ob = resized[125:250,300:700]
cv2.imshow("resized out of bounds", ob)
cv2.waitKey(0)
print(f"ob size:{len(ob)},{len(ob[0])}")
#seems whatever's out of bounds is just automatically excluded

cv2.destroyAllWindows()