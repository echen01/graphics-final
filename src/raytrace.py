import math
import sys
from display import *
from gmath import *
from matrix import *
import time

def intersect_sphere(origin, direction ,center, radius):
    
    radius_vector = [0,0,0]
    for i in range(0, 3):
        radius_vector[i] = origin[i] - center[i]

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
            return t
    return math.inf
    

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
    #if normal[2] < 0:
    #    return math.inf, None
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
        return math.inf, None
    '''
    edge0 = vector_subtraction(points[1], points[0])
    edge1 = vector_subtraction(points[2], points[1])
    edge2 = vector_subtraction(points[0], points[2])
    #normal = cross_product(edge0, edge2)
    '''
    #print(points[0])

    points[0].pop(scrap)
    points[1].pop(scrap)
    points[2].pop(scrap)
    intersection.pop(scrap)
    out = ispointinside(intersection, ((points[1], points[0]), (points[2], points[0]), (points[2], points[1])))
    
    #area = dot_product(polygon_normal, polygon_normal)
    '''
    c0 = vector_subtraction(intersection, points[0])
    c = cross_product(edge0, c0)
    if (dot_product(normal, c) < 0):
        return math.inf, None
    
    
    c1 = vector_subtraction(intersection, points[1])
    c = cross_product(edge1, c1)
    if (dot_product(normal, c) < 0):
        return math.inf, None
    
    
    c2 = vector_subtraction(intersection, points[2])
    c = cross_product(edge2, c2)
    if (dot_product(intersection, c) < 0):
        return math.inf, None
    out = True
    '''
    if out:
        #print(intersection)
        return t, normal   
    else:
        return math.inf, None
def absmax(vector):
    value = 0
    index = 0
    for i in range(0, len(vector)):
        if abs(vector[i]) > value:
            value = abs(vector[i])
            index = i
    return index

def rayintersectseg(p, edge):
    _eps = 0.00001
    _huge = sys.float_info.max
    _tiny = sys.float_info.min


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


def trace_ray(color_list, rayO, rayD, polygons, view, ambient, light, symbols, reflect):
    point = 0
    t = math.inf
    normal = []
    shape = ''
    

    while point < len(polygons) - 2:
        if polygons[point] == polygons[point+1]:
            #print("plane found")
            n_obj = polygons[point+2][:3]
            t_obj = intersect_plane(rayO, rayD, n_obj, polygons[point][:3])
            #print(t_obj)
            s_obj = 'plane'
        elif math.inf == polygons[point][0]:
            #print("FOUND SPHERE")
            t_obj = intersect_sphere(rayO, rayD, polygons[point+1][:3], polygons[point+2][0] )
            n_obj = None
            s_obj ='sphere'
        else:
            t_obj,n_obj = intersect_polygons(rayO, rayD, polygons, point)
            s_obj = 'poly'
        if t_obj < t:
            t, obj_idx, normal,shape = t_obj, point,n_obj, s_obj
        point += 3

    if t == math.inf:
        return False
    #print(t)
    #print(normal)
    obj = polygons[obj_idx]
    #print(t)
    M = [0,0,0]
    for x in range(0, 3):
        M[x] = rayO[x] + rayD[x] * t
    #print(normal)

    if shape == "sphere":
        normal = vector_subtraction(M, polygons[obj_idx + 1][0:3])
        normalize(normal)
    #print(normal)
    N_const = [0,0,0]
    for x in range(0, 3):
        N_const[x] = M[x] + normal[x] * .0001
    
    
    reflect = color_list[int(obj_idx / 3 )]
    '''
    if shape == 'plane':
         if (int(M[0] * 2) % 2) == (int(M[2] * 2) % 2):
            reflect = "white"
    '''
    color_ray = [10,10,10]
    for li in light:
        l = []
        toL = vector_subtraction(li[0], M)
        normalize(toL)
        point = 0
        
        while point < len(polygons) - 2:
            if point != obj_idx:
                if polygons[point] == polygons[point+1]:
                    #print('plane shadow')
                    shadow = intersect_plane(N_const, toL, normal, polygons[point][:3])
                elif polygons[point][0] == math.inf:
                    #print('sphere shadow')
                    shadow = intersect_sphere(N_const, toL, polygons[point+1][:3], polygons[point+2][0])
                else:
            
                    shadow, _ = intersect_polygons(N_const, toL, polygons, point)
                if shadow:
                    l.append(shadow)
            point += 3
        #print(l)
        if len(l) > 0 and min(l) < math.inf:
            #print("Found shadow!")
            color_ray = vector_addition(color_ray, calculate_ambient(ambient, symbols[reflect][1]))
            continue
        #print(rayD)
        
        color_ray = vector_addition(color_ray, get_point_lighting(normal, view, ambient, li, symbols, reflect))
        
                                
    
    return obj_idx, M, normal, color_ray

