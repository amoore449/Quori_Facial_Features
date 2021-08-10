#!/usr/bin/env python
# license removed for brevity
import rospy
import rospkg
from PIL import Image as PILimage
import time
import numpy as np
import sys
import cv2
import os.path
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import numpy as np
import math
import cv2
import json

#RISS Summer 2021 8.9.21
#image_process
#Takes in a Json file specifying an animation sequence for Quori's face
#and converts to an animation sequence
#
#
#


#rotate_image
#inputs: image and angle to rotate image to
#Rotates image a certain amount specified in "angle"
#
def rotate_image(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result


#
#malt_overlay_path
#takes in multiplier and poition values to resize a given image
#
def malt_overlay_path(multiplier, x_pos_mult, y_pos_mult, rot, image_1, str_foreground, count):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    foreground = os.path.join(script_dir, str_foreground)
    print(foreground)
    image_3 = cv2.imread(foreground, cv2.IMREAD_UNCHANGED)

    if count == 1:
        ones = np.ones((image_1.shape[0], image_1.shape[1]))*255
        image_1 = np.dstack([image_1, ones])
    ## Smart resizing function
    h, w, c = image_1.shape
    start_h = int(math.floor(h*y_pos_mult))
    start_w  = int(math.floor(w*x_pos_mult))
    h3, w3, c3 = image_3.shape
    w4 = int(math.floor(w3*multiplier))
    h4 = int(math.floor(h3*multiplier))
    resized_image_3 = cv2.resize(image_3, dsize=(w4, h4))
    h5, w5, c4 = resized_image_3.shape
    if(rot):
        h5, w5, c4 = rotate_image(rot).shape
    alpha_image_3 = resized_image_3[:, :, 3] / 255.0
    alpha_image = 1 - alpha_image_3
    for c in range(0, 3):
        image_1[start_h:start_h+h5, start_w:start_w+w5, c] = ((alpha_image*image_1[start_h:start_h+h5, start_w:start_w+w5, c]) + (alpha_image_3*resized_image_3[:, :, c]))
    # uncomment these to test saved files
    #filename = str(count) + 'savedImage.png'
    #cv2.imwrite(filename, image_1)
    return image_1


#
#picture_send
#Process images and send them to Gazebo
#
def picture_send(background, rate, prostart):
    #Establish Rospack and image path systems
    rospack = rospkg.RosPack()
    rospack.list()
    image_path = rospack.get_path('quori_gazebo') + '/images/'

    #initialize publisher node
    rospy.init_node('testvideo', anonymous=True)
    pub = rospy.Publisher("quori/face_image", Image, queue_size=10)
    rospy.init_node('testvideo', anonymous=True)
    script_dir = os.path.dirname(os.path.abspath(__file__))

    #number of images provided
    num_images = len(sys.argv)-2

    # array of all possible image names and all possible image terms
    image_names = []
    image_terms = []

    # create array of image names
    count = 0
    for x in background:
        new_path = x
        image_names.append(new_path)
        count = count + 1
        tester = "tester" + str(count)
        image_terms.append(tester)

    #Create ros images for the file system
    ros_images  = []

    #cycle through images and convert to ROS msg (These might need to be fixed)
    for i, arg in enumerate(image_names):
        print("Converting " + image_terms[i] + " to ROS msg")
        pil_image = image_names[i]
        pil_image = np.uint8(pil_image)

        #Convert to Color format appropriate for cv2
        opencvImage = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGBA2BGRA)
        bridge = CvBridge()
        cv_img = np.array(pil_image)

        #Convert image cv2 image to image message for ROS
        image_message = bridge.cv2_to_imgmsg(cv_img, "bgra8") #if this doesn't work try bgra8
        ros_images.append(image_message)
        period = float(rate)

    nimage = 0
    num_images = len(ros_images)

    # While not shutdown ROS will run ros_images and image_terms loop
    user_input = "y"
    num_count = 0
    proend = time.time()
    print("complete load time")
    print(proend-prostart)
    while user_input != "e":
        nimage = (nimage+1)%num_images
        #signal which image is being sent to ROS
        print("Sending Image " + image_terms[nimage] + " to ROS msg")
        pub.publish(ros_images[nimage])
        time.sleep(period)
        num_count = num_count + 1

        # Current iteration uses user input to exit
        if num_count == num_images:
            num_count = 0
            user_input = raw_input("Press e to exit, any other key to continue: ")

#'''
#find_max_array
#iterate through options to find longest segment
#'''
def find_max_array(array):
    max = 0
    for x in array:
        if len(x) > max:
            max = len(x)
    if max < len(array):
        max = len(array)
    return max

#'''
#segment_extracter
#extract components of json file
#'''
def sub_image_process(data_seg):
    file = []
    x_mult =  []
    y_mult = []
    scale = []
    rot = []
    outer_array = [file ,x_mult ,y_mult,scale,rot]
    for x in data_seg:
        if x.get("file"): outer_array[0].append(x.get("file"))
        if x.get("x_multiplier"): outer_array[1].append(x.get("x_multiplier"))
        if x.get("y_multiplier"): outer_array[2].append(x.get("y_multiplier"))
        if x.get("scale_factor"): outer_array[3].append(x.get("scale_factor"))
        if x.get("rotation_factor"):
            outer_array[4].append(float(x.get("rotation_factor")))
    for y in outer_array:
        if len(y) == 0:
            y.append(0)


    return outer_array

