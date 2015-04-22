import numpy as np
import cv2
import os

count = 4000
descriptor = cv2.SURF(count)
npy_pattern = '%%s-surf-%s' % count

def getDes(img_name):
    np_name = img_name[:-4]
    np_name = np_name.replace('/pages/', '/npys/')
    directory = np_name[:np_name.rfind('/')+1]
    if not os.path.exists(directory):
        os.makedirs(directory)
    np_name = npy_pattern % np_name
    try:
        npy = '%s.npy' % np_name
        #print 'load %s for %s' % (npy, img_name)
        return np.load(npy)
    except Exception, e:
        print e
        img = cv2.imread(img_name, 0) # trainImage
        kp, des = descriptor.detectAndCompute(img, None)
        np.save(np_name, des)
        return des

def match(des1, des2):
    #FLANN_INDEX_KDTREE = 0
    #index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    #search_params = dict(checks=5)
    #flann = cv2.FlannBasedMatcher(index_params, search_params)
    #matches = flann.knnMatch(des1, des2, k=2)

    # BFMatcher with default params
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    # store all the good matches as per Lowe's ratio test.
    good = []
    for m, n in matches:
        if m.distance < 0.7*n.distance:
            good.append(m)
    return len(good)
