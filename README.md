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
In each frame of a facial feature, five features can be specified:
```
            {
               "file":"images/right_brow/b_neutral.png",
               "x_multiplier":0.43,
               "y_multiplier":0.2,
               "scale_factor":0.3,
               "rotation_factor":0
            }
```
