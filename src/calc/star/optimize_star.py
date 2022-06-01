import numpy as np

import torch
from torch.autograd import Variable

from pathlib import Path
from STAR.star_module import STAR

import cv2

from cl_wrapper import opencl_render


def write_poses(frame):
    batch_size = 1
    num_betas = 12
    
    star = STAR(num_betas=num_betas, gender="male")
    for idx in range(72):
        poses = np.zeros((batch_size, 72))
        betas = np.zeros((batch_size, num_betas))
        trans = np.zeros((batch_size, 3))
    
        poses[0, idx] = 1
        trans = np.array([
            [0, 0, 2],
        ], dtype=np.float32)

        poses = torch.cuda.FloatTensor(poses)
        poses = Variable(poses,requires_grad=True)
        betas = torch.cuda.FloatTensor(betas)
        betas = Variable(betas,requires_grad=True)
        trans = torch.cuda.FloatTensor(trans)
        trans = Variable(trans,requires_grad=True)

        d = star(poses, betas, trans)
        torch.cuda.synchronize()

        vertices = d.cpu().detach().numpy()
        faces = star.faces.numpy()
        
        resolution = (frame.shape[1], frame.shape[0])
        colors, depths = opencl_render(vertices, faces, resolution)
        
        cv2.imwrite(f"output/pose_{idx:03d}_end.png", to_cv(colors[0]))


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



def to_cv(img):
    img = np.flip(img, 1)
    img = np.swapaxes(img, 0, 1)
    img = np.ascontiguousarray(img)
    return img


def normalize_rows(mat):
    return mat / np.linalg.norm(mat, axis=0)[np.newaxis, :]


def fit(frame, foreground):
    num_betas = 12
    
    betas = np.zeros(num_betas)
    trans = np.array(
        [-0.18, -0.3, 0.75],
        dtype=np.float32)
    
    poses = np.zeros(72)
    poses[41] = -0.45
    poses[44] = 0.45
    poses[56] = 2
    poses[59] = -2

    star = STAR(num_betas=num_betas, gender="male")
    
    batch_size = 64
    
    f = foreground
    f = np.expand_dims(f, 0)
    f = np.tile(f, [batch_size, 1, 1, 1])
    f = np.reshape(f, [batch_size, -1])
    print(f.shape)
    
    reps = 0
    pdelta, bdelta, tdelta = 0.01, 0.001, 0.0001
    for it in range(1000):
        pdir = np.random.random((batch_size, 72))
        bdir = np.random.random((batch_size, num_betas))
        tdir = np.random.random((batch_size, 3))
        
        pdir = normalize_rows(pdir)
        bdir = normalize_rows(bdir)
        tdir = normalize_rows(tdir)
        
        # ensure the first one doesn't change...
        pdir[0, :] = 0
        bdir[0, :] = 0
        tdir[0, :] = 0
        
        pdir = pdelta * pdir
        bdir = bdelta * bdir
        tdir = tdelta * tdir
        
        tposes = poses + pdir
        tbetas = betas + bdir
        ttrans = trans + tdir
        
        tposes = torch.cuda.FloatTensor(tposes)
        tposes = Variable(tposes,requires_grad=False)
        tbetas = torch.cuda.FloatTensor(tbetas)
        tbetas = Variable(tbetas,requires_grad=False)
        ttrans = torch.cuda.FloatTensor(ttrans)
        ttrans = Variable(ttrans, requires_grad=False)

        d = star(tposes, tbetas, ttrans)
        torch.cuda.synchronize()
        vertices = d.cpu().detach().numpy()
        faces = star.faces.numpy()
        resolution = (frame.shape[1], frame.shape[0])
        colors, depths = opencl_render(vertices, faces, resolution)
        
        imgs = colors
        imgs = np.flip(imgs, 2)
        imgs = np.swapaxes(imgs, 1, 2)
        imgs = np.ascontiguousarray(imgs)
        
        err = imgs
        err = np.reshape(err, [batch_size, -1])
        err = f - err
        err = np.square(err)
        err = np.sum(err, 1)
        print(err - err[0])
        min_idx = np.argmin(err)
        
        for alt in range(batch_size):
            cv2.imwrite(
                f"output/it_alt_{it:05d}_{alt:03d}.png",
                0.5 * frame + 0.5 * imgs[alt])
        
        if min_idx == 0:
            reps += 1
            if reps > 50:
                pdelta, bdelta, tdelta = pdelta / 2, bdelta / 2, tdelta / 2
                print("=========================================================")
                print("decreasing radius")
                print("=========================================================")
                reps = 0
            continue
        
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("found improvement")
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    
        reps = 0
        poses = poses + pdir[min_idx]
        betas = betas + bdir[min_idx]
        trans = trans + tdir[min_idx]
        
        for alt in range(batch_size):
            cv2.imwrite(
                f"output/improvement_{it:05d}_alpha.png",
                0.5 * foreground + 0.5 * imgs[min_idx])
            cv2.imwrite(
                f"output/improvement_{it:05d}_color.png",
                0.5 * frame + 0.5 * imgs[min_idx])
        
        
        


def main():
    path = "/work/ProjectsForFun/pgen/videos/inputs/my_video-5.mkv"
    frame = get_image(path, 50)
    
    path = "/work/ProjectsForFun/pgen/videos/outputs/alpha.mp4"
    foreground = get_image(path, 50)
    
    cv2.imwrite("output/begin.png", frame)
    fit(frame, foreground)


if __name__ == '__main__':
	main()
