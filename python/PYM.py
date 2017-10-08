# -*- coding: utf-8 -*-
"""
Created on Tue Jan 10 17:03:41 2017

@author: valle
"""

def PYM_image_transformation(original, filename): 
    "This function performs the PYM calculation and returns a new frame"
    h, w = original[:,:,0].shape # get original image shape
    pym = np.zeros((h, w),np.int) # blank b/w image for storing pym image
    red = np.zeros((h, w),np.int) # blank array for red
    blue = np.zeros((h, w),np.int) # blank array for blue

    # Specific channels
    red = (original[:,:,2]).astype('float') # reading red channel from original image (NIR)
    blue = (original[:,:,0]).astype('float') # reading blue channel from original image (blue)

    # PYM calculation
    max_sc = np.amax(red - blue/2)
    pym = ((red - blue/2)*255/max_sc).astype('uint8') # computing new channel
    
    pym[red - blue/2 < 0] = 0 # setting limit
    
    # False color image
    False_color_image = np.zeros((h, w,3),np.uint8) # make a blank RGB image 
    False_color_image[:,:,1] = pym
    False_color_image[:,:,2] = 255 - pym
    
    f_image = "FALSE_COLOR_" + filename 
    f_dest = "FALSE_COLOR/" + f_image 
    cv2.imwrite(f_dest, False_color_image) 
   
    return pym # return the image 


def PYM_leaf_area_estimation(filename, include_holes=True):
    image_source = cv2.imread(filename) # import source image
    
    
# Image transformation and storage
    t = PYM_image_transformation(image_source, filename) # Transform image with PYM_image_transformation function
    r_image = "NEW_CHANNEL_" + filename # Filename of the new image (visual checking)
    r_dest = "NEW_CHANNEL/" + r_image # Folder 
    cv2.imwrite(r_dest, t) # saving image
    
# Image analysis
    ret,thresh1 = cv2.threshold(t, 0, 255, cv2.THRESH_OTSU) # OTSU's thresholding

    kernel_open = np.ones((6,6),np.uint8) # large kernel
    kernel_mid = np.ones((4,4),np.uint8) # medium kernel
    kernel_close = np.ones((2,2),np.uint8) # small kernel
    kernel_veryclose = np.ones((1,1),np.uint8) # tiny petit

    erosion = cv2.erode(thresh1, kernel_veryclose,iterations = 1) # edge erosion
    opening = cv2.morphologyEx(erosion, cv2.MORPH_OPEN, kernel_open) # removing noise around the plant
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel_mid) # removing noise inside the plant
    contours, hierarchy = cv2.findContours(closing,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) # finding plant contours
    # aa, contours, hierarchy = cv2.findContours(closing,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) # with an older version of opencv
  

    if include_holes==1: # Counting all pixels inside the largest area
        areas = [] # list
        for contour in contours:
            ar = cv2.contourArea(contour)
            areas.append(ar)
        sorted_area = sorted(areas, key=int, reverse = True)
        leaf_area = sorted_area[0] # largest area, plant area by definition
        leaf_area_index = areas.index(leaf_area) # finding area index 
        cnt = contours[leaf_area_index] # plant contours, with holes included
        cv2.drawContours(closing, [cnt], 0,(255,0,0),-1) # drawing contours with holes included
        
    if include_holes==0: # Counting all pixels detected 
        cv2.drawContours(closing, contours, -1, (255, 255, 255), -1) # drawing contours without including holes
        leaf_area = (closing > 127).sum() # couting plants pixels
        
        
# Image storage
        
    image_finale = "OUTPUT_" + filename # Filename of the output image
    dest_finale = "OUTPUT/" + image_finale # Folder 
    cv2.imwrite(dest_finale, closing) # Saving image
    return leaf_area # Plant area is returned as output of the function

def PYM_folder(dirname, include_holes):
    os.chdir(dirname) # updating current directory
            
    try:
        os.mkdir("FALSE_COLOR") # creating a new folder to save FALSE_COLOR images
        os.mkdir("NEW_CHANNEL") # creating a new folder to save NEW_CHANNEL images
        os.mkdir("OUTPUT") # creating a new folder to save OUTPUT images
    except Exception: 
        pass
        
    fname = "out.csv"
    file = open(fname, "wb")
    writer = csv.writer(file)
    
    writer.writerow(('plant_ID', 'leaf_area_pixel'))

    i=0 
    types = ('*.png', '*.jpg') # checked formats
    files_g = []
    for files in types:
        files_g.extend(glob.glob(files))
    
    for filename in files_g: # loop for found files
        i+=1  
        fi = cv2.imread(filename) # reading image
        
        plant_id = filename[:-4] # picture's name is also plant ID, after removal of 4 last characters (".jpg" or ".png")   
        try:        
                leaf_area_pixel = PYM_leaf_area_estimation(filename, include_holes) # using precendtly declared function
                writer.writerow((plant_id, leaf_area_pixel)) # storing computed leaf_area 
        except IndexError:
            pass
    file.close()   
    
    


