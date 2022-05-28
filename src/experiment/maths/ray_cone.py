from dataclasses import dataclass
import numpy as np


def compute_intersections(rays, cones):
    assert len(rays.shape) == 3
    assert len(cones.shape) == 2
    assert rays.shape[0] == cones.shape[0]
    
    assert rays.shape[1] == 2
    assert rays.shape[2] == 3
    assert cones.shape[1] == 3
    
    dir = rays[:, 1, :] - rays[:, 0, :]
    
    px = rays[:, 0, 0]
    py = rays[:, 0, 1]
    dx = dir[:, 0]
    dy = dir[:, 1]
    r1 = cones[:, 0]
    rg = (cones[:, 1] - cones[:, 1]) / cones[:, 2]
    
    a0 = -px**2*rg**2 + px**2 - 2*px*r1*rg + py**2 - r1**2
    a1 = -2*dx*px*rg**2 + 2*dx*px - 2*dx*r1*rg + 2*dy*py
    a2 = -dx**2*rg**2 + dx**2 + dy**2
    
    d = a1 ** 2 - 4 * a2 * a0
    
    ts = np.concatenate([
         0.5 * (-a1 + d)[:, None],
         0.5 * (-a1 - d)[:, None],
    ], 1)
    inters = rays[:, None, :] + ts[:, :, None] * np.tile(dir[:, None, :], [1, 2, 1])
    print(inters)
    # inters = np.einsum('ijk,i->i', rays, ts)
    # print(inters)


# def compute_intersection(ray: Ray, cone: Cone):
#     px,py,dx,dy,r1,rg = ray.pnt[0], ray.pnt[1], ray.dir[0], ray.dir[1], cone.r1, (cone.r2 - cone.r1) / cone.len
#     a0 = -px**2*rg**2 + px**2 - 2*px*r1*rg + py**2 - r1**2
#     a1 = -2*dx*px*rg**2 + 2*dx*px - 2*dx*r1*rg + 2*dy*py
#     a2 = -dx**2*rg**2 + dx**2 + dy**2
    
#     d = a1 ** 2 - 4 * a2 * a0
#     if d < 0:
#         return
#     for t in [
#         0.5 * (-a1 + np.sqrt(d)),
#         0.5 * (-a1 - np.sqrt(d)),
#     ]:
#         print('val-1', a0  + a1 * t + a2 * t ** 2)
#         pz,dz = ray.pnt[2], ray.dir[2]
#         x = px + t * dx
#         y = py + t * dy
#         z = pz + t * dz
        
#         r = r1 + rg * z
#         print('r', r)
#         print('val-2', x**2 + y**2 - r**2)
        
#         ret = np.array(ray.pnt + t * ray.dir)
#         print('diff', np.linalg.norm(np.array([x, y, z]) - ret))
#         yield t, ret

def test_intersection():
    n = 10
    rays = 1 + np.random.random((n, 2, 3))
    cones = 1 + np.random.random((n, 3))
    compute_intersections(rays, cones)


if __name__ == "__main__":
    test_intersection()


    