import cv2
import numpy as np
import matplotlib.pyplot as plt
import camera_cal_helper as cal

def compare_images(original_image, modified_image, save=0, savefile=None, orig_format='RGB', mod_format='RGB'):
    '''Function to compare to images together'''
    #Modify to RGB if necessary
    if orig_format=='BGR':
        original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    if mod_format=='BGR':
        modified_image = cv2.cvtColor(modified_image, cv2.COLOR_BGR2RGB)
    #Plot
    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(24, 9))
    f.tight_layout()
    if orig_format=='GRAY':
        ax1.imshow(original_image, cmap='gray')
    else:
        ax1.imshow(original_image)
    ax1.set_title('Original', fontsize=50)
    if mod_format=='GRAY':
        ax2.imshow(modified_image, cmap='gray')
    else:
        ax2.imshow(modified_image)
    ax2.set_title('Modified', fontsize=50)
    plt.subplots_adjust(left=0., right=1, top=0.9, bottom=0.)
    #Save
    if save:
        plt.savefig(savefile)
    return None

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
