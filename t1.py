import dicom

p1 = dicom.read_file("dicom_images/000000.dcm")

#print "Thickness : %f" % p1.SliceThickness
print p1.dir('dow')
