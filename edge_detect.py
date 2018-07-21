#! /usr/bin/python3

import argparse

from PIL import Image
from numpy import *
from skimage import feature

parser = argparse.ArgumentParser(description='detect edge')
parser.add_argument('-i', dest='infile', action='store', help='image file')
parser.add_argument('-f', dest='flag', action='store', help='image file')
args = parser.parse_args()

im = array(Image.open(args.infile).convert('L'))
im.resize(280, 496)
imx = zeros(im.shape)
imx = feature.canny(im)

def check():
    mask = zeros(imx.shape, dtype=bool)
    mask[:, 108:387] = True
    r = mask * imx
    d = sum(reshape(imx, (imx.size,))) - sum(reshape(r, (r.size,)))

    (lt, lcs, li, rt, rcs, ri) = (0, 0, 108, 0, 0, 387)
    for i in range(108, 180):
        c = imx[:, i]
        cs = sum(reshape(c, (c.size, )))
        if (cs + lcs) > lt:
            lt = cs + lcs
            li = i
        lcs = cs

        c = imx[:, 496 - i]
        cs = sum(reshape(c, (c.size, )))
        if (cs + rcs) > rt:
            rt = cs + rcs
            ri = 496 - i
        rcs = cs
    
    c = imx[:, li]
    l1 = sum(reshape(c, (c.size, )))
    c = imx[:, li - 1]
    l2 = sum(reshape(c, (c.size, )))
    c = imx[:, ri]
    r1 = sum(reshape(c, (c.size, )))
    c = imx[:, ri + 1]
    r2 = sum(reshape(c, (c.size, )))
    print(li, l1, l2, ri, r1, r2)
    s= l1 + l2 + r1 + r2
    if (s >= 420):
        return True, 0
    if (d > s * 4):
        return False, 0
    if ((l1 > 140 or l2 > 140) and (r1 > 140 or r2 > 140)):
        return True, 1
    if (s > 280 and s < 560):
        return True, 2
    if (d < 100 and s > 140):
        return True, 3
    return False, 1

ret, code = check()
print(args.infile, ret, code)
if (int(ret) == int(args.flag)):
    Image.fromarray((imx * 255).astype(uint8)).save(args.infile + 'out.bmp')