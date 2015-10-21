import kzpy
from kzpy import *
from kzpy.img import *

def get_points(W = 512,parameter = 0.8649):
    X,Y = W,W
    points = []
    a = np.zeros((X,Y))
    for x in range(X):
        for y in range(Y):
            r = np.sqrt((x-W/2.0)**2+(y-W/2.0)**2)/(W/2.0*np.sqrt(2.0))
            #r = np.max((0.75,r))
            if r > 0.995:
                r = 0.995
            if np.random.rand() > r:
                if np.random.rand() > parameter:
                    a[x,y] = 1
                    points.append([x,y])
    points = np.array(points)                
    mi(a, img_title = str(np.sum(a)/(W**2)))
    return points

def get_points_SPECIAL_384x512(W = 512,parameter = 0.8649):
    X,Y = W,W
    points = []
    a = np.zeros((X,Y))
    for x in range(63,384+64):
        for y in range(Y):
            r = np.sqrt((x-W/2.0)**2+(y-W/2.0)**2)/(W/2.0*np.sqrt(2.0))
            #r = np.max((0.75,r))
            if r > 0.995:
                r = 0.995
            if np.random.rand() > r:
                if np.random.rand() > parameter:
                    a[x,y] = 1
                    points.append([x,y])
    points = np.array(points)                
    mi(a, img_title = str(np.sum(a)/(W**2)))
    return points

def get_points_SPECIAL_1(W = 512,parameter = 0.8649):
    X,Y = W,W
    points = []
    a = np.zeros((X,Y))
    for x in range(X):
        for y in range(Y):
            if (x>200 and x<300) and (y>200 and y<300):
                r = 0.98
            else:
                r = np.sqrt((x-W/2.0)**2+(y-W/2.0)**2)/(W/2.0*np.sqrt(2.0))
            if r > 0.995:
                r = 0.995
            if np.random.rand() > r:
                if np.random.rand() > parameter:
                    a[x,y] = 1
                    points.append([x,y])
    points = np.array(points)                
    mi(a, img_title = str(np.sum(a)/(W**2)))
    return points

def get_points_SPECIAL_2(W = 512,parameter = 0.8649):
    X,Y = W,W
    points = []
    a = np.zeros((X,Y))
    for x in range(X):
        for y in range(Y):
            r = 2*np.sqrt((x-W/2.0)**2+(y-W/2.0)**2)/(W/2.0*np.sqrt(2.0))
            if r > 0.995:
                r = 0.995
            if np.random.rand() > r:
                if np.random.rand() > parameter:
                    a[x,y] = 1
                    points.append([x,y])
    points = np.array(points)                
    mi(a, img_title = str(np.sum(a)/(W**2)))
    return points

def get_mappings(points,W=512,N = 30):
    tree = scipy.spatial.KDTree(points)
   
    X,Y = W,W
    xy2p = np.zeros((W,W,2,N))

    pb = kzpy.img.ProgressBar(X)
    for x in range(X):
        pb.animate(x+1)
        for y in range(Y):
            xy2p[x,y] = tree.query([x,y],N)
    p2xys = {}
    for p in range(len(points)):
        p2xys[p] = []
    pb = kzpy.img.ProgressBar(X)
    for x in range(X):
        pb.animate(x+1)
        for y in range(Y):
            p2xys[xy2p[x,y][1][0]].append([x,y])
    return xy2p,p2xys

def get_mappings_SPECIAL_384x512(points,W=512):
    tree = scipy.spatial.KDTree(points)
    N = 5
    X,Y = W,W
    xy2p = np.zeros((W,W,2,N))

    pb = kzpy.img.ProgressBar(X)
    for x in range(63,384+64):
        pb.animate(x+1)
        for y in range(Y):
            xy2p[x,y] = tree.query([x,y],N)
    p2xys = {}
    for p in range(len(points)):
        p2xys[p] = []
    pb = kzpy.img.ProgressBar(X)
    for x in range(63,384+64):
        pb.animate(x+1)
        for y in range(Y):
            p2xys[xy2p[x,y][1][0]].append([x,y])
    return xy2p,p2xys

def get_activations(p2xys,img):
    vs = np.zeros(len(p2xys))
    for i in range(len(p2xys)):
        v = 0.0;
        ctr = 0.0;
        for p in p2xys[i]:
            v += img[p[0],p[1]]
            ctr += 1.0
        vs[i] = v/ctr
    return vs

def get_activation_image(xy2p,vs,W=512):
    X,Y = W,W
    img3 = np.zeros((W,W))
    for x in range(X):
        for y in range(Y):
            v = 0.0
            j = xy2p[x,y][1][0]
            v = vs[j]
            img3[x,y] = v
    return img3

def get_activation_image_avg(xy2p,vs,W=512):
    X,Y = W,W
    img3 = np.zeros((W,W))
    for x in range(X):
        for y in range(Y):
            v = 0.0
            for i in range(len(xy2p[x,y][1])):
                j = xy2p[x,y][1][i]
                v += vs[j]
            img3[x,y] = v/float(len(xy2p[x,y][1]))
    return img3

def get_activation_image_new(xy2p,vs,W=512,num_to_average = 'all'):
    X,Y = W,W
    img3 = np.zeros((W,W))
    if num_to_average == 'all':
        num_to_average = len(xy2p[0,0][1]) # need to insure this will be a good coordinate
    else:
        assert num_to_average > 0
        assert num_to_average <= len(xy2p[0,0][1])
    for x in range(X):
        for y in range(Y):
            v = 0.0
            for i in range(num_to_average):
                j = xy2p[x,y][1][i]
                v += vs[j]
            img3[x,y] = v/num_to_average
    return img3

def get_activation_image_SPECIAL_384x512(xy2p,vs,W=512):
    X,Y = W,W
    img3 = np.zeros((W,W))
    for x in range(63,384+64):
        for y in range(Y):
            v = 0.0
            j = xy2p[x,y][1][0]
            v = vs[j]
            img3[x,y] = v
    return img3


