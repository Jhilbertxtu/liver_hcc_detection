import cv2

bgfb = cv2.createBackgroundSubtractorMOG2(varThreshold=0)
#bgfb = cv2.bgsegm.createBackgroundSubtractorGMG()

i = cv2.imread('OP/img-6.jpg')
#print i
fgmask = bgfb.apply(i)

cv2.imwrite('f.jpg',fgmask)
