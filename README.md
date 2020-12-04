# Image Stitching

## Introduction
Image stitching combines two or more image into a single image.  
This project is the second assignment for the Computer Vision course (Alexandria University).  



## How it works

## Requirements
This project requires the following python libraries:
* Numpy
* CV2
* Tkinter  
## Downloading the project
1. Clone the repository  
> git clone https://github.com/marwansalem/image-stitching  
2. Go to the project directory
> cd image-stitching
2. Run the code
> python stitch.py

## Guide
Upon running the project user asked to input the first image,  
then the second image.
![Load first image](tutorial/0.jpg)

Then user is asked either to mark the correspondence points on the image,
or to load it from a text file.  
![points prompt](tutorial/1.jpg)  
If the user choose to mark the points, the two images are opened in two windows,  
and the user can mark the corresponding points on the the two images using mouse clicks.  
After choosing the points press any keyboard key to continue.
### **4 points at least  must be chosen.**
![Mark points](tutorial/3.jpg)  
However, adding more points will generally make the result better.

If the user chooses not to mark the points, they can load them from a text file, which has the following format.  
The file must have a line for each pair of corresponding points. The line will be in this format: 
>**x1,y1,x2,y2**  

Where x1,y1 are the coordinates of the point in the first image, and x2,y2 are the coordinates of the corresponding points in the second image.  
A text file sample.
>106,575,577,610  
310,599,774,629  
107,505,570,544  
175,508,633,547  

After the correspondence points are marked or loaded from a file, they are shown on the two images, with the blue color for the first image, and red for the first image.
Then press enter to continue.
![Correspondence points](tutorial/4.jpg)  

### Finally the stitched image will be shown.
![Stitched image](tutorial/5.jpg)  

The user is asked whether save the output or not.  
![Save image prompt points](tutorial/6.jpg)  

Then is  asked whether save the correspondence points as  a text file or not.  
![Save points as text](tutorial/7.jpg)  
