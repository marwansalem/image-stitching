# importing the module 
import cv2 
import numpy as np
import sys

from correspondences import get_image_path, get_correspondences, load_correspondences, write_correspondence_to_file
import tkinter as tk
from tkinter import filedialog, messagebox as mb
from homography import initialize_matrix_A, compute_H, image1_to_image2
from warp import *
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
    return copy

def stitch_image(image1_name, image2_name,first_points, second_points, show_correspondence=True):
    img1 = cv2.imread(image1_name)
    imgA = cv2.cvtColor(img1 ,cv2.COLOR_BGR2GRAY)
    img2 = cv2.imread(image2_name)
    
    imgB = cv2.cvtColor(img2 ,cv2.COLOR_BGR2GRAY)

    imgA = img1
    imgB = img2
    print(imgA.shape)
    points1, points2 = first_points, second_points
    
    A = initialize_matrix_A(points1, points2)
    H = compute_H(A)


    if show_correspondence:
        #newA = cv2.resize(imgA, (2000, 1400)) 
        #newB = cv2.resize(imgB, (8000, 2800)) 
       
        # show_points_on_image(imgA, 'First Image Points', points1)
        # show_points_on_image(imgB, 'Second Image Points', points2, marker_color=(0, 0, 255))
        copy = show_points_on_image(imgB,'Mapping',points2,marker_color=(0,0, 255))
        mapped_points = image1_to_image2(H, points1)
        show_points_on_image(copy,'Mapping', mapped_points)
        cv2.waitKey(0) 
        cv2.destroyAllWindows() 

    warped, x_min, y_min= warp_pipeline(H, imgA, imgB)
    
    #dst = cv2.warpPerspective(imgA,H,(imgA.shape[1] + imgB.shape[1] ,  imgA.shape[0] + imgB.shape[0]))
    start_x = 0
    if x_min < 0:
        start_x = int(-np.floor(x_min))
    start_y = 0
    if y_min < 0:
        start_y = int(-np.floor(y_min))
    dst = warped
    dst[start_y: start_y + imgB.shape[0], start_x:start_x + imgB.shape[1]] = imgB
    
    print(dst.shape)

    cv2.imshow('output', dst)


    cv2.waitKey(0) 
    cv2.destroyAllWindows() 
    if len(imgA.shape) != 3:
        dst =cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)

    return dst

def test_warp_combine():
    
    print('====Testing some functions===')
    points1, points2 = load_correspondences('pointsperfect.txt')

    imgA = cv2.imread('image1.jpg')
    imgB= cv2.imread('image2.jpg')

    A = initialize_matrix_A(points1, points2)
    H = compute_H(A)
    warped, x_min, y_min = warp_pipeline(H, imgA, imgB)
    cv2.imshow('warped', warped)
    #cv2.imwrite('warpedshift.jpg', warped)
    start_x = 0
    if x_min < 0:
        start_x = int(-np.floor(x_min))
    start_y = 0
    if y_min < 0:
        start_y = int(-np.floor(y_min))
    
    print('B shape', imgB.shape)
    print('warped shape', warped.shape)

    print('xstart', start_x)
    print('xstart + W', start_x + imgB.shape[1])
    print('ystart', start_y)
    print('ystart + H', start_y + imgB.shape[0])

    warped[start_y: start_y + imgB.shape[0], start_x:start_x + imgB.shape[1]] = imgB
    #warped[0: imgA.shape[0], 0:imgA.shape[1]] = imgA
    
    cv2.imshow('comb', warped)
    #cv2.imwrite('combo.jpg', warped)
    cv2.waitKey(0) 
    cv2.destroyAllWindows()
    #######

    #warped_image = inverse_warp(H, warped_image, imgA, mask)
    #print(warped_image)
    #print(np.where(warped_image == 0)[0].shape)
    #cv2.imshow('TEST warped', warped_image)
    #cv2.imwrite('testwarpedrev.jpg', warped_image)


    print('===Testing Complete===')

  
# driver function 
if __name__=="__main__": 
  
    DEBUG = False
    
    if len(sys.argv) > 1:
        if sys.argv[1] == 'debug':
            DEBUG == True
    if not DEBUG :
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






