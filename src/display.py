from subprocess import Popen, PIPE
from os import remove, fork, execlp

#constants
XRES = 500
YRES = 500
MAX_COLOR = 255
RED = 0
GREEN = 1
BLUE = 2

DEFAULT_COLOR = [0, 0, 0]

def new_screen( width = XRES, height = YRES ):
    screen = []
    for y in range( height ):
        row = []
        screen.append( row )
        for x in range( width ):
            screen[y].append( DEFAULT_COLOR[:] )
    return screen

def new_zbuffer( width = XRES, height = YRES ):
    zb = []
    for y in range( height ):
        row = [ float('-inf') for x in range(width) ]
        zb.append( row )
    return zb

def plot( screen, zbuffer, color, x, y, z ):
    newy = YRES - 1 - y
    z = int((z * 1000)) / 1000.0

    if ( x >= 0 and x < XRES and newy >= 0 and newy < YRES and zbuffer[newy][x] <= z):
        screen[newy][x] = color[:]
        zbuffer[newy][x] = z

def clear_screen( screen ):
    for y in range( len(screen) ):
        for x in range( len(screen[y]) ):
            screen[y][x] = DEFAULT_COLOR[:]

def clear_zbuffer( zb ):
    for y in range( len(zb) ):
        for x in range( len(zb[y]) ):
            zb[y][x] = float('-inf')

def save_ppm( screen, fname ):
    f = open( fname, 'w' )
    ppm = 'P3\n' + str(len(screen[0])) +' '+ str(len(screen)) +' '+ str(MAX_COLOR) +'\n'
    for y in range( len(screen) ):
        row = ''
        for x in range( len(screen[y]) ):
            pixel = screen[y][x]
            row+= str( pixel[ RED ] ) + ' '
            row+= str( pixel[ GREEN ] ) + ' '
            row+= str( pixel[ BLUE ] ) + ' '
        ppm+= row + '\n'
    f.write( ppm )
    f.close()
def img_dict(fname):
    p = Popen( ['convert', fname, fname[:-4] + ".txt"], stdin=PIPE, stdout = PIPE )
    p.communicate()
    screen = {}
    f = open(fname[:-4] + ".txt", 'r')
    lines = f.read().split('\n')

    for line in lines[1:-1]:
        line = line.split(" ")
        
        coords = line[0]
        coords = coords.split(',')
        x = int(coords[0])
        y = int(coords[1][:-1])
        #screen[(x, y)] = 
        print(x, y)
        rgb = line[-1]
        rgb = rgb.split('(')
        rgb = rgb[1][:-1]
        rgb = tuple([int(color) for color in rgb.split(",")])
        print(rgb)
        screen[(x, y)] = rgb
    f.close()
    return screen
# def save_ppm( screen, fname ):
#     f = open( fname, 'w' )
#     ppm = 'P3\n' + str(len(screen[0])) +' '+ str(len(screen)) +' '+ str(MAX_COLOR) +'\n'
#     rows = []
#     for y in range( len(screen) ):
#         row = []
#         for x in range( len(screen[y]) ):
#             pixel = screen[y][x]
#             row.append(' '.join([str(x) for x in pixel]))
#         rows.append(' '.join(row))
#     ppm+= '\n'.join(rows)
#     print ppm
#     f.write( ppm )
#     f.close()

def save_extension( screen, fname ):
    ppm_name = fname[:fname.find('.')] + '.ppm'
    save_ppm( screen, ppm_name )
    p = Popen( ['convert', ppm_name, fname ], stdin=PIPE, stdout = PIPE )
    p.communicate()
    remove(ppm_name)

def display( screen ):
    ppm_name = 'pic.ppm'
    save_ppm( screen, ppm_name )
    p = Popen( ['display', ppm_name], stdin=PIPE, stdout = PIPE )
    p.communicate()
    remove(ppm_name)

def make_animation( name ):
    name_arg = 'anim/' + name + '*'
    name = name + '.gif'
    print('Saving animation as ' + name)
    f = fork()
    if f == 0:
        execlp('convert', 'convert', '-delay', '1.7', name_arg, name)

