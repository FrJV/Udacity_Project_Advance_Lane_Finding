'''This file is developed for the Udacity Project Advance Lane Finding.
It contains functions to fit a plynomial o the lanes.
All functions are based on those included in Lesson 8 from the Udacity course Self-driving car engineer.'''

import numpy as np
import cv2
import camera_cal_helper as cal

def find_lane_pixels(binary_top, nwindows, margin, minpix):
    '''Calculates the pixels corresponding to the lane'''
    # Create an output image to draw on and visualize the result
    out_img = np.dstack((binary_top, binary_top, binary_top))
    # Find the peak of the left and right halves of the bottom half of the image
    # These are be the starting point for the left and right lines
    sum_pix = np.sum(binary_top[binary_top.shape[0]//2:,:], axis=0)
    midpoint = np.int(sum_pix.shape[0]//2)
    leftx_current = np.argmax(sum_pix[:midpoint])
    rightx_current = np.argmax(sum_pix[midpoint:]) + midpoint
    # Set height of windows - based on nwindows and image shape
    window_height = np.int(binary_top.shape[0]//nwindows)
    # Identify the x and y positions of all nonzero pixels in the image
    nonzero = binary_top.nonzero()
    nonzeroy = np.array(nonzero[0])
    nonzerox = np.array(nonzero[1])
    # Lists to receive left and right lane pixel indices
    left_lane_inds = []
    right_lane_inds = []
    # Loop through the windows
    for window in range(nwindows):
        # Identify window boundaries in x and y (and right and left)
        win_y_low = binary_top.shape[0] - (window+1)*window_height
        win_y_high = binary_top.shape[0] - window*window_height
        win_xleft_low = leftx_current - margin
        win_xleft_high = leftx_current + margin
        win_xright_low = rightx_current - margin
        win_xright_high = rightx_current + margin
        # Draw the windows on the visualization image
        cv2.rectangle(out_img,(win_xleft_low,win_y_low), (win_xleft_high,win_y_high), (0,255,0), 2)
        cv2.rectangle(out_img,(win_xright_low,win_y_low), (win_xright_high,win_y_high),(0,255,0), 2)
        # Identify the nonzero pixels in x and y within the window
        good_left_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) & (nonzerox >= win_xleft_low) &  (nonzerox < win_xleft_high)).nonzero()[0]
        good_right_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) & (nonzerox >= win_xright_low) &  (nonzerox < win_xright_high)).nonzero()[0]
        # Append these indices to the lists
        left_lane_inds.append(good_left_inds)
        right_lane_inds.append(good_right_inds)
        #If you found more than minpix pixels, recenter next window on their mean position
        if len(good_left_inds)>minpix:
            leftx_current = np.int(np.mean(nonzerox[good_left_inds]))
        if len(good_right_inds)>minpix:
            rightx_current = np.int(np.mean(nonzerox[good_right_inds]))
    # Concatenate the arrays of indices (previously was a list of lists of pixels)
    try:
        left_lane_inds = np.concatenate(left_lane_inds)
        right_lane_inds = np.concatenate(right_lane_inds)
    except ValueError:
        # Avoids an error if the above is not implemented fully
        pass
    # Extract left and right line pixel positions
    leftx = nonzerox[left_lane_inds]
    lefty = nonzeroy[left_lane_inds]
    rightx = nonzerox[right_lane_inds]
    righty = nonzeroy[right_lane_inds]
    return leftx, lefty, rightx, righty, out_img

def fit_polynomial(img_shape, leftx, lefty, rightx, righty):
    '''Fits a polynomial based on the provided input'''
    #Coefficients of a second order polynomial fit to each lane
    left_coeff = np.polyfit(lefty, leftx, 2)
    right_coeff = np.polyfit(righty, rightx, 2)
    # Generate x and y values for plotting
    ploty = np.linspace(0, img_shape[0]-1, img_shape[0])
    left_fitx = left_coeff[0]*ploty**2 + left_coeff[1]*ploty + left_coeff[2]
    right_fitx = right_coeff[0]*ploty**2 + right_coeff[1]*ploty + right_coeff[2]
    return left_coeff, right_coeff, left_fitx, right_fitx, ploty

def lane_car_parameters(img_shape, left_coeff, right_coeff, left_fitx, right_fitx, ploty, xm_per_pix, ym_per_pix):
    '''Returns the radious of curvature in and distance to the center of the lane in m'''
    # Define coefficients for radious of curvature
    A_l=left_coeff[0]*xm_per_pix/ym_per_pix**2
    A_r=right_coeff[0]*xm_per_pix/ym_per_pix**2
    B_l=left_coeff[1]*xm_per_pix/ym_per_pix
    B_r=right_coeff[1]*xm_per_pix/ym_per_pix
    y_eval = np.max(ploty)*ym_per_pix
    #Calculate radius of curvature
    left_curverad = ((1+(2*A_l*y_eval+B_l)**2)**1.5)/np.absolute(2*A_l)
    right_curverad = ((1+(2*A_r*y_eval+B_r)**2)**1.5)/np.absolute(2*A_r)
    #Calculate distance from car to the center of lane
    center=img_shape[1]//2
    dist_left=(left_fitx[img_shape[0]-1]-center)*xm_per_pix
    dist_right=(right_fitx[img_shape[0]-1]-center)*xm_per_pix
    dist_center=dist_left+dist_right
    return left_curverad, right_curverad, dist_center

def lanes_image(image, left_fitx, right_fitx, ploty, x_off_low, x_off_high):
    '''includes the lanes in the image'''
    #Rearrange the points for fillPoly function
    pts_left = np.array([np.transpose(np.vstack([left_fitx, ploty]))])
    pts_right = np.array([np.flipud(np.transpose(np.vstack([right_fitx, ploty])))])
    pts = np.hstack((pts_left, pts_right))
    #Make image with the lanes in green
    lane_top=np.zeros_like(image)
    cv2.fillPoly(lane_top,np.int_(pts),(0,255,0))
    #Put the image in the original prespective
    lanes=cal.pers_transform(lane_top, x_off_low, x_off_high, 1)
    #Combine with original image
    result = cv2.addWeighted(image, 1, lanes, 0.3, 0)
    return result

def add_lane_par(image, left_curverad, right_curverad, dist_center):
    '''adds the distance to the center and radious of curvature to the image as text'''
    #See side of distane to center
    if dist_center>0:
        side='right'
    else:
        side='left'
    #Prepare text
    text1='Left radius of curvature: '+str(int(left_curverad))+' m'
    text2='Right radius of curvature: '+str(int(right_curverad))+' m'
    text3='Car is '+str(np.around(np.abs(dist_center),2))+' m to the '+side+' of the center of the lane'
    #Include text in image
    cv2.putText(image, text1, (300,50), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255) )
    cv2.putText(image, text2, (300,100), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255) )
    cv2.putText(image, text3, (100,150), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255) )
    return None
