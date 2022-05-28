import numpy as np

import torch
from torch.autograd import Variable

from pathlib import Path
from STAR.star_module import STAR

import cv2



def get_image(path: Path, frame_no: int):
    cap = cv2.VideoCapture(str(path))
    num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if frame_no > num_frames:
        raise Exception()
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
    ret, frame = cap.read()
    if not ret:
        raise Exception()
    return frame


def test_star():
    batch_size = 32
    num_betas = 12
    
    poses = np.zeros((batch_size, 72))
    betas = np.zeros((batch_size, num_betas))
    trans = np.zeros((batch_size, 3))
    
    # poses[:, 1] = 3 * np.random.random(batch_size)

    star = STAR(num_betas=num_betas)
    poses = torch.cuda.FloatTensor(poses)
    poses = Variable(poses,requires_grad=True)
    betas = torch.cuda.FloatTensor(betas)
    betas = Variable(betas,requires_grad=True)
    trans = torch.cuda.FloatTensor(trans)
    trans = Variable(trans,requires_grad=True)

    d = star(poses, betas, trans)
    torch.cuda.synchronize()

	# print('output', d.shape)
	# print('poses', poses.shape)
	# print('betas', betas.shape)
	# print('trans', trans.shape)

    vertices = d.cpu().detach().numpy()
    # np.save('mesh.npy', vertices[0])
    
    faces = star.faces.numpy()
    
    from cl_wrapper import opencl_render
    colors, depths = opencl_render(vertices, faces)
    # print(vertices)
    # print(faces)
    
    for b in range(batch_size):
        img = colors[b]
        img = np.flip(img, 1)
        img = np.swapaxes(img, 0, 1)
        img = np.ascontiguousarray(img)
    
        cv2.imwrite(f"rendered/{b:05d}.png", img)


if __name__ == '__main__':
	test_star()
