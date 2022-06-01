import numpy as np


import cv2
import torch
from torch.autograd import Variable

from third_party.star.STAR.star_module import STAR


def run_star(poses, betas, trans):
    num_betas = betas.shape[1]

    star = STAR(num_betas=num_betas)
    poses = torch.cuda.FloatTensor(poses)
    poses = Variable(poses, requires_grad=True)
    betas = torch.cuda.FloatTensor(betas)
    betas = Variable(betas, requires_grad=True)
    trans = torch.cuda.FloatTensor(trans)
    trans = Variable(trans, requires_grad=True)

    result = star(poses, betas, trans)
    torch.cuda.synchronize()
 
 
def read_frame(path: str, frame_no: int) -> np.ndarray:
    cap = cv2.VideoCapture(path)
    frame_count = int(cap.get(cv2. CAP_PROP_FRAME_COUNT))
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
    ret, frame = cap.read()
    if not ret:
        print('error')
    return frame
 
 
def main():
    path = '/work/ProjectsForFun/pgen/videos/inputs/my_video-5.mkv'
    frame = read_frame(path, 30)
    
 
 
if __name__ == "__main__":
    main()
