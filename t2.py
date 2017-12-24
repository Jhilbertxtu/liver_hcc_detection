import numpy as np
import dicom
import os
import matplotlib.pyplot as plt
from glob import glob
import scipy.ndimage
from skimage import morphology
from skimage import measure
from skimage.transform import resize
from plotly.graph_objs import *
from PIL.Image import fromarray
import cv2
import glob
import mudicom

def load_scan(path):
    slices = [dicom.read_file(path + '/' + s) for s in os.listdir(path)]
    slices.sort(key = lambda x: int(x.InstanceNumber))
    try:
        slice_thickness = np.abs(slices[0].ImagePositionPatient[2] - slices[1].ImagePositionPatient[2])
    except:
        slice_thickness = np.abs(slices[0].SliceLocation - slices[1].SliceLocation)
        
    for s in slices:
        s.SliceThickness = slice_thickness
       	s.WindowWidth = ['00120','00080']
    return slices

def get_pixels_hu(scans):
    image = np.stack([s.pixel_array for s in scans])
    # Convert to int16 (from sometimes int16), 
    # values should always be lower than <32k
    image = image.astype(np.int16)

    image[image == -2000] = 0
    
    # Convert to Hounsfield units (HU)
    intercept = scans[0].RescaleIntercept
    slope = scans[0].RescaleSlope
    
    if slope != 1:
        image = slope * image.astype(np.float64)
        image = image.astype(np.int16)
        
    image += np.int16(intercept)
    
    return np.array(image, dtype=np.int16)

def sample_stack(stack, rows=6, cols=6, start_with=0, show_every=2):
    fig,ax = plt.subplots(rows,cols,figsize=[12,12])
    
    for i in range(rows*cols):
	try:
        	ind = start_with + i*show_every
        	ax[int(i/rows),int(i % rows)].set_title('slice %d' % ind)
        	ax[int(i/rows),int(i % rows)].imshow(stack[ind],cmap='gray')
        	ax[int(i/rows),int(i % rows)].axis('off')
	except IndexError:
		break
    plt.show()

def resample(image, scan, new_spacing=[1,1,1]):
    # Determine current pixel spacing
    spacing = map(float, ([scan[0].SliceThickness] + scan[0].PixelSpacing))
    spacing = np.array(list(spacing))

    resize_factor = spacing / new_spacing
    new_real_shape = image.shape * resize_factor
    new_shape = np.round(new_real_shape)
    real_resize_factor = new_shape / image.shape
    new_spacing = spacing / real_resize_factor
    
    image = scipy.ndimage.interpolation.zoom(image, real_resize_factor)
    
    return image, new_spacing

id=0
patient = load_scan("dicom_images/")
imgs = get_pixels_hu(patient)
np.save("OP/" + "fullimages_%d.npy" % (id), imgs)

file_used="OP/"+"fullimages_%d.npy" % id
imgs_to_process = np.load(file_used).astype(np.float64) 

sample_stack(imgs_to_process)

imgs_after_resamp, spacing = resample(imgs_to_process, patient, [1,1,1])

og_names = glob.glob('dicom_images/*.dcm')

for n in og_names:
	og_img = mudicom.load(n)
	og_img.read()
	i = og_img.image
	i.save_as_plt('OP_OG/'+n.split('/')[1][:-3]+".jpg")
for i in range(0,len(imgs_after_resamp)):
	img = imgs_after_resamp[i]
	cv2.imwrite('OP/img-'+str(i).zfill(8)+'.jpg',img)
	im = fromarray(img,'RGB')
	i = i + 1

