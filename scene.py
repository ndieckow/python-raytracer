from abc import ABC, abstractmethod
import numpy as np

# normalizes a vector w.r.t. the 2-norm
def normalize(vec):
    return vec / np.linalg.norm(vec, ord=2)

# Every object in the scene has a position and an intersect function
class SceneObject(ABC):
    def __init__(self, pos):
        self.pos = pos
        super().__init__() # does this need to be called?

    @abstractmethod
    def intersect(self, ray) -> float:
        pass

    @abstractmethod
    def normal(self, point):
        pass

class Sphere(SceneObject):
    def __init__(self, pos, radius=1.0):
        SceneObject.__init__(self, pos) # call the parent constructor
        self.radius = radius

    # follows directly from the sphere equation and the p-q-formula
    def intersect(self, ray) -> float:
        omc = ray.orig - self.pos
        dir_omc = ray.dir.dot(omc)
        omc_omc = omc.dot(omc)
        dis = dir_omc*dir_omc - omc_omc + self.radius*self.radius # discriminant. if this is < 0, the result is not real
        if dis < 0: return 0.0 # 0 means no intersection
        t = -dir_omc - np.sqrt(dis)
        if t > 0.0: return t
        t = -dir_omc + np.sqrt(dis)
        return t if t > 0.0 else 0.0 # ternary operator

    def normal(self, point):
        return normalize(point - self.pos)

class Light():
    def __init__(self, pos, intensity=1.0):
        self.pos = pos
        self.intensity = intensity
