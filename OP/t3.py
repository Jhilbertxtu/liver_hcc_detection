import cv2
import glob
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
opnames = glob.glob('OP/*.jpg')
opnames = sorted(opnames)
for i in range(0, len(opnames)):
	#g = cv2.imread('img-'+str(i)+'.jpg',cv2.IMREAD_GRAYSCALE)
	g = cv2.imread(opnames[i],cv2.IMREAD_GRAYSCALE)
	c = cv2.applyColorMap(g, cv2.COLORMAP_JET)
	c2 = cv2.applyColorMap(c, cv2.COLORMAP_HSV)
	cv2.imwrite('JHS/img-'+str(i).zfill(8)+'.jpg',c2)
