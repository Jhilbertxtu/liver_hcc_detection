from __future__ import division
import cv2
#to show the image
from matplotlib import pyplot as plt
import numpy as np
from math import cos, sin
import glob
green = (0, 255, 0)

def show(image):
    # Figure size in inches
    plt.figure(figsize=(10, 10))

    # Show image, with nearest neighbour interpolation
    plt.imshow(image, interpolation='nearest')

def overlay_mask(mask, image):
    #make the mask rgb
    rgb_mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
    #calculates the weightes sum of two arrays. in our case image arrays
    #input, how much to weight each. 
    #optional depth value set to 0 no need
    img = cv2.addWeighted(rgb_mask, 0, image, 0.5, 0)
    return img

def find_biggest_contour(image):
    image = image.copy()
    image, contours, hierarchy = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    mask = np.zeros(image.shape, np.uint8)
    return contours, mask

def circle_contour(image, contour):
    image_with_contour = image.copy()
    cv2.drawContours(image_with_contour, contour, -1, (255,0,0), 5)
    '''
    #easy function
    ellipse = cv2.fitEllipse(contour)
    #add it
    cv2.ellipse(image_with_contour, ellipse, green, 2, cv2.LINE_AA)
    '''
    return image_with_contour

def find_tumor(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    max_dimension = max(image.shape)
    scale = 700/max_dimension
    image = cv2.resize(image, None, fx=scale, fy=scale)
    
    #we want to eliminate noise from our image. clean. smooth colors without
    #dots
    # Blurs an image using a Gaussian filter. input, kernel size, how much to filter, empty)
    image_blur = cv2.GaussianBlur(image, (7, 7), 0)
    #just want to focus on color, segmentation
    image_blur_hsv = cv2.cvtColor(image_blur, cv2.COLOR_RGB2HSV)
    
    min_color = np.array([30, 100, 80])
    max_color = np.array([110, 256, 256])
    mask1 = cv2.inRange(image_blur_hsv, min_color, max_color)

    min_color2 = np.array([170, 100, 80])
    max_color2 = np.array([180, 256, 256])
    mask2 = cv2.inRange(image_blur_hsv, min_color2, max_color2)
    
    # Combine masks
    mask = mask1 + mask2
    
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
    mask_closed = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    #erosion followed by dilation. It is useful in removing noise
    mask_clean = cv2.morphologyEx(mask_closed, cv2.MORPH_OPEN, kernel)
    big_tumor_contour, mask_tumors = find_biggest_contour(mask_clean)
    
    overlay = image
    circled = circle_contour(overlay, big_tumor_contour)
    #show(circled)
    bgr = cv2.cvtColor(circled, cv2.COLOR_RGB2BGR)
    
    return bgr

liver = glob.glob('Liver_OP/*.jpg')
liver = sorted(liver)

for i in range(0, len(liver)):
	img = cv2.imread(liver[i])
	result = find_tumor(img)
	cv2.imwrite('Tumor_OP/tumor-'+str(i).zfill(8)+'.jpg',result)
