<h2> YOLO-Breast-UltraSound-Images (Updated: 2023/04/14)</h2>

<p>
This is a simple tool to create YOLO BUSI (Breast UltraSound Images) Dataset from a BUSI Dataset 
with mask images (segmentations).
</p>
<p>
The original BUSI Dataset used here has been taken from the following web site:<br>
</p>

<b>Dataset-BUSI-with-GT</b><br>
<pre>
https://www.kaggle.com/datasets/aryashah2k/breast-ultrasound-images-dataset
</pre>


About Dataset (Taken from the above web site)<br>
<p>
Breast cancer is one of the most common causes of death among women worldwide. 
Early detection helps in reducing the number of early deaths. 
The data reviews the medical images of breast cancer using ultrasound scan. 
Breast Ultrasound Dataset is categorized into three classes: normal, benign, 
and malignant images. 
Breast ultrasound images can produce great results in classification, detection, 
and segmentation of breast cancer when combined with machine learning.
</p>
<b>Citation:</b>
<pre>
Al-Dhabyani W, Gomaa M, Khaled H, Fahmy A. 
Dataset of breast ultrasound images. Data in Brief. 
2020 Feb;28:104863. 
DOI: 10.1016/j.dib.2019.104863.
</pre>

<h2>1 Clone repository</h2>
 Please clone this repostory to your local PC.<br>
<pre>
>git clone https://github.com/sarah-antillia/YOLO-Breast-UltraSound-Images.git
</pre>

<h2>2 Dataset_BUSI_with_GT</h2>
Please download image dataset from the following, and expand it under your local 
repository <b>YOLO-BreastSound-Images</b>
<pre>
https://www.kaggle.com/datasets/aryashah2k/breast-ultrasound-images-dataset
</pre>

<pre>
YOLO-BREAST-ULTRASOUND-IMAGES
└─Dataset_BUSI_with_GT
</pre>

<h2>3 Create Master Dataset</h2>

Please run the following command to create master dataset.<br>
<pre>
>python create_augmented_master_512x512.py
</pre>

<a href="./create_augmented_master_512x512.py">This create_augmented_master_512x512.py</a> will create <b>BUSI_augmented_master_512x512</b> folder which contains <b>test, train, and valid</b> datasets from <b>Dataset_BUSI_with_GT</b>.<br>
<pre>
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
</pre>

<p>
1 This splits the original <b>Dataset_BUSI_with_GT</b> dataset to three subsets train, test and valid. 
with the ratios.
</p>
<pre>
 train: 0.5
 test:  0.3
 valid: 0.2
</pre>

<p>
2 Resize each image to 512x512
</p>
<p>
3 Augment each image in <b>train</b> dataset by rotating the image with an angle in the following range ANGLES, and save the rotated image as a jpg file.
</p>
<pre> 
ANGLES = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330]
</pre>
<p>
4 Flip each image horizontally and vertically in <b>train</b> dataset, and save the flipped image as a jpg file.
</p>

<p>
5 Save each image in <b>test</b> dataset as a jpg file without any augmentation.
</p>

<p>
6 Save each image in <b>valid</b> dataset as a jpg file without any augmentation.
</p>

<h2>4 Create YOLO Annotation</h2>
Please run the following command to create YOLO Annotation from <b>BUSI_augmented_master_512x512</b>.<br>
<pre>
>python create_yolo_annotation_from_augmented_master.py
</pre>
<a href="./create_yolo_annotation_from_augmented_master.py">This create_yolo_annotation_from_augmented_master.py</a> will create <b>YOLO</b> folder which contains <b>test, train, and valid</b> YOLO annotations
 from <b>BUSI_augmented_master_512x512</b> dataset.<br>
By finding the bounding boxes (rectangular region) from each mask-image in the 
train, test and valid dataset, we have created YOLO annotation for those subsets.<br>

<pre>
./YOLO/
├─test/
├─train/
└─valid/
</pre>

<b>Sample YOLO annotation in train:</b>
<br>
<img src="./asset/BUSI_YOLO_train_annotated.png"><br>

<br>
<h2>5 Download YOLO Dataset</h2>
<p>
You can download this YOLO Dataset (YOLO-BUSI-DATASET-20230414.zip) from
 <a href="https://drive.google.com/file/d/1IRSc7b3p6sF7ObI2wBk3Mo0ryhlJzKs7/view?usp=sharing">here</a>.
</p>

<h2>6 Download TFRecord Dataset</h2>
<p>
You can convert this YOLO dataset to TFRecord by using 
<a href="https://github.com/sarah-antillia/AnnotationConverters">AnnotationConverter</a>
<br>
You can alslo download TFRecord Dataset (TFRecord-BUSI-20230414.zip) from
 <a href="https://drive.google.com/file/d/1XaqPnH90ZQ9_FuwaUZSvwcUPWS7BdRvE/view?usp=sharing">here</a>.
</p>

<h2>7 Download COCO Dataset</h2>
<p>
You can convert this YOLO dataset to COCO by using 
<a href="https://github.com/sarah-antillia/AnnotationConverters">AnnotationConverter</a>
<br>
You can alslo download COCO Dataset (COCO-BUSI-20230414.zip) from
 <a href="https://drive.google.com/file/d/1jszrHyo91XcxKcuh6my-RIxpuz18_qEm/view?usp=sharing">here</a>.

</p>
