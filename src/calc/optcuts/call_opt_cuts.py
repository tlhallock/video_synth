import torch
import os
import numpy as np

 
'''

./OptCuts_bin 10 human.obj 0.999 1 0 4.1 1 0 anotherStringILike

'''


def get_faces():
    base_dir = '/work/ProjectsForFun/pgen/video_synth/src/external/star/star_1_1/'
    path_model = os.path.join(base_dir, 'male', 'model.npz')
    star_model = np.load(path_model, allow_pickle=True)
    faces = torch.from_numpy(star_model['f'].astype(np.int64))
    return faces

def get_vertices():
    path = '/work/ProjectsForFun/pgen/video_synth/src/external/optcuts/mesh.npy'
    mat = np.load(path)
    return mat


def write():
    vertices = get_vertices()
    faces = get_faces()
    with open("human.obj", "w") as outf:
        for vertex in vertices:
            outf.write(f"v {vertex[0]} {vertex[1]} {vertex[2]}\n")
        for face in faces:
            outf.write(f"f {face[0]+1} {face[1]+1} {face[2]+1}\n")
    
    print(vertices.shape)


def read():
    vertices = get_vertices()
    faces = get_faces()
    p = '/work/ProjectsForFun/pgen/video_synth/src/external/optcuts/output/human_Tutte_0.999_1_OptCuts_theStringILike/finalResult_mesh_normalizedUV.obj'
    
    num_faces = faces.shape[0]
    
    uvs = []
    with open(p, "r") as infile:
        for line in infile:
            if not line.startswith('vt '):
                continue
            uvs.append(
                [float(v) for v in line.split()[1:]])

    tex_coords = np.array(uvs, dtype=np.float64)
    
    face_uv_coords = np.empty(
        (num_faces, 3),
        dtype=np.uint64)
    
    face_idx = 0
    with open(p, "r") as infile:
        for line in infile:
            if not line.startswith('f '):
                continue
            face_idxs = [
                int(pair.split("/")[0]) - 1
                for pair in line.split()[1:]
            ]
            face_uvs = [
                int(pair.split("/")[1]) - 1
                for pair in line.split()[1:]
            ]
            for i in range(3):
                if faces[face_idx][i] != face_idxs[i]:
                    raise Exception()
            face_uv_coords[face_idx, :] = face_uvs
            face_idx += 1
    np.savez_compressed(
        "uvs.npz", t=tex_coords, f=face_uv_coords)


if __name__ == "__main__":
    # main()
    read()