def trace_rays(color_list, polygons,screen, zbuffer, view, ambient, light, symbols, reflect, max_depth = 5):
    '''
    polygons = polygons[:]
    scale = make_scale(2/XRES, 2/YRES, 2/XRES)
    matrix_mult(scale,polygons)
    trans = make_translate(-1, -1, 0)
    matrix_mult(trans, polygons)
    '''
    #print("COLOR LIST", color_list)
    #print("POLYS", polygons)
    focal_length = math.sqrt(XRES **2 + YRES **2) / ( 2* math.tan( math.pi/8 ) )
    print("FOCAL", focal_length) 
    aspect_ratio = float(XRES) / YRES
    x0 = -1 
    x1 = 1  
    xstep = (x1 - x0) / (XRES - 1)
    y0 = -1 / aspect_ratio
    y1 = 1 / aspect_ratio
    ystep = (y1 - y0) / (YRES - 1)
    start = time.time()
    rayO = view
    for j in range(YRES):
        if j % 10 == 0:
            print(j / float(XRES) * 100 , "%")
        y = y0 + j * ystep
        for i in range(XRES):
            x = x0 + i * xstep
            color = [0,0,0]
            depth = 0
            #print(x, y, 0)
            rayD = vector_subtraction((x,y,0), view)
            normalize(rayD)
            reflection = [1,1,1]
            while depth < max_depth:
                traced = trace_ray(color_list, rayO, rayD, polygons, view, ambient, light, symbols, reflect)
                if not traced:
                    break
                obj_idx, M, N, color_ray = traced
                RayO =[0,0,0]
                for num in range(0, 3):
                    RayO[num] = M[num] + N[num] * .0001
                rayD = vector_subtraction(rayD, scalar_multiplication(N, 2 * dot_product(rayD, N)))
                normalize(rayD)
                depth += 1
                color_ray[0] = color_ray[0] * reflection[0]
                color_ray[1] = color_ray[1] * reflection[1]
                color_ray[2] = color_ray[2] * reflection[2]
                color = vector_addition(color, color_ray)
                #print(symbols)
                reflect = color_list[int(obj_idx / 3)]
                reflection[0] *= symbols[reflect][1]['red'][SPECULAR]
                reflection[1] *= symbols[reflect][1]['green'][SPECULAR]
                reflection[2] *= symbols[reflect][1]['blue'][SPECULAR]

            limit_color(color)
            #print("x, y, color", i, j, color)
            # if color == [0,0,0]:
            #    color = [255, 255, 255]
            color = [int(c) for c in color]
            plot(screen, zbuffer, color, i, j,0)
            #print(color)
    print(len(polygons))
    elapsed = time.time() - start
    print("Time Elapsed: %.2f seconds" % elapsed)

def add_plane(polygons, x = 0, y = 0, z = 0, normal = [0,1,0]):
    polygons.append([x,y,x,1])
    polygons.append([x,y,z,1])
    n = normal[:]
    normalize(n)
    n.append(1)
    polygons.append(n)

def add_sphere_ray(polygons, x, y, z, r):
    polygons.append([math.inf, math.inf, math.inf, 1])
    polygons.append([x, y, z, 1])
    polygons.append([r, 0, 0, 1])