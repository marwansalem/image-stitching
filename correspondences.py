import cv2 
import numpy as np
import tkinter as tk
from tkinter import filedialog

def load_correspondences(file_name):
    try:
        f = open(file_name, "r")
        lines = f.readlines()
        lines = [l.rstrip() for l in lines]
        f.close()

        points1 = []
        points2 = []
        for line in lines:
            x1,y1,x2,y2 = line.split(',')
            x1,y1,x2,y2 = int(x1), int(y1), int(x2), int(y2)
            points1.append( [x1, y1])
            points2.append( [x2, y2])
        points1 = np.array(points1, np.float32)
        points2 = np.array(points2, np.float32)
        
        return points1, points2
 
    except Exception as e:
        print(e)
        print('Cannot read file',file_name)
        return False, True

def record_click(event, x, y, flags, params): 
  
    # checking for left mouse clicks 
    if event == cv2.EVENT_LBUTTONDOWN: 

        

        postitions, marker_color, image, window_name = params
        font = cv2.FONT_HERSHEY_SIMPLEX 

        #append coordinates of click
        postitions.append( [x, y] )
        #increment counter
        count = len(postitions) 

        cv2.putText(image, str(count) , (x,y), font, 
                    0.75, marker_color, 2) 
        cv2.imshow(window_name, image)

def write_correspondence_to_file(file_name, first_positions, second_positions):
    f = open(file_name,"w")
    for i in range(len(first_positions)):
        p1, p2 = first_positions[i], second_positions[i]
        x1, y1 = p1
        x2, y2 = p2
        x1,y1,x2,y2 = int(x1), int(y1), int(x2), int(y2)
        line = f'{x1},{y1},{x2},{y2}\n'
        f.write(line)

    f.close()

def get_image_path(title):
    root = tk.Tk()
    dummy = root.withdraw()
    image_path = filedialog.askopenfilename(initialdir = ".",title = title,filetypes = (("all files","*.*"),("png files","*.png"),("jpg files","*.jpg"),("jpeg files","*.jpeg")))
    return image_path



    

def get_correspondences(image1_path, image2_path, points_filename='points.txt'):
    first_image = cv2.imread(image1_path, 1) 
    second_image = cv2.imread(image2_path,1)
    # displaying the image 
    first_window_name = 'First Image'
    second_window_name = 'Second Image'
    cv2.imshow(first_window_name, first_image) 
    cv2.imshow(second_window_name, second_image) 
    #setting up parameters to be passed to the mouse click event callback for each window
    first_image_positions = [] #list of points in first image
    first_color = (255, 0, 0) #mark the points in blue for first image

    second_image_positions = []
    second_color = (0, 0, 255) # mark points in red for the second image

    first_window_param = (first_image_positions, first_color, first_image, first_window_name)
    second_window_param = (second_image_positions, second_color, second_image, second_window_name)
    cv2.setMouseCallback(first_window_name, record_click,param=first_window_param )
    cv2.setMouseCallback(second_window_name, record_click,param=second_window_param )


    # wait for a key to be pressed to exit 
    cv2.waitKey(0) 
  
    # close the window 
    cv2.destroyAllWindows() 


    #ignore points that have no correspondence
    length = min(len(first_image_positions), len(second_image_positions))
    first_image_positions = first_image_positions[0:length]
    second_image_positions = second_image_positions[0:length]

    first_image_positions = np.array(first_image_positions, np.float32)
    second_image_positions = np.array(second_image_positions, np.float32)


    return first_image_positions, second_image_positions


