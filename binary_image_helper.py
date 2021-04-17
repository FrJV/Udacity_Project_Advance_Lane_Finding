'''This file is developed for the Udacity Project Advance Lane Finding.
It contains functions to help creating a binary image that identifies the lanes.
All functions are based on those included in Lesson 7 from the Udacity course Self-driving car engineer.'''

import numpy as np
import cv2

def abs_sobel(img, orient='x', sobel_kernel=3, thresh=(0, 255)):
    '''This function to create a binary output based on the sobel gradient in x or y directon and a selected threshold
    Img is the image in a single channel format (e.g. grey, or one of the components H,L or S)'''
    # Take the derivative in x or y given orient = 'x' or 'y'
    if orient=='x':
        sobel = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=sobel_kernel)
    elif orient=='y':
        sobel = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=sobel_kernel)
    else:
        print('Error')
        return
    # Take the absolute value of the derivative or gradient
    abs_sobel = np.absolute(sobel)
    # Scale to 8-bit (0 - 255) then convert to type = np.uint8
    scaled_sobel = np.uint8(255*abs_sobel/np.max(abs_sobel))
    # Create a mask of 1's where the scaled gradient magnitude
    binary_output = np.zeros_like(scaled_sobel)
    binary_output[(scaled_sobel >= thresh[0]) & (scaled_sobel <= thresh[1])] = 1
    return binary_output

def mag_sobel(img, sobel_kernel=3, thresh=(0, 255)):
    '''This fuunction to create a binary output based on the sobel gradient magnitude and a selected threshold
    Img is the image in a single channel format (e.g. grey, or one of the components H,L or S)'''
    # Take the derivative in x or y given orient = 'x' or 'y'
    sobel_x = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=sobel_kernel)
    sobel_y = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=sobel_kernel)
    # Calculate the magnitude
    mag_sobel = np.sqrt(sobel_x**2 + sobel_y**2)
    # Scale to 8-bit (0 - 255) then convert to type = np.uint8
    scaled_mag = np.uint8(255*mag_sobel/np.max(mag_sobel))
    # Create a mask of 1's where the scaled gradient magnitude
    binary_output = np.zeros_like(scaled_mag)
    binary_output[(scaled_mag >= thresh[0]) & (scaled_mag <= thresh[1])] = 1
    return binary_output

def dir_sobel(img, sobel_kernel=3, thresh=(0, np.pi/2)):
    '''This function to create a binary output based on the sobel gradient direction and a selected threshold
    Img is the image in a single channel format (e.g. grey, or one of the components H,L or S)'''
    # Take the gradient in x and y separately
    sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=sobel_kernel)
    sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=sobel_kernel)
    # Take the absolute value of the x and y gradients
    abs_sobelx = np.absolute(sobelx)
    abs_sobely = np.absolute(sobely)
    # Calculate the direction of the gradient
    direction=np.arctan2(abs_sobely, abs_sobelx)
    # Create a binary mask where direction thresholds are met
    binary_output = np.zeros_like(direction)
    binary_output[(direction >= thresh[0]) & (direction <= thresh[1])] = 1
    return binary_output

def binary_threshold(img, thresh=(0, 255)):
    '''This function to create a binary output based on the selected threshold
    Img is the image in a single channel format (e.g. grey, or one of the components H,L or S)'''
    # Create a mask of 1's where the scaled gradient magnitude
    binary_output = np.zeros_like(img)
    binary_output[(img >= thresh[0]) & (img <= thresh[1])] = 1
    return binary_output
