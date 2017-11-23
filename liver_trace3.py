from __future__ import division
import cv2
#to show the image
from matplotlib import pyplot as plt
import numpy as np
from math import cos, sin
from PIL import Image
import glob
green = (0, 255, 0)

def show(image):
    plt.figure(figsize=(10, 10))
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
    #Copy
    image = image.copy()
    #input, gives all the contours, contour approximation compresses horizontal, 
    #vertical, and diagonal segments and leaves only their end points. For example, 
    #an up-right rectangular contour is encoded with 4 points.
    #Optional output vector, containing information about the image topology. 
    #It has as many elements as the number of contours.
    #we dont need it
    image, contours, hierarchy = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    #Isolate largest contour
    
    contour_sizes = [(cv2.contourArea(contour), contour) for contour in contours]
    biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]
    
    mask = np.zeros(image.shape, np.uint8)
    
    cv2.drawContours(mask, [biggest_contour], -1, 255, -1)
    return biggest_contour, mask
    
    #return contours, mask

def circle_contour(image, contour):
    #Bounding ellipse
    image_with_contour = image.copy()
    #stencil = np.zeros(image.shape).astype(image.dtype)
    #kernel = np.ones((1,1),np.uint8)
    #image_with_contour = cv2.bitwise_not(image_with_contour)
    cv2.drawContours(image_with_contour, contour, -1, (255,255,255), 4)
    #cv2.fillPoly(stencil, contour, (255,255,255))
    #cv2.dilate(stencil, kernel, iterations=10000)
    #stencil.imwrite('St.jpg')
    #cv2.fillConvexPoly(stencil, contour, (255,255,255))
    #image_with_contour = cv2.bitwise_and(image_with_contour, stencil)
    #image_with_contour = cv2.bitwise_and(image_with_contour, stencil)
    '''
    #easy function
    ellipse = cv2.fitEllipse(contour)
    #add it
    cv2.ellipse(image_with_contour, ellipse, green, 2, cv2.LINE_AA)
    '''
    #cv2.imshow("img",image_with_contour)
    #cv2.waitKey(0)
    return image_with_contour
    #return stencil
def find_tumor(image):
    # we'll be manipulating pixels directly
    #most compatible for the transofrmations we're about to do
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Make a consistent size
    #get largest dimension
    max_dimension = max(image.shape)
    #The maximum window size is 700 by 660 pixels. make it fit in that
    scale = 700/max_dimension
    #resize it. same width and hieght none since output is 'image'.
    image = cv2.resize(image, None, fx=scale, fy=scale)
    
    #we want to eliminate noise from our image. clean. smooth colors without
    #dots
    # Blurs an image using a Gaussian filter. input, kernel size, how much to filter, empty)
    image_blur = cv2.GaussianBlur(image, (7, 7), 0)
    #t unlike RGB, HSV separates luma, or the image intensity, from
    # chroma or the color information.
    #just want to focus on color, segmentation
    image_blur_hsv = cv2.cvtColor(image_blur, cv2.COLOR_RGB2HSV)
    
    # Filter by colour
    # Purple for Tumor
    min_color = np.array([90, 100, 80])
    max_color = np.array([140, 256, 256])
    #layer
    mask1 = cv2.inRange(image_blur_hsv, min_color, max_color)

    min_color2 = np.array([170, 100, 80])
    max_color2 = np.array([180, 256, 256])
    
    mask2 = cv2.inRange(image_blur_hsv, min_color2, max_color2)
    
    #mask = mask1 + mask2
    mask = mask1
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
    #morph the image. closing operation Dilation followed by Erosion. 
    #It is useful in closing small holes inside the foreground objects, 
    #or small black points on the object.
    mask_closed = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    #erosion followed by dilation. It is useful in removing noise
    mask_clean = cv2.morphologyEx(mask_closed, cv2.MORPH_OPEN, kernel)

    # Find biggest tumor
    #get back list of segmented tumor and an outline for the biggest one
    big_tumor_contour, mask_tumors = find_biggest_contour(mask_clean)

    # Overlay cleaned mask on image
    # overlay mask on image, tumor now segmented
    #overlay = overlay_mask(mask_closed, image)

    # Circle biggest tumor
    #circle the biggest one
    #show(image)
    circled = circle_contour(image, big_tumor_contour)
    
    #we're done, convert back to original color scheme
    bgr = cv2.cvtColor(circled, cv2.COLOR_RGB2BGR)
    show(circled)
    return bgr

#read the image
#image = cv2.imread('OP/JHS/img-8.jpg')
#detect it
#result = find_tumor(image)
#print result
#write the new image
#cv2.imwrite('aniresult8.jpg', result)
#work2
jhs = glob.glob('OP/JHS/*.jpg')
jhs = sorted(jhs)

for i in range(0, len(jhs)):
	img = cv2.imread(jhs[i])
	result = find_tumor(img)
	cv2.imwrite('Liver_OP_BG/liver-'+str(i).zfill(8)+'.jpg',result)
