# Completing Class Project Part 1
# Advanced Python for Streaming Analytics
# Julian McClellan

import numpy as np

# Task 0
import cv2
from PIL import Image, ImageDraw

mario1 = cv2.imread("mario.png", cv2.IMREAD_GRAYSCALE)
mario2 = cv2.imread("mario2.png", cv2.IMREAD_GRAYSCALE)

(thresh, mario_bw) = cv2.threshold(mario1, 128, 255, cv2.THRESH_BINARY)
mario_bw = cv2.threshold(mario1, thresh, 255, cv2.THRESH_BINARY)[1]


# cv2.imshow("Window pindow 0", mario_bw)
cv2.waitKey(0)


# Task 1-a 
# I already read in Mario in grey
# cv2.imshow("Window pindow 1-a", mario1)


# Task 1-b
X = 39
mario1_gaus = cv2.GaussianBlur(mario1, (X, X), 0)
# cv2.imshow("Window pindow 1-b", mario1_gaus)


# Task 1-c
def make_smooth_im(path, blur_level = 39, float32 = True):
    """
    Returns a smooth (mario) image
    """
    image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    (thrsh, bw) = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)
    bw_image = cv2.threshold(image, thrsh, 255, cv2.THRESH_BINARY)[1]
    bw_image_gaus = cv2.GaussianBlur(bw_image, (blur_level, blur_level), 0)

    if float32:
        return np.float32(bw_image_gaus)
    else:
        return bw_image_gaus

dif = cv2.absdiff(make_smooth_im("mario.png"), make_smooth_im("mario2.png"))
# cv2.imshow("Window pindow 1-c", dif)


# Task 2/3
import matplotlib.pyplot as plt

def thresh_image(gray_image):
    """
    Returns thresholded version of gray image
    """
    thrsh, bw = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY)
    bw_image = cv2.threshold(gray_image, thrsh, 255, cv2.THRESH_BINARY)[1]
    
    return bw_image

import pdb

TRAIN_TEST_RECTS = {"training": {"left": ((0, 334), (70, 420)), 
                                 "right": ((565, 295), (638, 370))},
                    "testing": {"left": ((20, 10), (85, 30)), "right": ((587, 186), (633, 340))}
                    }
def difference_video(path="train_training.mp4", kernel_size=451, show=True, lr_regions=False):
    """
    """
    plt.close()
    feed_descriptor = cv2.VideoCapture(path)

    change_ratio = []
    if lr_regions:
        if "training" in path:
            vid_type = "training"
        else:
            vid_type = "testing"
        lx1, ly1 = TRAIN_TEST_RECTS[vid_type]["left"][0]
        lx2, ly2 = TRAIN_TEST_RECTS[vid_type]["left"][1]
        rx1, ry1 = TRAIN_TEST_RECTS[vid_type]["right"][0]
        rx2, ry2 = TRAIN_TEST_RECTS[vid_type]["right"][1]
        
        ftf_difs = {"left": [], "right": []}
    else:
        ftf_difs = []
    running_avg_made, last_frame_made = False, False
    alpha = .02
    
    while (feed_descriptor.isOpened()):
        # Read frame by frame
        exists, current_frame = feed_descriptor.read()
    
        if not exists:
            break
    
        cf_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
        cf_gray_gaus = np.float32(cv2.GaussianBlur(cf_gray, (kernel_size, kernel_size), 0))
    
        if not running_avg_made:
            running_avg = cf_gray_gaus
            running_avg_made = True
        else:
            dif = cv2.absdiff(running_avg, cf_gray_gaus)
            change_ratio.append(cv2.countNonZero(dif) / dif.size)
            running_avg = cv2.accumulateWeighted(cf_gray_gaus, running_avg, alpha)
        
        if not last_frame_made:
            last_frame_made = True
        else:
            if lr_regions:
                # Get LR regions, get frame to frame differences
                last_left_cut, cur_left_cut = last_frame[ly1:ly2, lx1:lx2], cf_gray_gaus[ly1:ly2, lx1:lx2]
                last_right_cut, cur_right_cut = last_frame[ry1:ry2:, rx1:rx2], cf_gray_gaus[ry1:ry2, rx1:rx2]
                
                lftf_dif = cv2.absdiff(last_left_cut, cur_left_cut)
                rftf_dif = cv2.absdiff(last_right_cut, cur_right_cut)
    
                ftf_difs["left"].append(cv2.countNonZero(lftf_dif) / lftf_dif.size)
                ftf_difs["right"].append(cv2.countNonZero(rftf_dif) / rftf_dif.size)
            else:
                ftf_dif = cv2.absdiff(last_frame, cf_gray_gaus)
                ftf_difs.append(cv2.countNonZero(ftf_dif) / ftf_dif.size)
            
        last_frame = cf_gray_gaus
    if show:
        fig, ax = plt.subplots()
        if lr_regions:
            ax.plot(range(len(ftf_difs["left"])), ftf_difs["left"], color="green", label="Left Difs", linewidth=.7)
            ax.plot(range(len(ftf_difs["right"])), ftf_difs["right"], color="red", label="Right Difs", linewidth=.7)
            ax.set_title("Change Ratio per Frame (Left vs. Right Cuts): Kernel = {}".format(kernel_size))
            ax.legend()
            ax.set_xlabel("Frame")
        else:
            ax.plot(range(len(ftf_difs)), ftf_difs, color="green", label="Difs", linewidth=.7)
            ax.set_title("Change Ratio per Frame (Whole Image): Kernel = {}".format(kernel_size))
            ax.set_xlabel("Frame")
        plt.show()
    return ftf_difs
    
train_ftf_difs = difference_video(kernel_size=451)

# Task 4
# Drawing the rectangle is kind of useless in actually doing the detection so
# I won't do that.
def determine_train_direction(path="train_training.mp4", kernel_size=451, show=False):
    """
    I'm only going to have this function attempt to determine the direction in
    which the train first appears since in the training video there is only one
    train, and in the testing video, there is only one train, but there is stupid
    slow-motion rewind that shows the same train going several times, which
    I'm not going to deal with. Indeed, the rewind moves the train back to the middle
    of the frame. Why? What live video system messes with time like this?
    """
    lvr = difference_video(path, lr_regions=True, kernel_size=kernel_size, show=show)
    
    # Take first derviative of pixel change ratio
    left_argmax = np.argmax(np.diff(lvr["left"]))
    right_argmax = np.argmax(np.diff(lvr["right"]))
    
    if left_argmax > right_argmax:
        print("The train in {} comes from the left.".format(path))
    elif right_argmax > left_argmax:
        print("The train in {} comes from the right.".format(path))
    else:
        print("Unable to determine train direction")
    
determine_train_direction("train_training.mp4")
determine_train_direction("train_testing.mp4")

    


