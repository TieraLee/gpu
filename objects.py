class BackgroundColor(object):
    def __init__(self, r,g,b):
        self.r = r
        self.g = g
        self.b = b

class create_sphere(object):
    def __init__(self, radius, x, y, z,surface):
        self.radius = radius
        self.x = x
        self.y = y
        self.z = z
        self.surface = surface
    
class Light(object):
    def __init__(self, x, y, z, r, g, b,):
        self.x = x
        self.y = y
        self.z = z
        self.r = r
        self.g = g
        self.b = b

class Surface(object):
    def __init__(self, cdr, cdg, cdb):
        self.cdr = cdr
        self.cdg = cdg
        self.cdb = cdb

class Ray(object):
    def __init__(self, origin, direction):
        self.x = origin.x
        self.y = origin.y
        self.z = origin.z
        self.dirX = direction.x
        self.dirY = direction.y
        self.dirZ = direction.z
    
class Hit(object):
    def __init__(self, t, x, y, z, id):
        self.t = t
        self.x = x
        self.y = y
        self.z = z
        self.id = id