import png
import numpy as np
import sys # for highest float
from scene import Sphere, Light, normalize

WIDTH = 900
HEIGHT = 900
VIEWPOINT = np.zeros(3)
BG_COL = np.array([0.8, 0.8, 1.0])

INF = sys.float_info.max

### RAY CLASS ###
class Ray:
    def __init__(self, direction, orig=np.zeros(3)):
        self.orig = orig
        self.dir = direction
#################

def max(a, b):
    return a if a > b else b

def camcr(x, y):
    fovx = np.pi / 4
    fovy = (HEIGHT / WIDTH) * fovx
    return normalize(np.array([(2 * x - WIDTH) / WIDTH, -((2 * y - HEIGHT) / HEIGHT) * np.tan(fovy), -1.0]))

# Takes a nested list and flattens it.
def flatten(list):
    flat_list = []
    for sub in list:
        for item in sub:
            flat_list.append(item)
    return flat_list

# Takes an image (list of rows, where each row is a list of 3d lists of floats)
# and converts it into a 2d list of ints that can be handled by PyPNG.
def img_to_px(img):
    return map(lambda ls : map(int, ls), map(flatten, img))

image = [[0 for j in range(WIDTH)] for i in range(HEIGHT)]
objects = [
    Sphere(np.array([0.5, 0.6, -1]), 0.2),
    Sphere(np.array([-0.2, 0, -1]), 0.6)
] # list of objects in the scene

lights = [
    Light(np.array([0, 2.0, 0]), 0.8)
] # list of light sources in the scene

# casts a given ray and returns the resulting color as a 3d vector
def cast_ray(ray):
    inters_obj = None # the closest object that the ray meets
    inters_dist = INF # the intersection distance
    for obj in objects: # check for each object whether the ray hits it
        dist = obj.intersect(ray)
        if dist != 0.0 and dist < inters_dist: # update the intersection values
            inters_obj = obj
            inters_dist = dist

    if inters_obj == None: return BG_COL.copy() # copying is important: all objects are stored as pointers (like Java)

    inters_point = inters_dist * ray.dir + ray.orig # the point of intersection

    # if there was an intersection, we want to figure out the correct color using phong-shading
    ambient = np.array([0.3, 0, 0])
    diffuse = np.zeros(3)
    for light in lights:
        point_light_dist = light.pos - inters_point
        diffuse_intensity = max(0.0, normalize(point_light_dist).dot(obj.normal(inters_point)))
        diffuse += np.ones(3) * diffuse_intensity * light.intensity

    return np.clip(ambient + diffuse, 0.0, 1.0) # make sure the values are within [0, 1]

# loops through every pixel and casts a ray
def render():
    for y in range(HEIGHT):
        for x in range(WIDTH):
            color = cast_ray(Ray(camcr(x, y)))
            image[y][x] = (color*255).tolist()

render() # the main render call

# Image writing
f = open('out.png', 'wb')
w = png.Writer(WIDTH, HEIGHT, greyscale=False)
w.write(f, img_to_px(image))
f.close()
