import cv2
import numpy as np

# warp each position into the position in the output frame


def warp_first_image_points(H_mat, imgA):
    '''
    Computes the warped coordinates for an image, using homography
    matrix H
    '''
    H, W, C = imgA.shape

    #mapped_points = []
    x_values = []
    y_values = []


    for x in range(W):
        for y in range(H):
            p = np.array([x, y, 1]).reshape(3, 1)
            p_dash = np.matmul(H_mat, p)
            x_dash, y_dash, w = p_dash[:, 0]
            x_dash /= w
            y_dash /= w
            #mapped_points.append((x_dash, y_dash))
            x_values.append(x_dash)
            y_values.append(y_dash)
    # there are W*H mapped points
    #mapped_points = np.array(mapped_points).reshape(2 * W, H)
    x_values = np.array(x_values).reshape(W, H)
    y_values = np.array(y_values).reshape(W, H)

    return x_values, y_values


def apply_forward_warp(first_image, mapped_points, output_image_shape):
    H, W, C = output_image_shape
    #print('out_image_shape',output_image_shape)
    #print('first_image_shape', first_image.shape)
    warped_image = np.zeros(output_image_shape, dtype=np.uint16)
    #mask = np.bool(output_image_shape)
    averaging_weight = np.zeros(output_image_shape, dtype=np.uint16)

    H_src, W_src, C_src = first_image.shape

    x_values, y_values = mapped_points
    print('before loop1')
    for x_src in range(W_src):
        for y_src in range(H_src):
            for c_src in range(C_src):
                x, y = x_values[x_src, y_src], y_values[x_src, y_src]
                if x == int(x) and y == int(y) and (x < W and x >= 0 and x < H and y >= 0):
                    x, y = int(x), int(y)
                    warped_image[y, x, c_src] += first_image[y_src, x_src, c_src]
                    averaging_weight[y, x, c_src] += 1
                else:
                    # exception will be raised if x or y are sub pixel values or out x>=W y>=H
                    x_ceil = int(np.ceil(x))
                    x_floor = int(np.floor(x)) #, dtype=np.int16)
                    y_ceil = int(np.ceil(y))
                    y_floor = int(np.floor(y))
                    ptA = (x_ceil, y_floor)
                    ptB = (x_ceil, y_ceil)
                    ptC = (x_floor, y_floor)
                    ptD = (x_floor, y_ceil)
                    pts = [ptA, ptB, ptC, ptD]
                    for pt in pts:
                        if pt[0] >= W or pt[0] < 0 or pt[1] >= H or pt[1] < 0:
                            continue
                        ### what in the world is splatting
                        warped_image[pt[1], pt[0], c_src] += first_image[y_src, x_src, c_src]
                        averaging_weight[pt[1], pt[0], c_src] += 1
    print('before loop2')
    #empty_pos
    # for x in range(W):
    #     for y in range(H):
    #         for c in range(C):
    #             w = averaging_weight[x, y, c]
    #             if w > 1:
    #                 warped_image[x, y, c] //= w
                
    #             if w !=0:
    #                 pass
    eps = 0.0000000001
    # added small value to avoid integer division
    warped_image = np.where(averaging_weight > 1, warped_image//(averaging_weight + eps), warped_image)
    warped_image = warped_image.astype(np.uint8)
    return warped_image, averaging_weight[:, :, 0]
    # apply splatting


def inverse_warp(H, warped_image, source_image, mask):
    '''
    Fill out the holes (black pixels) in the warped image
    '''
    H_inv = np.linalg.pinv(H)
    W, H, C = warped_image.shape
    W_src, H_src, C_src = source_image.shape

    for c in range(C):
        for x in range(W):
            for y in range(H):
                pixel_value = warped_image[x, y, c]
                if mask[x, y] == 0:
                    p_dash = np.array([x, y, 1]).reshape(3, 1)
                    p_src = np.matmul(H_inv, p_dash)
                    x_src, y_src, w_src = p_src[:, 0]
                    x_src = x_src/w_src
                    y_src = y_src/w_src
                    if x_src == int(x_src) and y_src == int(y_src) and (x_src < W_src and x_src >= 0 and x_src < H_src and y_src >= 0):
                        warped_image[x, y, c] = source_image[x_src, y_src, c]
                    else:
                        # if x_src, y_src are subpixel values or out of range will need to do something
                        # bilinear interpolation for inverse warp
                        x_ceil = int(np.ceil(x_src))
                        x_floor = int(np.floor(x_src))
                        y_ceil = int(np.ceil(y_src))
                        y_floor = int(np.floor(y_src))
                        ptA = (x_ceil, y_floor)
                        ptB = (x_ceil, y_ceil)
                        ptC = (x_floor, y_floor)
                        ptD = (x_floor, y_ceil)
                        pts = [ptA, ptB, ptC, ptD]
                        for pt in pts:
                            if pt[0] >= W_src or pt[0] < 0 or pt[1] >= H_src or pt[1] < 0:
                                continue
                            ratio = abs(x_src-pt[0]) * abs(y_src-pt[1])
                            intensity = ratio * source_image[pt[0], pt[1], c]
                            warped_image[x, y, c] += intensity

    return warped_image


def warp_pipeline(H_matrix, first_image, second_image):
    mapped_points = warp_first_image_points(H_matrix, first_image)
    output_image_shape = (first_image.shape[0]+ second_image.shape[0], first_image.shape[1] + second_image.shape[1], first_image.shape[2])
    x_vals, y_vals = mapped_points
    x_min, y_min = np.min(x_vals), np.min(y_vals)

    if x_min < 0:
        x_vals += -x_min
    if y_min < 0:
        y_vals += -y_min

    mapped_points = (x_vals, y_vals)

    warped_image, mask = apply_forward_warp(first_image, mapped_points, output_image_shape)

    return warped_image, x_min, y_min
