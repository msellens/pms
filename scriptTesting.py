import sys
import array
import argparse
import json
import pickle
from pms import *
import OpenEXR
import Imath
import os

import numpy as np
#from scipy.misc import imread
from imageio import imread
from scipy import sparse
from scipy import optimize

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

import mesh

imagedir = 'D:/Test Images/quilt/small/'
filenames = os.listdir(imagedir)
images_filenames = [(imagedir + name) for name in filenames if name.endswith("sm.jpg")]
masknames = [(imagedir + name) for name in filenames if name.startswith('photo_mask') and name.endswith(".png")]
maskname = masknames[0]
mask = getImage(maskname)
mask = mask.T

#images_filenames = ('IMG_1229sm.jpg', 'IMG_1230sm.jpg', 'IMG_1231sm.jpg', 'IMG_1232sm.jpg', 'IMG_1233sm.jpg', 'IMG_1234sm.jpg', 'IMG_1235sm.jpg', 'IMG_1236sm.jpg')
normals = photometricStereoWithoutLightning(images_filenames)
normals[mask<(mask.max() - mask.min())/2.] = np.nan

color = colorizeNormals(normals)
plt.imsave(imagedir + 'out.png', color)
mesh.write3dNormals(normals, imagedir + 'out-3dn.stl')
surface = mesh.surfaceFromNormals(normals)
mesh.writeMesh(surface, normals, imagedir + 'out-mesh.stl')
heightMap = mesh.surfaceToHeight(surface)
plt.imsave(imagedir + 'out-height.png', heightMap)
outfile = OpenEXR.OutputFile(imagedir + 'out-height-fl2.exr', OpenEXR.Header(surface.shape[0], surface.shape[1]))
R = array.array('f', surface[:,:,2].reshape(-1,1)).tostring()
outfile.writePixels({'R' : R})
outfile.close()
mesh.writeObj(surface, normals, imagedir + 'out-surface.obj')

