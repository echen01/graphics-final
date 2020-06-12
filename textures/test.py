#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 20:04:36 2020

@author: eric
"""
screen = {}
f = open('sand.txt', 'r')
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