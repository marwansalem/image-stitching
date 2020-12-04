# importing the module 
import cv2 
import numpy as np
import matplotlib.pyplot as plt
from correspondences import get_image_path, get_correspondences, load_correspondences, write_correspondence_to_file
import tkinter as tk
from tkinter import filedialog, messagebox as mb
from homography import initialize_matrix_A, compute_H
# function to display the coordinates of
# of the points clicked on the image  




def save_dialog(title, filetypes):
    root = tk.Tk()
    dummy = root.withdraw()
    file_name = filedialog.asksaveasfilename(initialdir=".", title=title,
                                      filetypes=filetypes)
    return file_name



def show_points_on_image(img, window_name, points, marker_color=(255,0,0)):
    font = cv2.FONT_HERSHEY_SIMPLEX
    i = 1
    copy = img.copy()
    for point in points:
        x,y = point
        copy = cv2.putText(copy, str(i) , (x,y), font, 
                        0.75, marker_color, 2) 
        i +=1
    cv2.imshow(window_name, copy)

def stitch_image(image1_name, image2_name,first_points, second_points, show_correspondence=True):
    img1 = cv2.imread(image1_name)
    imgA = cv2.cvtColor(img1 ,cv2.COLOR_BGR2GRAY)
    img2 = cv2.imread(image2_name)
    
    imgB = cv2.cvtColor(img2 ,cv2.COLOR_BGR2GRAY)

    imgA = img1
    imgB = img2
    print(imgA.shape)
    points1, points2 = first_points, second_points
    
    if show_correspondence:
        #newA = cv2.resize(imgA, (2000, 1400)) 
        #newB = cv2.resize(imgB, (8000, 2800)) 
       
        show_points_on_image(imgA, 'First Image Points', points1)
        show_points_on_image(imgB, 'Second Image Points', points2, marker_color=(0, 0, 255))
        cv2.waitKey(0) 
        cv2.destroyAllWindows() 


        #H, masked = cv2.findHomography(points1, points2, cv2.RANSAC, 5.0)
        
        A = initialize_matrix_A(points1, points2)
        H = compute_H(A)

        dst = cv2.warpPerspective(imgA,H,(imgA.shape[1] + imgB.shape[1] ,  imgA.shape[0] + imgB.shape[0]))
        print(dst.shape)
        dst[0:imgB.shape[0], 0:imgB.shape[1]] = imgB
        cv2.imshow('output', dst)
        plt.show()
        plt.figure()

        #new = cv2.resize(dst, (8000, 2800)) 
        #print(new)
        #new = cv2.cvtColor(dst, cv2.COLOR_RGB2BGR)
        #cv2.imshow('resized', new)
        cv2.waitKey(0) 
        cv2.destroyAllWindows() 
        if len(imgA.shape) != 3:
            print(dst)
            print(dst.shape)
            dst =cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)

        return dst

  
# driver function 
if __name__=="__main__": 
  
    # reading the image 
    DEBUG = False

    # points1, points2 = load_correspondences('points.txt')

    # print(points1.shape)
    
    # A = initialize_matrix_A(points1, points2)
    # print(A.shape)
    # V = compute_H(A)

    # print(V.shape)
    # H, masked = cv2.findHomography(points1, points2, cv2.RANSAC, 5.0)
    # print(H/436.39)
    # print(np.linalg.norm(H.reshape(9,1)))
    # print(H.shape)
    if not DEBUG:
        image1_path = get_image_path("Select first image")
        image2_path = get_image_path("Select second image")

        dialog = mb.askyesno('Mark Points' , 'Mark points on images?(No: Load from text file)')
        if dialog:
            first_image_positions, second_image_positions = get_correspondences(image1_path,image2_path)
        else:
            root = tk.Tk()
            dummy = root.withdraw()
            points_path = filedialog.askopenfilename(initialdir = ".",title = 'Load points file',filetypes = (("all files","*.*"), ("png files","*.png"), ("txt files","*.txt")))
            first_image_positions, second_image_positions = load_correspondences(points_path)
        
        stitched_image = stitch_image(image1_path, image2_path, first_image_positions, second_image_positions)
        
        dialog = mb.askyesno('Save Image' , 'Save Stitched Image?')
        if dialog:
            file_name = save_dialog(title="Save Points:",filetypes=(("all files","*.*"),("png files","*.png"),("jpg files","*.jpg"),("jpeg files","*.jpeg")))
            if file_name is not False:
                cv2.imwrite(file_name, stitched_image)

        dialog = mb.askyesno('Save Correspondence as Text file?' , 'Save Points?')

        if dialog:
            file_name = save_dialog(title="Save Points:",filetypes=(("all files","*.*"),("txt files","*.txt")) )
            write_correspondence_to_file(file_name, first_image_positions, second_image_positions)






