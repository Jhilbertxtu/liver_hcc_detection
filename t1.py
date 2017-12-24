import dicom
import cv2
from PIL.Image import fromarray
p1 = dicom.read_file("dicom_images/000009.dcm")
p2 = dicom.read_file("OP2/000009.dcm")
p3 = dicom.read_file("OP3/000009.dcm")
p4 = dicom.read_file("HARD_CASE_NW/000009.dcm")
p5 = dicom.read_file("OP5/000009.dcm")
#print "Thickness : %f" % p1.SliceThickness
#print p1.WindowWidth
#print p1.WindowCenter
print dir(p1)
print p1.Manufacturer
print p1.ManufacturerModelName
print p2.Manufacturer
print p3.Manufacturer
print p4.Manufacturer
#img = fromarray(p1.pixel_array)
#if img.mode != 'RGB':
#    img = img.convert('RGB')
#img.save("w0.jpg")
#p1.WindowWidth = ['425','55']
#p1.WindowWidth = ['10000','10000']
#help(p1.WindowWidth)
#print p1.WindowWidth
#img = fromarray(p1.pixel_array)
#scaled_img = cv2.convertScaleAbs(img-window_center, alpha=(255.0 /window_width))
#
#if img.mode != 'RGB':
#    img = img.convert('RGB')
#img.save("w1.jpg")
