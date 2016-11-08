from kzpy3.teg2.gps_fence.fourth_3 import *
from kzpy3.teg2.gps_fence.geometry import *

ar = np.array

o = ar([0.,0.])
w = 0.4
v1 = ar([1.,1.])
v1_ = ar([0,1])
d = 0.1
h=0.3

def pt_plot(p):
	plt.plot(p[0],p[1],'o')

def line_plot(p1,p2):
	plt.plot([p1[0],p2[0]],[p1[1],p2[1]],'r-')

def get_pts(v1,w,h,graphics=False):
	v1 = na(v1)
	m = np.sqrt(v1[0]**2 + v1[1]**2)
	u1 = v1 / m
	v2 = -w * u1
	v3a = rotatePoint(o,v2,90)
	v3b = rotatePoint(o,v2,-90)
	v4a = v1 + v3a
	v4b = v1 + v3b
	v5a = ar([d*v4a[0]/v4a[1],d])
	v5b = ar([d*v4b[0]/v4b[1],d])
	if graphics:
		plt.figure(3)
		#clf()
		plt.plot([-2,2],[d,d])
		pt_plot(o)
		pt_plot(v4a);pt_plot(v4b)
		pt_plot(v1)
		#line_plot(o,v4a)
		#line_plot(o,v4b)		
		line_plot(o,v5a)
		line_plot(o,v5b)
		plt.xlim(-2,2);plt.ylim(-2,2)
		plt_square()
	return v5a[0],v5b[0],m


def get_pts2(v1,w,h,d,graphics=False):
	v1 = na(v1)
	m = np.sqrt(v1[0]**2 + v1[1]**2)
	a,b,m2 = get_pts([0,m],w,d,False)
	object_screen_width = np.abs(a-b)
	a2,b2,m3 = get_pts(v1,0.00001,d,False)
	v_center = [a2,d]
	v_left = [a2-object_screen_width/2.,d]
	v_right = [a2+object_screen_width/2.,d]
	v_bottom = [h*(1-d/m),d]
	if False:
		if graphics:
			plt.figure(3)
			#clf()
			plt.plot([-2,2],[d,d])
			pt_plot(o)
			line_plot(o,v1)
			line_plot(o,v_left)
			line_plot(o,v_right)
			plt.xlim(-2,2);plt.ylim(-2,2)
			plt_square()

	x0 = v_left[0]
	y0 = -v_bottom[0]
	x1 = v_right[0]
	y1 = -v_bottom[0]
	x2 = v_left[0]
	y2 = h/w*object_screen_width-v_bottom[0]
	x3 = v_right[0]
	y3 = h/w*object_screen_width-v_bottom[0]
	if graphics:
		plt.figure(3)
		plot([x0,x1,x3,x2,x0],[-y0,-y1,-y3,-y2,-y0])
	return [[x0,y0],[x1,y1],[x2,y2],[x3,y3]],m


def pt_to_img_coordinates(pt):
	pt = na(pt)
	pt *= 600.
	pt[0] += 100
	pt[1] += 50
	return pt

def get_pts3(v1,w,h,d,graphics=False):
	pts,m = get_pts2(v1,w,h,d,True)
	img_pts = []
	for p in pts:
		img_pts.append(pt_to_img_coordinates(p))
	if graphics:
		figure(4)
		plt_square()
		plt.xlim(0,200)
		plt.ylim(0,100)

		#line_plot(img_pts[0],img_pts[1])
		#line_plot(img_pts[1],img_pts[2])
		#line_plot(img_pts[2],img_pts[3])
		#line_plot(img_pts[3],img_pts[0])
		x1 = int(img_pts[0][0])
		x2 = int(img_pts[1][0])
		y1 = int(img_pts[1][1])
		y2 = int(img_pts[3][1])
		plot([x1,x2],[y1,y1],'r')
		plot([x1,x2],[y2,y2],'r')
		plot([x1,x1],[y1,y2],'r')
		plot([x2,x2],[y1,y2],'r')
	return img_pts,m



def mi_picture(img_pts,m,graphics=False):
	global img
	x1 = int(img_pts[0][0])
	x2 = int(img_pts[1][0])
	y1 = int(img_pts[1][1])
	y2 = int(img_pts[3][1])

	img[y1:y2,x1:x2] = 1/(10.0*m)

	if graphics:
		mi(img,2)










if True:

	screen_distance = 0.1

	img = zeros((300,300))

	p = Points()
	for i in range(1000):
		img *= 0
		pts_R = p.do_update()
		figure(3)
		clf()
		plt.xlim(-0.5,0.5)
		plt.ylim(-0.5,0.5)
		figure(2)
		clf()
		plt.xlim(-1.5,1.5)
		plt.ylim(-1.5,1.5)
		plot(0,0,'ko')
		plot(pts_R[:,0],pts_R[:,1],'b.')
		


		dist = []
		for rp in pts_R:
			dist.append(np.sqrt(rp[0]**2+rp[1]**2))

		pts_V = []
		pts_A = []

		import operator
		dist_sorted = sorted(enumerate(dist), key=operator.itemgetter(1))
		for i in range(len(dist_sorted)-1,-1,-1):
			s = dist_sorted[i]
			rp = pts_R[s[0]]
			x = rp[0]
			y = rp[1]
			pts_A.append([x,y])
			if y > 0:#screen_distance:
				if np.rad2deg(angle_between([1,0],[x,y])) > 30:
					if np.rad2deg(angle_between([1,0],[x,y])) < 180-30:
						pts_V.append([x,y])
		figure(2)
		for pt in pts_A:
			x = pt[0]
			y = pt[1]
			plot(x,y,'bx')
		for pt in pts_V:
			x = pt[0]
			y = pt[1]
			figure(2)
			plot(x,y,'ro')
			img_pts,m = get_pts3([x,y],0.02,0.08,screen_distance,False)
			mi_picture(img_pts,m,False)
		img[100,0]=0.33
		mi(img,'img')#mi(img[:,50:150],'img')
		plt.pause(0.001)
