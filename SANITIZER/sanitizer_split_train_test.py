# USAGE
# python3 cheese_split_train.py -i all_images/ -o output/ -s 0.75 -tf 1

# import the necessary packages
from __future__ import print_function
from imutils import paths
import traceback
import argparse
import imutils
import numpy as np
import random
import cv2
import os
import shutil

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", required=True, help="path to the images to be classified")
ap.add_argument("-o", "--output", required=True, help="path to the output output directory for training/testing samples")
ap.add_argument('-s', '--train-percentage', type=float, default=0.50, help='percent of images to include as training')
ap.add_argument('-tf, --tensorflow-enabled', type=int, required=False, default=-1, help='enter number >1 if want to copy train/test to seperate directory with "loose image and annotation files"')
args = vars(ap.parse_args())

# if the output directory exists, delete it
if os.path.exists(args['output']):
    shutil.rmtree(args['output'])

# create the output directories
if not os.path.exists(args['output']):
    os.mkdir(args['output'])
    os.mkdir(args['output'] + '/train')
    os.mkdir(args['output'] + '/test')

# randomly select a portion of the images
imagePaths = list(paths.list_images(args["images"]))
random.shuffle(imagePaths)
i = int(len(imagePaths) * args['train_percentage'])

# define test/train splits
trainPaths = imagePaths[:i]
testPaths = imagePaths[i:]
print('Train Path Length: {}'.format(len(trainPaths)), '\nTest Path Length: {}'.format(len(testPaths)))

# initialize counters and error path list
train_success = 0
train_fail = 0
train_error_list = []

# loop over trainPaths and copy images + corresponding .xml to output/train dir
for trainPath in trainPaths:
    annot = trainPath.replace('.jpg', '.xml')
    try:
        shutil.copy(trainPath, os.path.join(args['output'], 'train'))
        shutil.copy(annot, os.path.join(args['output'], 'train'))
        train_success += 1
    except:
        print('problem....')
        train_error_list.append(trainPath)
        train_fail += 1

# initialize counters and error path list
test_success = 0
test_fail = 0
test_error_list = []

# loop over testPaths and copy images + corresponding .xml to output/test dir
for testPath in testPaths:
    annot = testPath.replace('.jpg', '.xml')
    try:
        shutil.copy(testPath, os.path.join(args['output'], 'test'))
        shutil.copy(annot, os.path.join(args['output'], 'test'))
        test_success += 1
    except:
        print('problem....')
        error_list.append(testPath)
        test_fail += 1

print('Train Success: {}'.format(train_success), '\nTrain Fail: {}'.format(train_fail))
print('Test Success: {}'.format(test_success), '\nTest Fail: {}'.format(test_fail))
if train_error_list:
    print('Train error list: ', train_error_list)
if test_error_list:
    print('Test error list: ', test_error_list)

# if args['tensorflow_enabled'] > 0:
#     paths = list(paths.list_files(os.path.join(args['output'], 'test')
#     print([i for i in paths])
