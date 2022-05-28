
import numpy as np
# import ctypes
import cv2
import rendering


def opencl_render(vertices: np.ndarray, faces: np.ndarray, resolution=None):
    batch_size = vertices.shape[0]
    # vertices = vertices + np.array([0, 0, 0.5], dtype=np.float32)
    
    print(vertices.shape)
    print(faces.shape)
    
    if resolution is None:
        resolution = 1280, 720
        
    w, h = resolution
    colors = np.empty((batch_size, w, h, 3), dtype=np.uint8)
    depths = np.empty((batch_size, w, h), dtype=np.float32)
    indexes = np.empty((batch_size, w, h), dtype=np.int64)
    
    # print(vertices)
    # print(faces)
    
    rendering.render_wrapper(
        vertices=vertices,
        faces=faces,
        colors=colors,
        depths=depths)
    
    # rendering.indexes_wrapper(
    #     vertices=vertices,
    #     faces=faces,
    #     indexes=indexes)
    
    # print("Number of indexes >0", np.sum(indexes > 0))

    return colors, depths
    
    
    