'''This file is developed for the Udacity Project Advance Lane Finding.
It contains functions to help solving the camera calibration and perspective transform.
All functions are based on those included in Lesson 6 from the Udacity course Self-driving car engineer.'''

import numpy as np
import cv2
import matplotlib.pyplot as plt

def find_corners_chessbooard(img,nx,ny,plot=1):
    ''' Function to find and draw the corners of the chessboard
    - img is the image in BGR
    - nx and ny are the number of square coners (not counting external) in the chessboard in x and y direction
    - plot is a switch to activate or deactivate the plotting of the result
    '''
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Find the chessboard corners
    ret, corners = cv2.findChessboardCorners(gray, (nx, ny), None)
    # If found, draw corners
    if ret and plot:
        # Draw and display the corners
        cv2.drawChessboardCorners(img, (nx, ny), corners, ret)
        plt.imshow(img)
        #print(corners)
    return ret, corners


def object_points(nx,ny):
    '''Function to create object points based on the square coners
    in the chessboard in x and y direction (nx and ny)'''
    objp = np.zeros((nx*ny,3), np.float32)
    objp[:,:2] = np.mgrid[0:nx, 0:ny].T.reshape(-1,2)
    return objp

def cal_undistort(img, objpoints, imgpoints):
    ''' Function to undistort an image based on object points and image points'''
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, img.shape[1:], None, None)
    undist = cv2.undistort(img, mtx, dist, None, mtx)
    return undist

def pers_transform(image, x_off_low, x_off_high, Inv=0):
    '''Function to perform persective transform on lane road images
    It creates the source and destination ponts from x_off_low and x_off_high
    Inv is a flag to make the inverse transform'''
    # Define image size for warpPerspective function
    img_size = (image.shape[1], image.shape[0])
    #Parameters for source and destination points
    xmid=image.shape[1]/2
    yhigh=image.shape[0]*0.65
    ylow=image.shape[0]
    x_off=(x_off_high+x_off_low)//2
    #Source points
    source= np.float32([[xmid-x_off_low,ylow],[xmid+x_off_low,ylow],[xmid+x_off_high,yhigh],[xmid-x_off_high,yhigh]])
    #Destination points
    dest= np.float32([[xmid-x_off,ylow],[xmid+x_off,ylow],[xmid+x_off,0],[xmid-x_off,0]])
    #Perspective matrix
    if not Inv:
        M = cv2.getPerspectiveTransform(source, dest)
    else:
        M = cv2.getPerspectiveTransform(dest, source)
    #Perform perspective transform
    transformed = cv2.warpPerspective(image, M, img_size, flags=cv2.INTER_LINEAR)
    return transformed
