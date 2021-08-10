import numpy as np
import math
import cv2
import os


#Overlay_Tester.py
#Test code for image placement, will place features and save them as an image
#
#

#
#
#
#
def malt_overlay_path(multiplier, x_pos_mult, y_pos_mult, image_1, str_foreground, count):
    print(count)
    image_3 = cv2.imread(str_foreground, cv2.IMREAD_UNCHANGED)
    cv2.imwrite("test.jpg", image_3)

    if count == 1:
        ones = np.ones((image_1.shape[0], image_1.shape[1]))*255
        image_1 = np.dstack([image_1, ones])
    ## Smart resizing function
    h, w, c = image_1.shape
    start_h = math.floor(h*y_pos_mult)
    start_w  = math.floor(w*x_pos_mult)
    ## Smart resizing function
    h3, w3, c3 = image_3.shape
    w4 = math.floor(w3*multiplier)
    h4 = math.floor(h3*multiplier)

    resized_image_3 = cv2.resize(image_3, dsize=(w4, h4))
    h5, w5, c4 = resized_image_3.shape
    #image_1[150:250, 150:250] = resized_image_3
    alpha_image_3 = resized_image_3[:, :, 3] / 255.0
    alpha_image = 1 - alpha_image_3
    for c in range(0, 3):
        image_1[start_h:start_h+h5, start_w:start_w+w5, c] = ((alpha_image*image_1[start_h:start_h+h5, start_w:start_w+w5, c]) + (alpha_image_3*resized_image_3[:, :, c]))
    # Filename
    filename = str(count) + 'savedImage.png'
    return image_1

if __name__ == '__main__':

    #Features are directly 

    left_pupil = "images/pupil.png"
    left_spot = "images/spot.png"
    right_pupil = "images/pupil.png"
    right_spot = "images/spot.png"
    my_background = "images/background.jpg"

    l_6 = "images/6.png"
    l_5 = "images/5.png"
    l_4 = "images/4.png"
    l_3 = "images/3.png"
    l_2 = "images/2.png"
    l_1 = "images/1.png"

    r_6 = "images/right/6.png"
    r_5 = "images/right/5.png"
    r_4 = "images/right/4.png"
    r_3 = "images/right/3.png"
    r_2 = "images/right/2.png"
    r_1 = "images/right/1.png"

    #Mouth pieces
    neu = "images/Mouth/neutral.png"
    #upper 1 --------------
    u_1 = "images/Mouth/upper/1.png"
    u_2 = "images/Mouth/upper/2.png"
    u_3 = "images/Mouth/upper/3.png"
    u_4 = "images/Mouth/upper/4.png"
    u_5 = "images/Mouth/upper/5.png"
    u_6 = "images/Mouth/upper/6.png"
    #lower 1 --------------
    l_1 = "images/Mouth/lower/1.png"
    l_2 = "images/Mouth/lower/2.png"
    l_3 = "images/Mouth/lower/3.png"
    l_4 = "images/Mouth/lower/4.png"
    l_5 = "images/Mouth/lower/5.png"
    l_6 = "images/Mouth/lower/6.png"


    eye_motions = [l_1,l_2, l_3, l_4, l_5, l_6, r_1, r_2, r_3, r_4, r_5,r_6]
    pupils = [left_pupil, right_pupil]
    spots = [left_spot, right_spot]

    #Shift through iterations
    lid_array_1 = [pupils[0], eye_motions[5], spots[0], pupils[1], eye_motions[11], spots[1], neu, l_6]
    x_multiplier = [.6, .55, .65, .3, .25, .35, .4, .4]
    y_multiplier = [.3, .25, .35, .3, .25, .35, .5, .5]

    ##Set Parameters
    script_dir = os.path.dirname(os.path.abspath(__file__))
    str_background = os.path.join(script_dir, "background1.jpg")
    str_foreground = os.path.join(script_dir, "4.png")
    print(str_background)
    print(str_foreground)

    count = 0
    image_1 = cv2.imread(str_background)
    for x in lid_array_1:
        print(str(x))
        x_pos_mult  = x_multiplier[count]
        y_pos_mult = y_multiplier[count]
        count = count + 1
        x = os.path.join(script_dir, x)
        if (count == 3 or count == 6):
            multiplier = .05
        else:
            multiplier = .45
        image_1 = malt_overlay_path(multiplier, x_pos_mult, y_pos_mult, image_1, str(x), count)
        # Filename
        filename = (str(count) + 'savedImage.png')
        image_1 = np.uint8(image_1)
        cv2.imwrite(filename, image_1)
