'''This file is developed for the Udacity Project Advance Lane Finding.
It contains a class line and additional functions to make it work.
find_line_pixels and line_around_poly are based on functions included in Lesson 8 from the Udacity course Self-driving car engineer.'''

import numpy as np

def find_line_pixels(img, nwindows, margin, minpix):
    '''Calculates the pixels corresponding to the lane'''
    # Find the peak of the bottom half of the image
    # These are be the starting point for the line
    sum_pix = np.sum(img[img.shape[0]//2:,:], axis=0)
    x_current = np.argmax(sum_pix)
    # Set height of windows - based on nwindows and image shape
    window_height = np.int(img.shape[0]//nwindows)
    # Identify the x and y positions of all nonzero pixels in the image
    nonzero = img.nonzero()
    nonzeroy = np.array(nonzero[0])
    nonzerox = np.array(nonzero[1])
    # Lists to receive lane pixel indices
    lane_inds = []
    # Loop through the windows
    for window in range(nwindows):
        # Identify window boundaries in x and y (and right and left)
        win_y_low = img.shape[0] - (window+1)*window_height
        win_y_high = img.shape[0] - window*window_height
        win_x_low = x_current - margin
        win_x_high = x_current + margin
        # Identify the nonzero pixels in x and y within the window
        good_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) & (nonzerox >= win_x_low) &  (nonzerox < win_x_high)).nonzero()[0]
        # Append these indices to the lists
        lane_inds.append(good_inds)
        #If you found more than minpix pixels, recenter next window on their mean position
        if len(good_inds)>minpix:
            x_current = np.int(np.mean(nonzerox[good_inds]))
    # Concatenate the arrays of indices (previously was a list of lists of pixels)
    try:
        lane_inds = np.concatenate(lane_inds)
    except ValueError:
        # Avoids an error if the above is not implemented fully
        pass
    # Extract left and right line pixel positions
    pixels_x = nonzerox[lane_inds]
    pixels_y = nonzeroy[lane_inds]
    return pixels_x, pixels_y

def line_around_poly(img, polyfit):

    # Margin around the previous polynomial to search
    margin = 100

    # Grab activated pixels
    nonzero = img.nonzero()
    nonzeroy = np.array(nonzero[0])
    nonzerox = np.array(nonzero[1])

    # Set the area of search based on activated x-values within the +/- margin of the polynomial function
    lane_inds = ((nonzerox > (polyfit[0]*(nonzeroy**2) + polyfit[1]*nonzeroy + polyfit[2] - margin)) & (nonzerox < (polyfit[0]*(nonzeroy**2) + polyfit[1]*nonzeroy + polyfit[2] + margin)))

    # Extract left and right line pixel positions
    pixels_x = nonzerox[lane_inds]
    pixels_y = nonzeroy[lane_inds]
    return pixels_x, pixels_y

class Line():
    def __init__(self, nwindows, margin, minpix, xm_per_pix, ym_per_pix):
        ## Initiate main parameters for the functions
        #number of sliding windows
        self.nwindows = nwindows
        #width of the windows(+/- margin)
        self.margin = margin
        #minimum number of pixels found to recenter window
        self.minpix = minpix
        #meters per pixel in x and y direction
        self.ym = ym_per_pix
        self.xm = xm_per_pix

        ## Initiate characteristics of the line
        #Does the line exist already
        self.exists = False
        #Polynomal fit coefficients
        self.polyfit = None
        #List of last 5 polynomial fits
        self.fitlist = []
        #Average polynomial fit (based on list)
        self.avefit = None
        #Line polynomial
        self.poly = None
        #Radius of curvature
        self.curverad = None
        #Dist to zero
        self.dist = None
        #Previous wrong lines
        self.wrong = 0

    def new_line(self, top_binary_image):
        '''The image corresponds only to half image (left or right)'''
        if self.exists:
            self.update_line(top_binary_image)
        else:
            self.init_line(top_binary_image)
        return

    def init_line(self, top_binary_image):
        #Update exists
        self.exists = True
        #Calculate lane pixels
        pixels_x, pixels_y = find_line_pixels(top_binary_image, self.nwindows, self.margin, self.minpix)
        if pixels_x.size == 0 or pixels_y.size == 0:
            self.exists = False
            return
        #Calculate polynomial coefficients
        self.polyfit = np.polyfit(pixels_y, pixels_x, 2)
        #Calculate fitlist
        self.update_fitlist()
        #Calculate avefit
        self.update_avefit()
        #Caculate rest of parameters
        self.calculate_parameters(top_binary_image.shape)
        return

    def update_line(self, top_binary_image):
        ## Calculate parameters
        #Calculate lane pixels
        pixels_x, pixels_y = line_around_poly(top_binary_image, self.polyfit)
        if pixels_x.size == 0 or pixels_y.size == 0:
            self.exists = False
            return
        #Polynomial coefficients
        polyfit = np.polyfit(pixels_y, pixels_x, 2)
        #Poynomial
        ploty = np.linspace(0, top_binary_image.shape[0]-1, top_binary_image.shape[0])
        polynomial = polyfit[0]*ploty**2 + polyfit[1]*ploty + polyfit[2]
        #Curve radious
        curverad = self.calc_radius(polyfit, np.max(ploty))
        #Distance to zero
        dist = [polynomial[top_binary_image.shape[0]-1]*self.xm, polynomial[0]*self.xm]
        ## Sanity check
        if self.check_line(curverad, dist):
            self.wrong = 0
            #Save parameters
            self.polyfit = polyfit
            self.update_fitlist()
            self.update_avefit()
            #Caculate rest of parameters
            self.calculate_parameters(top_binary_image.shape)
        else:
            self.wrong += 1
            #print('Skip line')
            if self.wrong > 4:
                self.wrong = 0
                self.fitlist = []
                self.init_line(top_binary_image)
                #print('Reinitialize line')
        return

    def check_line(self, curverad, dist):
        error_c = 150 #m
        error_d = 0.2 # m
        status = True
        #Check radius
        if np.abs(curverad - self.curverad) > error_c:
            #print('Cuverad out of boundaries. Error: {} m'.format(int(curverad-self.curverad)))
            status = False
        elif np.abs(dist[0] - self.dist[0]) > error_d or np.abs(dist[1] - self.dist[1]) > error_d:
            #print('Dist out of boundaries. Error: {} pix'.format(int(dist-self.dist)))
            status = False
        return status

    def update_fitlist(self):
        self.fitlist.append(self.polyfit)
        if len(self.fitlist)>5:
                del self.fitlist[0]
        return None

    def update_avefit(self):
        M = np.array(self.fitlist)
        self.avefit = np.mean(M, axis=0)
        return None

    def calc_radius(self, polyfit, y_p):
        A = polyfit[0]*self.xm/self.ym**2
        B = polyfit[1]*self.xm/self.ym
        y_eval = y_p*self.ym
        curverad = ((1+(2*A*y_eval+B)**2)**1.5)/np.absolute(2*A)
        return curverad

    def line_returned(self, top_binary_image):
        if len(self.fitlist) < 2 or self.wrong > 4:
            self.wrong = 0
            self.fitlist = []
            self.init_line(top_binary_image)
        else:
            self.wrong += 1
            self.retrieve_line(top_binary_image)
        return None

    def retrieve_line(self, top_binary_image):
        self.fitlist[-1] = self.fitlist[-2]
        self.update_avefit()
        self.calculate_parameters(top_binary_image.shape)
        return None

    def calculate_parameters(self, image_shape):
        #Calculate polynomial
        ploty = np.linspace(0, image_shape[0]-1, image_shape[0])
        self.poly = self.avefit[0]*ploty**2 + self.avefit[1]*ploty + self.avefit[2]
        #Calculate radious (in m)
        self.curverad = self.calc_radius(self.avefit, np.max(ploty))
        #Calculate distance (in pix)
        self.dist = [self.poly[image_shape[0]-1]*self.xm, self.poly[0]*self.xm]
        return
