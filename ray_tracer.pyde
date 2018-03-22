# Tiera Lee, tlee320
# This is the starter code for the CS 3451 Ray Tracing project.
#
# The most important part of this code is the interpreter, which will
# help you parse the scene description (.cli) files.

import copy
from objects import *
def setup():
    size(500, 500) 
    noStroke()
    colorMode(RGB, 1.0)  # Processing color values will be in [0, 1]  (not 255)
    background(0, 0, 0)

# read and interpret the appropriate scene description .cli file based on key press
def keyPressed():
    if key == '1':
        interpreter("i1.cli")
    elif key == '2':
        interpreter("i2.cli")
    elif key == '3':
        interpreter("i3.cli")
    elif key == '4':
        interpreter("i4.cli")
    elif key == '5':
        interpreter("i5.cli")
    elif key == '6':
        interpreter("i6.cli")
    elif key == '7':
        interpreter("i7.cli")
    elif key == '8':
        interpreter("i8.cli")
    elif key == '9':
        interpreter("i9.cli")

def interpreter(fname):
    global sceneObjects
    global lightSources
    global hasBg
    hasBg = False
    sceneObjects = []
    lightSources = []
    
    fname = "data/" + fname
    # read in the lines of a file
    with open(fname) as f:
        lines = f.readlines()

    # parse each line in the file in turn
    for line in lines:
        words = line.split()  # split the line into individual tokens
        if len(words) == 0:   # skip empty lines
            continue
        if words[0] == 'sphere':
            radius = float(words[1])
            x = float(words[2])
            y = float(words[3])
            z = float(words[4])
            global currentSurf
            sceneObjects.append(create_sphere(radius,x,y,z,currentSurf))
            
        elif words[0] == 'fov':
            global fov
            fov = float(words[1])
            
        elif words[0] == 'background':
           r = float(words[1])
           g = float(words[2])
           b = float(words[3])
           global bg
           bg = BackgroundColor(r,g,b)
           hasBg = True
           
        elif words[0] == 'light':
            x = float(words[1])
            y = float(words[2])
            z = float(words[3])
            r = float(words[4])
            g = float(words[5])
            b = float(words[6])
            lightSources.append(Light(x,y,z,r,g,b))
            
        elif words[0] == 'surface':
            cdr = float(words[1])
            cdg = float(words[2])
            cdb = float(words[3])
            global currentSurf
            currentSurf = Surface(cdr,cdg,cdb)
            
        elif words[0] == 'begin':
            pass
        elif words[0] == 'vertex':
            pass
        elif words[0] == 'end':
            pass
        elif words[0] == 'write':
            render_scene()    # render the scene
            save(words[1])  # write the image to a file
            pass

# render the ray tracing scene
def render_scene():
    for j in range(height):
        for i in range(width):
            # create an eye ray for pixel (i,j) and cast it into the scene
            eyeRay = castEyeRay(i,j,fov)
            intersectingObjects = []
            closest = float("inf")
            for sphereObject in sceneObjects:
                t, xt, yt, zt = detectIntersection(eyeRay,sphereObject)
                if(t > 0 and t < closest):
                    closest = t
                    intersectingObjects.append(Hit(t,xt,yt,zt, sphereObject))
        
            ##takes closest intersection point and calculates color
            if(len(intersectingObjects) > 0):
                chosenHit = intersectingObjects[len(intersectingObjects)-1]
                colorX, colorY,colorZ = calculateColor(chosenHit,chosenHit.id)
                pix_color = color(colorX, colorY, colorZ)

            ##if ray misses objects, use background color
            else:
                # global hasBg
                if (hasBg):
                    pix_color = color(bg.r, bg.g, bg.b)
                else:
                    pix_color = color(0,0,0)
            set (i, j, pix_color)         # fill the pixel with the calculated color
    


def castEyeRay(i,j,fov):
    (x,y,z) = perspectiveView(i,j,-1,fov)
    origin = PVector(0.0,0.0,0.0)
    slope = PVector(x,y,z)
    slope.sub(origin)
    slope.normalize()
    return Ray(origin, slope)


def perspectiveView(x,y,z,fov):
    x1 = x / abs(z)
    y1 = (height - y) / abs(z)
    k = tan(radians(fov)/2.0)
    
    x2 = (x1 - (width/2.0)) * ((2.0*k) / width)
    y2 = (y1 - (height/2.0)) * ((2.0*k) / height)
    z2 = -1
    
    return (x2,y2,z2)

def detectIntersection(eyeRay, sphereObject):
    dx = eyeRay.dirX
    dy = eyeRay.dirY
    dz = eyeRay.dirZ
    x0 = eyeRay.x
    y0 = eyeRay.y
    z0 = eyeRay.z
    cx = sphereObject.x
    cy = sphereObject.y
    cz = sphereObject.z
    a = dx**2 + dy**2 + dz**2
    b = 2.0*((x0*dx - cx*dx) + (y0 * dy - cy*dy) + (z0 * dz - cz *dz))
    c = (x0 - cx)**2 + (y0 - cy)**2 + (z0 - cz)**2 - (sphereObject.radius)**2

    discr = b**2 - 4.0 * a * c
    if discr >= 0:
         t1 = (-1.0 * b + sqrt(discr)) / (2.0 * a)
         t2 = (-1.0 * b - sqrt(discr)) / (2.0 * a)
         
         if (t1 > 0 and t2 > 0):
             if (t1 > t2):
                 t = t2
             else:
                 t = t1
         elif (t1 > 0 and t2 < 0):
             t = t1
         else:
             t = t2
         xt = x0 + t* dx
         yt = y0 + t* dy
         zt = z0 + t* dz
         
         return (t, xt, yt, zt)
    else:
        return (None,None,None,None)
    
def calculateColor(hit, sphereObject):
    sphereCenter = PVector(sphereObject.x, sphereObject.y, sphereObject.z)
    intersectPoint = PVector(hit.x, hit.y, hit.z)
    surfaceNormal = copy.deepcopy(intersectPoint)
    surfaceNormal.sub(sphereCenter)
    surfaceNormal.normalize()
    
    sum = PVector(0,0,0)
    
    for light in lightSources:
        lightVector = PVector(light.x, light.y, light.z)
        lightVector.sub(intersectPoint)
        lightVector.normalize()
        vectorMath = max(0, lightVector.dot(surfaceNormal))

        
        sum.x += light.r * vectorMath
        sum.y += light.g * vectorMath
        sum.z += light.b * vectorMath
        
    surface = sphereObject.surface
    colorX = sum.x * surface.cdr
    colorY = sum.y * surface.cdg
    colorZ = sum.z * surface.cdb
    
    return(colorX, colorY, colorZ)
def draw():
    pass