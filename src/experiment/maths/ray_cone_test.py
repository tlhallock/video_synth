from dataclasses import dataclass
import numpy as np



@dataclass
class Cone:
    r1: float = 1.0
    r2: float = 1.0
    len: float = 1.0


@dataclass
class Ray:
    pnt: np.ndarray
    dir: np.ndarray



"""

from sympy import *
# The distance along the ray
t = symbols('t')
# The pixel location	
px, py, pz = var('px py pz')
# The pixel direction
dx, dy, dz = var('dx dy dz')
# Tntersection point
x = px + t * dx
y = py + t * dy
z = px + t * dx
# The radaii of the cone
r1, rg = var('r1 rg')
# Cone radius
r = r1 + rg * z
poly = x^2 + y^2 - r^2
poly = poly.expand().collect(t)

a0 = poly.coeff(t, 0)
a1 = poly.coeff(t, 1)
a2 = poly.coeff(t, 2)

"""

def compute_intersection(ray: Ray, cone: Cone):
    px,py,dx,dy,r1,rg = ray.pnt[0], ray.pnt[1], ray.dir[0], ray.dir[1], cone.r1, (cone.r2 - cone.r1) / cone.len
    a0 = -px**2*rg**2 + px**2 - 2*px*r1*rg + py**2 - r1**2
    a1 = -2*dx*px*rg**2 + 2*dx*px - 2*dx*r1*rg + 2*dy*py
    a2 = -dx**2*rg**2 + dx**2 + dy**2
    
    d = a1 ** 2 - 4 * a2 * a0
    if d < 0:
        return
    for t in [
        0.5 * (-a1 + np.sqrt(d)),
        0.5 * (-a1 - np.sqrt(d)),
    ]:
        print('val-1', a0  + a1 * t + a2 * t ** 2)
        pz,dz = ray.pnt[2], ray.dir[2]
        x = px + t * dx
        y = py + t * dy
        z = pz + t * dz
        
        r = r1 + rg * z
        print('r', r)
        print('val-2', x**2 + y**2 - r**2)
        
        ret = np.array(ray.pnt + t * ray.dir)
        print('diff', np.linalg.norm(np.array([x, y, z]) - ret))
        yield t, ret

def test_intersection():
    ray = Ray(pnt=np.random.random(3), dir=np.array([-1, 0, 0]))
    cone = Cone(r1=1.0, r2=1.0, len=3)
    for t, intersection in compute_intersection(ray, cone):
        print(t, intersection)
        print(np.linalg.norm(intersection[:2]) - (cone.r1 + (cone.r2 - cone.r1) / cone.len * intersection[2]) ** 2)


if __name__ == "__main__":
    test_intersection()


    