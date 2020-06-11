import math
import sys
from display import *
from gmath import *

def intersect_sphere(point, origin, center, radius):
    direction = [0,0,0]
    radius_vector = [0,0,0]
    for i in range(0, 3):
        direction[i] = point[i] - origin[i]
        radius_vector[i] = point[i] - center[i]
    normalize(direction)

    b = 2 * dot_product(direction, radius_vector)
    c = dot_product(radius_vector, radius_vector) - radius * radius

    discriminant = b * b - 4 * c
    if discriminant > 0:
        disc_root = math.sqrt(discriminant)
        t0 = (-b - disc_root) / 2
        t1 = (-b + disc_root) / 2
        t0, t1 = min(t0, t1), max(t0, t1)
        if t1 >= 0:
            if t0 < 0:
                t = t1
            else:
                t = t0
            intersection = [0,0,0]
            normal = [0,0,0]
            for i in range(0, 3):
                intersection[i] = origin[i] + direction[i] * t
                normal[i] = (intersection[i] - center[i]) / radius
            return normal
    return None

def intersect_plane(origin, direction, normal, point):
    
    #direction = vector_subtraction(polygons[i][0:3], origin)
    #normalize(direction)
    
    d = dot_product(point, normal)
    vd = dot_product(normal, direction)
    if abs(vd) < 1e-6:
        return math.inf
    t = (dot_product(origin, normal) + d)/ vd
    if t < 0:
        return math.inf
    else:
        return t

def intersect_polygons(origin, direction, polygons, i):
    #normalize(normal)
    #direction = vector_subtraction(polygons[i][0:3], origin)
    #normalize(direction)
    normal = calculate_normal(polygons, i)
    normalize(normal)
    points = [ [polygons[i][0], polygons[i][1], polygons[i][2]],
               [polygons[i+1][0], polygons[i+1][1], polygons[i+1][2]],
               [polygons[i+2][0], polygons[i+2][1], polygons[i+2][2]] ]
    
    t = intersect_plane(origin, direction, normal, points[0])
    if t != math.inf:
        intersection = [0,0,0]
        for x in range(0, 3):
            intersection[x] = origin[x] + direction[x] * t
        scrap = absmax(normal)

    else:
        return

    #polygon_normal = cross_product(edge0, edge1)
    edge0 = vector_subtraction(points[1], points[0])
    edge1 = vector_subtraction(points[2], points[1])
    edge2 = vector_subtraction(points[0], points[2])
    #edge0.pop(scrap)
    #edge1.pop(scrap)
    #edge2.pop(scrap)
    #print(points[0])

    #v0 = points[0].copy().pop(scrap)
    #v1 = points[1].copy().pop(scrap)
    #v2 = points[2].copy().pop(scrap)
    #ri.pop(scrap)
    #out = ispointinside(ri, ((points[1], points[0]), (points[2], points[0]), (points[2], points[1])))
    
    #area = dot_product(polygon_normal, polygon_normal)
    
    c0 = vector_subtraction(intersection, points[0])
    c = cross_product(edge0, c0)
    if (dot_product(normal, c) < 0):
        return False, False
    
    
    c1 = vector_subtraction(intersection, points[1])
    c = cross_product(edge1, c1)
    if (dot_product(normal, c) < 0):
        return False, False
    
    
    c2 = vector_subtraction(intersection, points[2])
    c = cross_product(edge2, c2)
    if (dot_product(intersection, c) < 0):
        return False, False
    out = True
    if out:
        print(intersection)
        return t, normal
def absmax(vector):
    value = 0
    index = 0
    for i in range(0, len(vector)):
        if abs(vector[i]) > value:
            value = abs(vector[i])
            index = i
    return index
#def trace_rays(origin, direction, bounce = 0):
#_eps = 0.00001
#_huge = sys.float_info.max
#_tiny = sys.float_info.min

'''
def rayintersectseg(p, edge):

    a,b = edge
    if a[1] > b[1]:
        a,b = b,a
    if p[1] == a[1] or p[1] == b[1]:
        p = [p[0], p[1] + _eps]
 
    intersect = False
 
    if (p[1] > b[1] or p[1] < a[1]) or (
        p[0] > max(a[0], b[0])):
        return False
 
    if p[0] < min(a[0], b[0]):
        intersect = True
    else:
        if abs(a[0] - b[0]) > _tiny:
            m_red = (b[1] - a[1]) / float(b[0] - a[0])
        else:
            m_red = _huge
        if abs(a[0] - p[0]) > _tiny:
            m_blue = (p[1] - a[1]) / float(p[0] - a[0])
        else:
            m_blue = _huge
        intersect = m_blue >= m_red
    return intersect
 
def odd(x): return x%2 == 1
 
def ispointinside(p, poly):
    return odd(sum(rayintersectseg(p, edge) for edge in poly))
'''

def trace_ray(rayO, rayD, polygons, view, ambient, light, symbols, reflect):
    point = 0
    t = math.inf
    while point < len(polygons) - 2:
        
        t_obj,normal = intersect_polygons(rayO, rayD, polygons, point)
        if t_obj < t:
            t, obj_idx = t_obj, point
        point += 3

    if t == math.inf:
        return
    obj = polygons[obj_idx]
    M = [0,0,0]
    for x in range(0, 3):
        M[x] = rayO[x] + rayD[x] * t
    
    N_const = [0,0,0]
    for x in range(0, 3):
        N_const[x] = M[x] + N[x] * .0001
    
    #toL = normalize(vector_subtraction(light, M))
    #l= [intersect_polygons(N_const, toL, polygons, i) for k, obj_sh in enumerate(polygons)]
    color_ray = get_lighting(normal, view, ambient, light, symbols, reflect)
    return obj_idx, M, normal, color_ray

def trace_rays(screen, zbuffer, view, polygons, ambient, light, symbols, reflect, max_depth = 4):
    w = len(screen[0])
    r = float(w) / len(screen)
    for j in YRES:
        if j % 10 == 0:
            print(j / float(w) * 100 , "%")
        for i in XRES:
            color = [0,0,0]
            rayD = normalize(vector_subtraction((i,j,0), view))
            rayO = view
            while depth < depth_max:
                traced = trace_ray(rayO, rayD, polygons, view, ambient, light, symbols, reflect)
                if not traced:
                    break
                obj_idx, M, N, color_ray = traced
                RayO =[0,0,0]
                for num in range(0, 3):
                    RayO[num] = M[num] + N[num] * .0001
                rayD = vector_subtraction(rayD, scalar_multiplication(N, 2 * dot_product(rayD, N))))
                normalize(rayD)
                depth += 1
                color = vector_addition(color, color_ray)
            plot(screen, zbuffer, color, i, j,)

                    