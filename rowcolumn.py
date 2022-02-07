import numpy as np
import matplotlib.pyplot as plt
import cv2

img = np.zeros((5,5))  # initialize empty image as numpy array
img[3,3] = 1  # assign 1 to the pixel of row 0 and column 2

M = cv2.moments(img)  # calculate moments of binary image
cX = int(M["m10"] / M["m00"])  # calculate x coordinate of centroid
cY = int(M["m01"] / M["m00"])  # calculate y coordinate of centroid

img2 = np.zeros((5,5))  # initialize another empty image
img2[cX,cY] = 1  # assign 1 to the pixel with x = cX and y = cY

img3 = np.zeros((5,5))  # initialize another empty image
img3[cY,cX] = 1  # invert x and y

plt.figure()
plt.subplots_adjust(wspace=0.4)  # add space between subplots
plt.subplot(131), plt.imshow(img, cmap = "gray"), plt.title("With [rows,cols]")
plt.subplot(132), plt.imshow(img2, cmap = "gray"), plt.title("With [x,y]")
plt.subplot(133), plt.imshow(img3, cmap= "gray"), plt.title("With [y,x]"), plt.xlabel('x'), plt.ylabel('y')



plt.show()