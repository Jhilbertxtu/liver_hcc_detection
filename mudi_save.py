import mudicom

s = mudicom.load('dicom_images/000000.dcm')

s.read()
#s.validate()

i = s.image

i.numpy

i.save_as_plt('test_mu.jpg')
