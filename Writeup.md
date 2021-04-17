# Writeup
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

[image1]: ./output_images/writeup_chess_board.png "Camera calibration example"
[image2]: ./output_images/writeup_distortion_correction.png "Road tranformation"
[image3]: ./output_images/writeup_binary_image.png "Binary Example (binary_image function)"
[image4]: ./output_images/writeup_binary_image2.png "Binary Example (alt_binary_image function)"
[image5]: ./output_images/writeup_transformed.png "Perspective transform Example"
[image6]: ./output_images/writeup_result_image.png "Result Example"
[video1]: ./project_video_output.mp4 "Project video"
[video2]: ./challenge_video_output.mp4 "Challenge video"
[video3]: ./harder_challenge_video_output.mp4 "Harder challenge video"


## [Rubric](https://review.udacity.com/#!/rubrics/571/view) Points

---


### Camera Calibration

#### 1. Briefly state how you computed the camera matrix and distortion coefficients. Provide an example of a distortion corrected calibration image.
All the functions that facilitate this step are contained in the file called `camera_cal_helper.py` (these functions are all based on those included in Lesson 6 from the Udacity course Self-driving car engineer). These functions are used in the first step of the main project notebook: `Project.ipynb`. 

After importing the relevant libraries I prepare the object points (`obj`) and the image points(`corners`):
- The object points ("real" coordinates of the chessboard corners) are similar for each chess board image. 
- The image points (image coordinates of chessboard corners) are calculated for each image using the function find_corners_chessboard. 
For each image the corners are successfully identified, `obj` and `corners` are appended to the lists of object points (`obj_points`) and image points(`img_points`).

Finally, these sets of object and image points are used to compute the camera calibration and distortion coefficients and apply the distortion correction to an example image (in this case `calibration1` - see result below). Both these steps are performed in `cal_undistort` function.

Additionally, a function `compare_images` (in file `visualize_helper.py`) was made to plot both images (original and undistorted) and save the result.

![alt text][image1]

### Pipeline (single images)

#### 1. Provide an example of a distortion-corrected image.
In this step the same functions used in the point above were applied to the images in the `test_images` folder. All the output images were saved in folder `output_images` using the same name as the input ones. 
As an example, see below image:
![alt text][image2]

#### 2. Describe how (and identify where in your code) you used color transforms, gradients or other methods to create a thresholded binary image.  Provide an example of a binary image result.
The functions used for this step are contained in the file called `binary_image_helper.py` (these functions are all based on those included in Lesson 7 from the Udacity course Self-driving car engineer). These functions are used in step 2.2 of the main project notebook: `Project.ipynb`. 

I created two different binary image functions (`binary_image` and `alt_binary_image`) to be used in the project video:
- The first one is a composition based on R and S channels thresholds. It isolates the lanes very well from the rest of the environment, but it has troubles catching them when light is not good.
- The second one adds a gradient threshold in x direction and a direction threshold. It finds the lanes better, but it introduces aditional noise.

The numbers used for the thresholds, sobel kernel, etc. can be found in the notebook `Project.ipynb`.

Here's an example of the output of function `binary_image`:
![alt text][image3]

And here from the output of function `alt_binary_image`:
![alt text][image4]


#### 3. Describe how (and identify where in your code) you performed a perspective transform and provide an example of a transformed image.
This step uses the function `pers_transform`, in the file called `camera_cal_helper.py`. This fuction assumes that the road is centered in the image. 

Following the assumption that camera is in the ceterline, the function needs just an offset in the x direction to create the source and destination points. To find the points in the vertical direction it assumes the horizon is at 65% height in the image.
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
The lane line pixels are found with the functions `find_line_pixels` and `line_around_poly`, in the file `line_class.py` (lines 7 - 62) - these functions are all based on those included in Lesson 8 from the Udacity course Self-driving car engineer.
These functions are used inside the `class Line`, programmed in the same file.

Once they are found, the polynomial fit occurs in the class line (in the same file), inside functions `init_line` and `update_line` (lines 103 -156).

The `class Line` is used in both steps 2.4 and 3 of the project notebook `Project.ipynb`

The number of windows, window width and minimum pixels to recenter used can be found in pont 2.4 of `Project.ipynb`.

#### 5. Describe how (and identify where in your code) you calculated the radius of curvature of the lane and the position of the vehicle with respect to center.
The radius of curvature is calculated inside the `class Line`, in the file `line_class.py` (lines 182 - 187).
The position with respect to the centeris calculated in the function `pipeline`, in the project notebook (`Project.ipynb`), in point 2.4.2.

Both are used as a "healthy check" for the lines, and are displayed in the result images (and videos).

#### 6. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.
The generation of the image with the lane identified is made with functions `lanes_image` and `add_lane_par` in the file `visualize_helper.py`. Also, they're used as partof function `pipeline` in step 2.4 of the main project notebook: `Project.ipynb`.

This is an example of the final result after all the steps:
![alt text][image6]

---

### Pipeline (video)

#### 1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (wobbly lines are ok but no catastrophic failures that would cause the car to drive off the road!).
Here's a [link to my video result](./project_video_output.mp4)

---

### Discussion

#### 1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?
The biggest challenge I found was to identify the lines (especially the discontinuous line) when there are changes of light (this is particularly remarkable under the tunnel in the `challenge video`, when both lines are lost).

A number of "safety checks" were introduced by checking the variation of the radius of curvature and the distance to the center (in the `class Line`), and also if they are paralell and curve in the same direction (in the function `pipeline`). Also, the function `alt_binary_image` was used in cases were line pixels were not found (if this still occured, the previous lines were retrieved and reused - see `pipeline` and `class Line`). Still, the result for the challenge video is not satisfactory.

To be honest I'm not sure what could I do to make it more robust. I played with further checks to filter the lines, but then they made them very stiff (once they found a good one, they stayed there for very long time).

You an find the output for teh three videos: `project_video_output.mp4`, `challenge_video_output.mp4` and `harder_challenge_video_output.mp4` in the same directory as this writeup. 
