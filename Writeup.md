## Writeup Template

### You can use this file as a template for your writeup if you want to submit it as a markdown file, but feel free to use some other method and submit a pdf if you prefer.

---

**Advanced Lane Finding Project**

The goals / steps of this project are the following:

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Use color transforms, gradients, etc., to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

[//]: # (Image References)

[image1]: ./images_for_writeup/undistorted_chess_board.png "Camera calibration example"
[image2]: ./images_for_writeup/distortion_correction_lanes.png "Road tranformation"
[image3]: ./images_for_writeup/binary_image.png "Binary Example"
[image4]: ./images_for_writeup/source_points.png "Source points Example"
[image5]: ./images_for_writeup/transformed_image.png "Perspective transform Example"
[image6]: ./images_for_writeup/lanes_image.png "Lane identification Example"
[image7]: ./images_for_writeup/result_image.png "Result Example"
[video1]: ./project_video.mp4 "Video"

## [Rubric](https://review.udacity.com/#!/rubrics/571/view) Points

### Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

---

### Writeup / README

#### 1. Provide a Writeup / README that includes all the rubric points and how you addressed each one.  You can submit your writeup as markdown or pdf.  [Here](https://github.com/udacity/CarND-Advanced-Lane-Lines/blob/master/writeup_template.md) is a template writeup for this project you can use as a guide and a starting point.  

You're reading it!

### Camera Calibration

#### 1. Briefly state how you computed the camera matrix and distortion coefficients. Provide an example of a distortion corrected calibration image.
All the functions that facilitate this step are contained in the file called `camera_cal_helper.py` (these functions are all based on those included in Lesson 6 from the Udacity course Self-driving car engineer). These functions are used in the first steps of the main project notebook: `Project.ipynb`. 

After importing the relevant libraries I prepare the object points (`obj`) and the image points(`corners`):
- The object points ("real" coordinates of the chessboard corners) are similar for each chess board image. 
- The image points (image coordinates of chessboard corners) are calculated for each image using the function find_corners_chessboard. 
For each image the corners are successfully identified, `obj` and `corners` are appended to the lists of object points (`obj_points`) and image points(`img_points`).

Finally, these sets of object and image points are used to compute the camera calibration and distortion coefficients and apply the distortion correction to an example image (in this case `calibration1` - see result below). Both these steps are performed in `cal_undistort` function.

Additionally, a function `compare_images` was made to plot both images (original and undistorted) and save the result.


![alt text][image1]

### Pipeline (single images)

#### 1. Provide an example of a distortion-corrected image.
In this step the same functions used in the point above were applied to the images in the `test_images` folder. All the output images were saved in folder `output_images` using the same name as the input ones. 
As an example, see below image:
![alt text][image2]

#### 2. Describe how (and identify where in your code) you used color transforms, gradients or other methods to create a thresholded binary image.  Provide an example of a binary image result.
The functions used for this step are contained in the file called `binary_image_helper.py` (these functions are all based on those included in Lesson 7 from the Udacity course Self-driving car engineer). These functions are used in the 2.2 step of the main project notebook: `Project.ipynb`. 

In order to produced the output binary image I used a combination of:
- Color, channel S, threshold (150, 250)
- Magnitud of the gradient in the red channel. Sobel kernel of 7 and threshold (50, 100)
- Direction of the gradient. Sobel kernel of 9 and threshold (0.8, 1.2)

To come up with these parameters and combination I tested different alternatives in the notebook `Tests_binary_image.ipynb`.

Here's an example of my output for this step:
![alt text][image3]

#### 3. Describe how (and identify where in your code) you performed a perspective transform and provide an example of a transformed image.
This step uses the function `pers_transform`, in the file called `camera_cal_helper.py`. This fuction assumes that the road is centered in the image. Actually, this induces a small error, as it seems the camera is slightly closer to the left lane (see image below).
![alt text][image4]

Following the the assumption that camera is in the ceterline, the function needs just an offset in the x direction to create the source and destination points. To find the points in the vertical direction it assumes the horizon is at 65% height in the image.
I used the ipython notebook `Perspective_Transform_tests.ipynb` to come up with the best parameters, ending up using `x_offlow=450` and `x_offhigh=75`. 

This resulted in the following source and destination points:

| Source        | Destination   | 
|:-------------:|:-------------:| 
| 190, 720      | 378, 720      | 
| 1090, 720     | 903, 720      |
| 715, 468      | 903, 0        |
| 565, 468      | 378, 0        |

Result is shown in this example image:
![alt text][image5]

#### 4. Describe how (and identify where in your code) you identified lane-line pixels and fit their positions with a polynomial?
The functions that facilitate this step are contained in the file `lane_polynomial_helper.py`, functions `find_lane_pixels` and `fit_polynomial`  (these functions are all based on those included in Lesson 8 from the Udacity course Self-driving car engineer). 
These functions are used in the step 2.4 of the main project notebook: `Project.ipynb`.
In order to set the number of windows, window width and minimum pixels to recenter, the notebook `Test_finding_lanes.ipynb` was used. In general, the continous line is caught well, but the discontinuous is more challenging. 

As an example of lane identification see image below:
![alt text][image6]

#### 5. Describe how (and identify where in your code) you calculated the radius of curvature of the lane and the position of the vehicle with respect to center.
This occurs in function `lane_car_parameters` in the file `lane_polynomial_helper.py`. Also, it's use in step 2.4 of the main project notebook: `Project.ipynb`.

#### 6. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.
This last step is made with functions `lanes_image` and `add_lane_par` in the file `lane_polynomial_helper.py`. Also, they're used in step 2.4 of the main project notebook: `Project.ipynb`.

This is an example of teh final result after all the steps:
![alt text][image7]

---

### Pipeline (video)

#### 1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (wobbly lines are ok but no catastrophic failures that would cause the car to drive off the road!).

Here's a [link to my video result](./project_video.mp4)

---

### Discussion

#### 1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

Here I'll talk about the approach I took, what techniques I used, what worked and why, where the pipeline might fail and how I might improve it if I were going to pursue this project further.  
