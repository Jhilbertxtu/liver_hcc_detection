import cv2
'''
g = cv2.imread('img-12.jpg',cv2.IMREAD_GRAYSCALE)
c = cv2.applyColorMap(g, cv2.COLORMAP_JET)
c2 = cv2.applyColorMap(c, cv2.COLORMAP_HSV)
cv2.imwrite('JHS/img-12.jpg',c2)

g = cv2.imread('img-10.jpg',cv2.IMREAD_GRAYSCALE)
c = cv2.applyColorMap(g, cv2.COLORMAP_JET)
c2 = cv2.applyColorMap(c, cv2.COLORMAP_HSV)
cv2.imwrite('JHS/img-10.jpg',c2)
'''

g = cv2.imread('../OP_OG/000040..jpg',cv2.IMREAD_GRAYSCALE)
c = cv2.applyColorMap(g, cv2.COLORMAP_JET)
c2 = cv2.applyColorMap(c, cv2.COLORMAP_HSV)
cv2.imwrite('te.jpg',c2)
