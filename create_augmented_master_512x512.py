# Copyright 2023 (C) antillia.com. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

#
# create_augmented_master_512x512.py
# 2023/04/12 Antillia.com Toshiyuki Arai
# 2023/04/13 Modified to pass a parameter augment_all to create_augmented_master_512x512 function.
# 
# 1 This splits the original Dataset_BUSI_with_GT dataset 
# to three subsets train, test and valid. 
# 
# 2 Resize each image to 512x512
#
# 3 Rotae each image in train dataset by angle in ANGLES = [0, 90, 180, 270]
#
# 4 Save each rotated image as a jpg file,
#   In this way, the orignal image dataset has been augumented.
#    
import sys
import os
import glob
import random
import shutil
import traceback
import cv2

def create_augmented_master_512x512(input_dir, output_dir, image_format=".jpg", augment_all=True):
  class_dirs = ["benign", "malignant"]
  for class_dir  in class_dirs:
    images_dir = os.path.join(input_dir, class_dir)
    pattern = images_dir + "/*mask.png"
    
    print("--- pattern {}".format(pattern))
    mask_files  = glob.glob(pattern)
    num_files   = len(mask_files)
    # 1 shuffle mask_files
    random.shuffle(mask_files)
    
    # 2 Compute the number of images to split
    # train= 0.5 test=0.3 valid=0.2
    num_train = int(num_files * 0.5)
    num_test  = int(num_files * 0.3)
    num_valid = int(num_files * 0.2)
    # 2023/04/13 Setting smaller rate on num_train before, 
    # because the train images are agumented not depending augment_all paramter.

    train_files = mask_files[0: num_train]
    test_files  = mask_files[num_train: num_train+num_test]
    valid_files = mask_files[num_train+num_test: num_files]

    print("=== number of train_files {}".format(len(train_files)))
    print("=== number of test_files  {}".format(len(test_files)))
    print("=== number of valid_files {}".format(len(valid_files)))

    # 1 Any way, augment the images in train_files.
    create_resized_rotated_flipped_files(images_dir, output_dir, class_dir, train_files, image_format, "train")
    
    if augment_all:
      # 2 Augment the images in test_files and valid_files provided augment_all is True.
      create_resized_rotated_flipped_files(images_dir, output_dir, class_dir, test_files,  image_format, "test")
      create_resized_rotated_flipped_files(images_dir, output_dir, class_dir, valid_files, image_format, "valid")
    else:
      # 3 Resize only the images in test_files and valid_files provided augment_all is False.
      create_resized_files(images_dir, output_dir, class_dir, test_files,  image_format, "test")
      create_resized_files(images_dir, output_dir, class_dir, valid_files, image_format, "valid")
   
# 1 Resize an original image to 512x512 size,
# 2 Rotate the resized_image by an angle in ANGLES    = [0, 90, 180, 270]
# 3 Save the rotated_resize_image as a JPG file.
# 4 Flip the resized_image by a flipcode in FLIPCODES = [0, 1] # 0: veritcal_flip, 1: horizontal_flip
# 5 Save the flipped_resized_image as a JPG file

