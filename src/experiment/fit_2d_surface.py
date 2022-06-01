
import torch
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import os
import matplotlib
# matplotlib.use( 'tkagg')


def square(x):
    return x**2


def coord_to_sphere(thetas):
    theta, phi = torch.split(thetas, [1, 1], 1)
    x = torch.cos(phi) * torch.sin(theta)
    y = torch.sin(phi) * torch.sin(theta)
    z = torch.cos(theta)
    return torch.cat([x, y, z], 1)


def distance_loss(x):
    assert x.shape[1] == 3
    n_pnts = x.shape[0]
    d = torch.unsqueeze(x, 0) - torch.unsqueeze(x, 1)
    d = torch.square(d)
    d = torch.sum(d, 2)
    d.fill_diagonal_(10)
    
    r = d
    r, _ = torch.min(r, dim=1)
    r = torch.sum(r)
    
    # e = d
    # e = torch.exp(-2 * e)
    # e = torch.sum(e)
    
    return -r # + 1e-3 * e


def get_faces():
    base_dir = '/work/ProjectsForFun/pgen/video_synth/src/external/star/star_1_1/'
    path_model = os.path.join(base_dir, 'male', 'model.npz')
    star_model = np.load(path_model, allow_pickle=True)
    faces = torch.from_numpy(star_model['f'].astype(np.int64))
    return faces


def calc_face_cost(vertices, faces):
    triangles = vertices[faces]
    v1, v2, v3 = torch.split(triangles, [1, 1, 1], 1)
    v1, v2, v3 = torch.squeeze(v1, 1), torch.squeeze(v2, 1), torch.squeeze(v3, 1)
    l12 = torch.sum(torch.square(v1 - v2), 1)
    l13 = torch.sum(torch.square(v1 - v3), 1)
    l23 = torch.sum(torch.square(v2 - v3), 1)
    loss = l12 + l13 + l23
    return torch.sum(loss)


def main():
    faces = get_faces()
    faces = faces[:15, :]
    num_points = 50
    thetas = 3 * torch.rand((num_points, 2)).cuda()
    thetas.requires_grad_()
    
    print(thetas)

    # Do gradient descent
    n_optim_steps = int(1e4)
    optimizer = torch.optim.SGD([thetas], 1e-2)

    for ii in range(n_optim_steps):
        optimizer.zero_grad()
        x = coord_to_sphere(thetas)
        distance_cost = distance_loss(x)
        face_cost = calc_face_cost(x, faces)
        loss = distance_cost + 0.1 * face_cost
        
        print('Step # {}, loss: {}'.format(ii, loss.item()))
        loss.backward()
        # Access gradient if necessary
        grad = thetas.grad.data
        optimizer.step()
 
    cart = coord_to_sphere(thetas).detach().cpu().numpy()
    # import pdb; pdb.set_trace()
    print(np.linalg.norm(cart, axis=1))
    x, y, z = cart[:, 0], cart[:, 1], cart[:, 2]
    fig = plt.figure(figsize=(4,4))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x, y, z)
    plt.show()
    # print(thetas)
    # print(coord_to_sphere(thetas))


if __name__ == "__main__":
    main()
