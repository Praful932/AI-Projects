import cv2
import numpy as np


img = cv2.imread('img2.ppm')
IMG_WIDTH = 30
IMG_HEIGHT = 30

print(img.shape)
img2 = cv2.resize(img,(IMG_WIDTH,IMG_HEIGHT))
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()