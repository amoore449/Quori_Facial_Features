# Quori_Facial_Features

This sub-repository contains files for the simulation of Facial Features for Gazebo and Quori. 
- Image Processing: Main file for converting images file JSON to Gazebo. Send sets of files here.
- Overlay_Tester: Test file for placement of features from a JSON file. Will save features to an independent format.
- images: a folder of base facial features for Quori's facial features. These can be replaced by alternative images if necessary. 
- JSON: A folder of base traits expressions for JSON

## Installing Basic Software
---- 
Reference the guide for getting started with Quori and VirtualBox and VMware [here](https://github.com/CMU-RASL/quori).

## Installing Facial Features
1. To install Git: sudo apt-get update and sudo apt-get install git-core
2. Create a directory in Home (for example, quori_files/src) and open a terminal inside it
3. Clone the repository with git clone https://github.com/CMU-RASL/quori.git
4. sudo apt install python3-pip
5. pip3 install --upgrade pip
6. python3 -m pip install opencv-python
7. Make sure to switch to the branch you want to be working on before making any changes

# Positioning Facial Features
In each frame of a facial feature, five features can be specified: file, x_multiplier, y_multiplier, scale_factor, and rotation_factor.
- file: Specifies the file path to the file path for a given image
- x_multiplier: specifies how far from 0 to 1 (left to right)
- y_multiplier: specifies how far from 0 to 1 (top to bottom) 
- scale_factor: Resizes the image by the specified factor
- rotation_factor: Rotates the image by the specified factor

```
            {
               "file":"images/right_brow/b_neutral.png",
               "x_multiplier":0.43,
               "y_multiplier":0.2,
               "scale_factor":0.3,
               "rotation_factor":0
            }
```

### Feature Animations

Each facial feature holds an array of feature frames within the JSON file. In each frame, each feature can be moved or specified.

```
  "Upper_Lip":[
         {
            "file":"images/Mouth/neutral.png",
            "x_multiplier":0.4,
            "y_multiplier":0.5,
            "scale_factor":0.6,
            "rotation_factor":0
         },
         {
           "file":"images/Mouth/upper/1.png",
           "x_multiplier":0.4,
           "y_multiplier":0.5,
           "scale_factor":0.6,
           "rotation_factor":0
         },
         {
           "file":"images/Mouth/upper/2.png",
           "x_multiplier":0.4,
           "y_multiplier":0.5,
           "scale_factor":0.6,
           "rotation_factor":0
         }
      ]
 ```
 
 This can also be shortened by only specifying variables that are changed. For example, this syntex is also valid:
 
 ```
  "Upper_Lip":[
         {
            "file":"images/Mouth/neutral.png",
            "x_multiplier":0.4,
            "y_multiplier":0.5,
            "scale_factor":0.6,
            "rotation_factor":0
         },
         {
           "file":"images/Mouth/upper/1.png"
         },
         {
           "file":"images/Mouth/upper/2.png"
         }
      ]
 ```
 
 Alternatively, if a feature is not changed or not changed after a certain number of stills, the last specified still will repeat until the end of the animation. 
 
 For example, if the total animation for this file is 13 frames, the image "images/Mouth/upper/1.png" with an x_multiplier of "0.4", a y_multiplier of "0.5", a scale_factor of  .6", and a rotation factor of "0" for the last 12 frames and the image "images/Mouth/neutral.png" with the same positioning for the first frame.
  ```
  "Upper_Lip":[
         {
            "file":"images/Mouth/neutral.png",
            "x_multiplier":0.4,
            "y_multiplier":0.5,
            "scale_factor":0.6,
            "rotation_factor":0
         },
           {
           "file":"images/Mouth/upper/1.png"
         }
      ]
 ```
 
