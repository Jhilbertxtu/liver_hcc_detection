import dicom
import cv2
from PIL.Image import fromarray
p1 = dicom.read_file("dicom_images/000009.dcm")

#print "Thickness : %f" % p1.SliceThickness
print p1.WindowWidth
print p1.WindowCenter
img = fromarray(p1.pixel_array)
if img.mode != 'RGB':
    img = img.convert('RGB')
img.save("w0.jpg")
p1.WindowWidth = ['425','55']
#p1.WindowWidth = ['10000','10000']
#help(p1.WindowWidth)
#print p1.WindowWidth
img = fromarray(p1.pixel_array)
#scaled_img = cv2.convertScaleAbs(img-window_center, alpha=(255.0 /window_width))

if img.mode != 'RGB':
    img = img.convert('RGB')
img.save("w1.jpg")