#'''
#compile_pic_array
#compile array of pictures to send in sequence to gazebo
#'''
def compile_pic_array(my_all_expressions):
    max_length = find_max_array(my_all_expressions)
    print(max_length)
    picture_array = []
    for x in range(max_length):
        features = []
        for y in my_all_expressions:
            if len(y) <= x: features.append(len(y)-1)
            else: features.append(x)
        #value ------------------------------------------
        i = 0
        my_picture =[]
        for y in my_all_expressions:
            my_picture.append(my_all_expressions[i][features[i]])
            i = i +1
        picture_array.append(my_picture)
    return picture_array


#'''
#image_process
#define all relevant images to import and file paths
#'''
def image_process(data):
    print("Setting Up Facial Features")
    #All facial components-------------------

    #Add to pupils----------
    pupils_left = sub_image_process(data["leftEyesStills"]["Pupil"])
    pupils_right = sub_image_process(data["rightEyesStills"]["Pupil"])
    #Add to eye lids-------------
    eye_motions_left = sub_image_process(data["leftEyesStills"]["Lid"])
    eye_motions_right = sub_image_process(data["rightEyesStills"]["Lid"])
    #Add to spots-------------------
    spots_left = sub_image_process(data["leftEyesStills"]["Spot"])
    spots_right = sub_image_process(data["rightEyesStills"]["Spot"])
    #Add to lip-------------------
    lip_upper = sub_image_process(data["Mouth"]["Lower_Lip"])
    lip_lower = sub_image_process(data["Mouth"]["Upper_Lip"])
    #Add to brow-------------------
    brow_l = sub_image_process(data["Brows"]["leftBrow"])
    brow_r = sub_image_process(data["Brows"]["rightBrow"])

    #create array of the relevant file sequences for each eye
    all_expressions = [
    pupils_left[0], eye_motions_left[0],
    spots_left[0], pupils_right[0],
    eye_motions_right[0], spots_right[0],
    lip_upper[0], lip_lower[0],
    brow_l[0], brow_r[0]
    ]

    x_multipliers = [pupils_left[1], eye_motions_left[1], spots_left[1],
    pupils_right[1], eye_motions_right[1], spots_right[1], lip_upper[1], lip_lower[1],
    brow_l[1], brow_r[1]]

    y_multipliers = [pupils_left[2], eye_motions_left[2], spots_left[2],
    pupils_right[2], eye_motions_right[2], spots_right[2], lip_upper[2], lip_lower[2],
    brow_l[2], brow_r[2]]

    scale = [pupils_left[3], eye_motions_left[3], spots_left[3],
    pupils_right[3], eye_motions_right[3], spots_right[3], lip_upper[3], lip_lower[3],
    brow_l[3], brow_r[3]]

    rotation_factor = [pupils_left[4], eye_motions_left[4], spots_left[4],
    pupils_right[4], eye_motions_right[4], spots_right[4], lip_upper[4], lip_lower[4],
    brow_l[4], brow_r[4]]

    #put images in order
    picture_array = compile_pic_array(all_expressions)
    comp_x_multipliers = compile_pic_array(x_multipliers)
    comp_y_multipliers = compile_pic_array(y_multipliers)
    comp_scale = compile_pic_array(scale)
    comp_rotation_factor = compile_pic_array(rotation_factor)


    image_consol = []
    i = 0
    script_dir = os.path.dirname(os.path.abspath(__file__))
    str_background = os.path.join(script_dir, "background1.jpg")
    for y in picture_array:
        background = cv2.imread(str_background)
        rot_check = 0
        if i < len(comp_rotation_factor):
            rot_check = comp_rotation_factor[i]
        background = image_process_value(y, i, comp_x_multipliers[i],
        comp_y_multipliers[i], comp_scale[i], rot_check, script_dir, background)
        newer_names = str(i) + "et_new.png"
        image_consol.append(background)
        i = i + 1
    return image_consol

#'''
#image_process_value
#processes images and converts values to floats
#'''
def image_process_value(picture_array, my_counter, x_multiplier, y_multiplier, scale, rotation_factor, script_dir, background):
    i = 0
    count = 0
    image_1 = background
    for x in picture_array:
        x_pos_mult  = float(x_multiplier[count])
        y_pos_mult = float(y_multiplier[count])
        multiplier = float(scale[count])
        rot = float(rotation_factor[count])
        count = count + 1
        image_1 = malt_overlay_path(multiplier, x_pos_mult, y_pos_mult, rot, image_1, str(x), count)
    return image_1

#
#Main function
#Cakks image process and picture send functions
#
if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    my_p = os.path.join(script_dir, sys.argv[1])
    prostart = time.time()
    with open(my_p, 'r') as f:
      #my_p = os.path.join(script_dir, f)
      data = json.load(f)
    background = image_process(data)
    rate = data["transitionTime"]
    picture_send(background, rate, prostart)