def create_resized_rotated_flipped_files(images_dir, output_dir, class_dir, mask_files, image_format, target): 
  # target = train_or_test_or_valid_dir:

  output_class_dir  = os.path.join(output_dir, target)
  target_output_dir = os.path.join(output_class_dir, class_dir)
  if not os.path.exists(target_output_dir):
    os.makedirs(target_output_dir)
  W = 512
  H = 512
  for mask_file in mask_files:
    basename  = os.path.basename(mask_file)
    nameonly  = basename.split(".")[0]
    mask_img = cv2.imread(mask_file)
    # 1 Resize the mask_img to 512x512
    resized_mask_img  = cv2.resize(mask_img, (W, H), interpolation = cv2.INTER_LANCZOS4)
    
    extension = basename.split(".")[1]
 
    non_mask_filename  = basename.split("_")[0] + "." + extension
    non_mask_file_path = os.path.join(images_dir, non_mask_filename)

    non_mask_img = cv2.imread(non_mask_file_path)
    # 2 Resize the non_mask_img to 512x512
    resized_non_mask_img  = cv2.resize(non_mask_img, (W, H), interpolation = cv2.INTER_LANCZOS4)

    ANGLES = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330]

    for angle in ANGLES:
      center = (W/2, H/2)
      rotate_matrix = cv2.getRotationMatrix2D(center=center, angle=angle, scale=1)

      # 3 Rotate the resize_mask_img by angle
      rotated_resized_mask_image     = cv2.warpAffine(src=resized_mask_img,     M=rotate_matrix, dsize=(W, H))

      # 4 Rotate the resize_non_mask_img by angle
      rotated_resized_non_mask_image = cv2.warpAffine(src=resized_non_mask_img, M=rotate_matrix, dsize=(W, H))  

      rotated_mask_filename         = "rotated-" + str(angle) + "-" + nameonly + image_format
      rotated_resized_mask_img_file = os.path.join(target_output_dir, rotated_mask_filename)

      # 5 Write the rotated_resized_mask_image as a jpg file.
      cv2.imwrite(rotated_resized_mask_img_file, rotated_resized_mask_image)
      print("Saved {} ".format(rotated_resized_mask_img_file))

      non_mask_basename = basename.split("_")[0] + image_format
      rotated_non_mask_filename = "rotated-" + str(angle) + "-" + non_mask_basename

      rotated_resized_non_mask_img_file = os.path.join(target_output_dir, rotated_non_mask_filename)

      # 6 Write the rotated_resized_non_mask_image as a jpg file.
      cv2.imwrite(rotated_resized_non_mask_img_file, rotated_resized_non_mask_image)
      print("Saved {} ".format(rotated_resized_non_mask_img_file))

    FLIPCODES = [0, 1]
    for flipcode in FLIPCODES:
      # 7 Flip the resized_mask_img by flipcode
      flipped_resized_mask_img = cv2.flip(resized_mask_img, flipcode)
      # Save flipped mask_filename is jpg
      save_flipped_mask_filename = "flipped-" + str(flipcode) + "-" + nameonly + image_format
      flipped_resized_mask_img_file = os.path.join(target_output_dir, save_flipped_mask_filename)

      # 8 Write the flipped_resized_mask_img as a jpg file.
      cv2.imwrite(flipped_resized_mask_img_file, flipped_resized_mask_img)
      print("Saved {} ".format(flipped_resized_mask_img_file))
      
      # 9 Flip the resized_non_mask_img by flipcode
      # save_non_mask_basename is jpg 
      save_non_mask_filename = basename.split("_")[0] + image_format
      flipped_resized_non_mask_img = cv2.flip(resized_non_mask_img, flipcode)
      save_flipped_non_mask_filename = "flipped-" + str(flipcode) + "-" + save_non_mask_filename
      flipped_resized_non_mask_img_file = os.path.join(target_output_dir, save_flipped_non_mask_filename)

      # 10 Write the flipped_resized_non_mask_img as a jpg file.
      cv2.imwrite(flipped_resized_non_mask_img_file, flipped_resized_non_mask_img)
      print("Saved {} ".format(flipped_resized_non_mask_img_file))


def create_resized_files(images_dir, output_dir, class_dir, mask_files, image_format, target): 
  # target = train_or_test_or_valid_dir:

  output_class_dir  = os.path.join(output_dir, target)
  target_output_dir = os.path.join(output_class_dir, class_dir)
  if not os.path.exists(target_output_dir):
    os.makedirs(target_output_dir)
  W = 512
  H = 512
  for mask_file in mask_files:
    basename  = os.path.basename(mask_file)
    nameonly  = basename.split(".")[0]
    mask_img = cv2.imread(mask_file)
    # 1 Resize the mask_img to 512x512
    resized_mask_img  = cv2.resize(mask_img, (W, H), interpolation = cv2.INTER_LANCZOS4)
    save_resized_mask_filename = nameonly + image_format 

    resized_mask_img_filepath = os.path.join(target_output_dir, save_resized_mask_filename)
    # 2 Write the resized_mask_img as a jpg file.

    cv2.imwrite(resized_mask_img_filepath, resized_mask_img)
    print("Saved {} ".format(resized_mask_img_filepath))
    extension = basename.split(".")[1]
 
    non_mask_filename  = basename.split("_")[0] + "." + extension

    non_mask_img_filepath = os.path.join(images_dir, non_mask_filename)

    non_mask_img = cv2.imread(non_mask_img_filepath)
    # 3 Resize the non_mask_img to 512x512
    resized_non_mask_img  = cv2.resize(non_mask_img, (W, H), interpolation = cv2.INTER_LANCZOS4)
    save_non_mask_filename = basename.split("_")[0] + image_format

    resized_non_mask_img_filepath = os.path.join(target_output_dir, save_non_mask_filename)

    # 4 Write the resized_non_mask_img as a jpg file.
    cv2.imwrite(resized_non_mask_img_filepath, resized_non_mask_img)
    print("Saved {} ".format(resized_non_mask_img_filepath))

"""
Input:
./Dataset_BUSI_with_GT/
├─benign/
├─malignant/
└─normal/

"""

"""
Output:
./BUSI_augmented_master_512x512/
├─test/
│  ├─benign/
│  └─malignant/
├─train/
│  ├─benign/
│  └─malignant/
└─valid/
    ├─benign/
    └─malignant/      
      
"""

if __name__ == "__main__":
  try:
    input_dir  = "./Dataset_BUSI_with_GT"
    output_dir = "./BUSI_augmented_master_512x512"
    if not os.path.exists(input_dir):
      raise Exception("===NOT FOUND " + input_dir)
    if os.path.exists(output_dir):
      shutil.rmtree(output_dir)
    if not os.path.exists(output_dir):
      os.makedirs(output_dir)
      
    # create BUS_augmented_master_512x512 dataset train, test, valid 
    # from the orignal Dataset_BUSI_with_GT .
    create_augmented_master_512x512(input_dir, output_dir, image_format=".jpg", augment_all=False)

  except:
    traceback.print_exc()
    