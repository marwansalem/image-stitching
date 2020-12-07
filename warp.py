import cv2
import numpy as np

# warp each position into the position in the output frame
def warp_first_image_points(H_mat, imgA):
    '''
    Computes the warped coordinates for an image, using homography
    matrix H
    '''
    W, H, C= imgA.shape

    mapped_points = []
    for x in range(W):
        for y in range(H):
            p = np.array([x, y, 1]).reshape(3,1)
            p_dash = np.matmul(H_mat, p)
            x_dash, y_dash, w = p_dash[:, 0]
            x_dash /= w
            y_dash /= w
            mapped_points.append(np.array([x_dash, y_dash]))
    #there are W*H mapped points
    mapped_points =np.array(mapped_points).reshape(W, H)
    return mapped_points


def apply_forward_warp(first_image, mapped_points, second_image_shape):
    W, H, C = second_image_shape
    warped_image = np.zeros(second_image_shape, dtype=np.uint16)
    averaging_weight = np.zeros(second_image_shape, dtype=np.uint16)

    W_src, H_src, C_src = first_image.shape

    for x_src in range(W_src):
        for y_src in range(H_src):
            for c_src in range(C_src):
                x, y = mapped_points[x_src, y_src]
                try:
                    warped_image[x, y, c_src] += first_image[x_src, y_src, c_src]
                    averaging_weight[x, y, c_src] += 1
                except:
                    # exception will be raised if x or y are sub pixel values or out x>=W y>=H
                    pass
    
    for x in range(W):
        for y in range(H):
            for c in range(C):
                w = averaging_weight[x, y, c]
                if w > 1:
                    warped_image[x, y, c] //= w
    return warped_image
    #apply splatting
    

    
def inverse_warp(H, warped_image, source_image):
    '''
    Fill out the holes (black pixels) in the warped image
    '''
    H_inv = np.linalg.pinv(H)
    W, H, C = warped_image.shape
    W_src, H_src, C_src = source_image.shape

    
    for c in range(C):
        for x in range(W):
            for y in range(H):
                pixel_value = warped_image[x , y, c]
                if pixel_value == 0:
                    p_dash = np.array([x, y, 1]).reshape(3,1)
                    p_src = np.matmul(H_inv, p_dash)
                    x_src, y_src, w_src = p_src[:, 0]
                    x_src = x_src/w_src
                    y_src = y_src/w_src
                    try:
                        warped_image[x, y, c] = source_image[x_src, y_src, c]
                    except:
                        # if x_src, y_src are subpixel values or out of range will need to do something
                        # bilinear interpolation for inverse warp
                        pass
    
    return warped_image
    
                    


    