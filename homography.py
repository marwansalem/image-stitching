import numpy as np

def initialize_A_i(p, p_dash):
    x, y = p
    x_dash, y_dash = p_dash
    A_i = np.array([-x, -y, -1, 0, 0, 0, x*x_dash, y*x_dash, x_dash,
                     0, 0, 0, -x,-y, -1, x*y_dash, y*y_dash, y_dash])
    
    A_i = A_i.reshape(2,9)
    
    return A_i

def initialize_matrix_A(points_1, points_2):
    num_points = len(points_1)
    A = []
    print(num_points)
    for i in range(num_points):
        p = points_1[i]
        p_dash = points_2[i]
        if i == 0:
            A = initialize_A_i(p, p_dash)
        else:
            A_i = initialize_A_i(p, p_dash)
            A = np.vstack((A, A_i))


    return A

def compute_H(A):
    U, singular_values, V = np.linalg.svd(A, full_matrices=True )
    
    # return the vector corresponding to the smallest singular value
    return V[-1].reshape(3,3)

if __name__=="__main__":
    pass

        
