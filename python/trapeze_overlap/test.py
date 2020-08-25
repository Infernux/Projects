#!/usr/bin/python3

import json
import math
import sys
import glob
from PIL import Image, ImageDraw
from math import *

png_out_folder = 'pngs'

res = None

base_point = (500, 1000)
target_radius = 300
target_angle = 100

offset_angle = 5
offset_radius = 20

def get_four_points(base_point, offset_angle, offset_radius):
    tgt_rad = convert_deg_to_rad(target_angle)
    offset_rad = convert_deg_to_rad(offset_angle)
    x1 = base_point[0] + cos(tgt_rad - offset_rad) * (target_radius - offset_radius)
    y1 = base_point[1] - sin(tgt_rad - offset_rad) * (target_radius - offset_radius)
    x2 = base_point[0] + cos(tgt_rad + offset_rad) * (target_radius - offset_radius)
    y2 = base_point[1] - sin(tgt_rad + offset_rad) * (target_radius - offset_radius)
    x3 = base_point[0] + cos(tgt_rad + offset_rad) * (target_radius + offset_radius)
    y3 = base_point[1] - sin(tgt_rad + offset_rad) * (target_radius + offset_radius)
    x4 = base_point[0] + cos(tgt_rad - offset_rad) * (target_radius + offset_radius)
    y4 = base_point[1] - sin(tgt_rad - offset_rad) * (target_radius + offset_radius)
    return ((x1,y1), (x2, y2), (x3, y3), (x4, y4))

def convert_deg_to_rad(deg):
    return ((2*pi) / 360) * deg

def get_point(base, target_radius, target_angle):
    x = base[0] + cos(target_angle) * target_radius
    y = base[1] - sin(target_angle) * target_radius

    return (x, y)

def draw_stuff():
    im = Image.new('RGB', (1000, 1000), (0,0,0))
    draw = ImageDraw.Draw(im)

    square_width = 20
    square_height = 20

    white = (255,255,255)

    x = 500 - (square_width / 2)
    y = 950

    draw.line((base_point, (500, 0)))

    draw.polygon(get_four_points(base_point, offset_angle, offset_radius), fill=(255,0,0))

    im.save(png_out_folder+'/{}.png'.format('output'))

if __name__ == "__main__":
    draw_stuff()
