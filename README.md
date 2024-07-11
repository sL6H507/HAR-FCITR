# This is our Senior Project,

Human Action Recognition using Yolo 

Installation
----
To install the packages just run 
 	`Setup.py`

  
For GPU installation please use this pip **NVIDIA ONLY!**

	pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

Next install the cudatoolkit 

https://developer.download.nvidia.com/compute/cuda/12.5.1/local_installers/cuda_12.5.1_555.85_windows.exe

for anaconda users

	conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia

 Dataset
 ----
 if you faced problems with default dataset [Click Here](https://universe.roboflow.com/realtime-human-action-recognition-in-still-images-c4ciq/real-time-human-action-recognition/dataset/7/download) and select YoloV9 > **download zip to computer**

Training
----
> Epochs : parameter that defines the number times that the learning algorithm will work through the entire training dataset.
> 
> Batch Size `Default = 16`: the number of samples that you feed into your model at each iteration **epoch** of the training process.
> 
> Image Size `Default = 640`: Target image size for training. All images are resized to this dimension before being fed into the model.
 
Predicting
----
> Confidence `Higher Better`: Sets the minimum confidence threshold for detections. Objects detected with confidence below this threshold will be disregarded. Adjusting this value can help reduce false positives.
> 
> Intersection Over Union (IoU) `Lower Better`:  threshold for Non-Maximum Suppression (NMS). Lower values result in fewer detections by eliminating overlapping boxes, useful for reducing duplicates.


 
