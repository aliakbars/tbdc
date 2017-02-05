from django.conf import settings
from keras.models import load_model
from keras.utils import np_utils
from scipy import misc

import glob
import matplotlib.pyplot as plt
import numpy as np
import os

nb_classes = 2
kernel_size = (160, 160)
stride = 160
downsample = 8
sample_size = 1000
model = None

def create_patches(img, size, step, downsample=1, debug=False):
    height, width, c = img.shape
    cols = (width - size) / step + 1
    rows = (height - size) / step + 1

    if debug:
        print("Rows:", rows)
        print("Columns:", cols)
        print(img.shape)

    img = np.rollaxis(img, 2)

    patches = []
    for i in range(rows):
        for j in range(cols):
            patch = img[:, i*step:i*step+size:downsample, j*step:j*step+size:downsample]
            patch = np.expand_dims(patch, axis=0)
            patches.append(patch.copy())

    return np.concatenate(patches), rows, cols

def import_model():
    global model
    print "Loading model.."
    model = load_model(os.path.join(settings.BASE_DIR, 'media/quinn.h5'))
    print "Loaded.."

def detect_mtb(f):
    global model

    if model == None:
        import_model()

    img = misc.imread(f)
    X, rows, cols = create_patches(img, kernel_size[0], stride, downsample)
    X = X.astype('float32')

    y_pred = model.predict(X)
    y_pred = (y_pred > .5).astype('float32')

    pos = np.sum(y_pred, axis=0)[1]
    neg = np.sum(y_pred, axis=0)[0]

    return pos
