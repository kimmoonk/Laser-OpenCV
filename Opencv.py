import cv2
import numpy as np
from matplotlib import pyplot as plt

src = cv2.imread("Image/geese.jpg", cv2.IMREAD_COLOR)

gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

sobel = cv2.Sobel(gray, cv2.CV_8U, 1, 0, 3)
laplacian = cv2.Laplacian(gray, cv2.CV_8U, ksize=3)
canny = cv2.Canny(src, 100, 255)



ret, thresh1 = cv2.threshold(gray,127,255, cv2.THRESH_BINARY)
ret, thresh2 = cv2.threshold(gray,127,255, cv2.THRESH_BINARY_INV)
ret, thresh3 = cv2.threshold(gray,127,255, cv2.THRESH_TRUNC)
ret, thresh4 = cv2.threshold(gray,127,255, cv2.THRESH_TOZERO)
ret, thresh5 = cv2.threshold(gray,127,255, cv2.THRESH_TOZERO_INV)

cv2.imshow("thresh1",thresh1)
#cv2.imshow("thresh2",thresh2)
#cv2.imshow("thresh3",thresh3)
#cv2.imshow("thresh4",thresh4)
#cv2.imshow("thresh5",thresh5)

# cv2.imshow("sobel", sobel)
# cv2.imshow("laplacian", laplacian)
#cv2.imshow("canny", canny)
cv2.waitKey()
cv2.destroyAllWindows()

# ret, dst = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)

# contours, hierarchy = cv2.findContours(dst, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)


# cv2.imshow("dst", dst)
# cv2.waitKey()
# cv2.destroyAllWindows()

# gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
# ret, dst = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)