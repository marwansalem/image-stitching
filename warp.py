import cv2
import numpy as np

# warp each position into the position in the output frame
def warp_first_image_points(H, imgA):
    '''
    Computes the warped coordinates for an image, using homography
    matrix H
    '''
    W, H, C= imgA.shape

    mapped_points = []
    for x in range(W):
        for y in range(H):
            p = np.array([x, y, 1]).reshape(3,1)
            p_dash = np.matmul(H, p)
            x_dash, y_dash, w = p_dash[:, 0]
            x_dash /= w
            y_dash /= w
            mapped_points.append(np.array([x_dash, y_dash]))
    #there are W*H mapped points
    mapped_points =np.array(mapped_points).reshape(W, H)
    return mapped_points

    
def inverse_warp(H, warped_image, source_image):
    '''
    Fill out the holes (black pixels) in the warped image
    '''
    H_inv = np.linalg.pinv(H)
    H, W, C = warped_image.shape
    
    for c in range(C):
        for x in range(W):
            for y in range(H):
                pixel_value = warped_image[x , y, c]
                if pixel_value == 0:
                    p_dash = np.array([x, y, 1]).reshape(3,1)
                    p_src = np.matmul(H_inv, p_dash)
                    x_src, y_src, w_src = p_src[:, 0]
                    x_src = int(x_src/w_src)
                    y_src = int(y_src/w_src)
                    try:
                        warped_image[x , y, c] = source_image[x_src, y_src, c]
                    except:
                        # if x_src, y_src are subpixel values or out of range will need to do something
                        pass
    
    return warped_image
    
                    


    