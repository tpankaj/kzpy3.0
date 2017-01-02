"""
This code is not necessary
"""


img = imread('/Users/karlzipser/2015/12/Research/data/experiments/Kendrick_Kay_visit_19to26June2015/Vermeer/attend_face/subjects/S6_2015/2015/6/21/0/stats/pp_a0/p_images/png_std/4.png')

big = imread('/Users/karlzipser/2015/12/Research/stimuli/Kendrick_Kay_visit_19to26June2015/Vermeer/Vermeer_4_1024x768.png')

p_img_big = imresize(img,8.0)

z=zscore(p_img_big)

y = z.copy()

y[y<0]=0

b = z.copy()

b[b>0]=0

b = -b

ci = yb_color_modulation_of_grayscale_image(big,y,b,True);mi(ci)

paintings = ['woman+chair','woamn+vase','man','artist']
sizes = [1.0,1.2,1.4]
flip = [False,True]

p_images_path = 
ctr = 0
for p in paintings:
	for f in flip:
		for s in sizes:
			print((p,f,s))
			ctr += 1



def center_img_A_in_img_B(A,B):
	sA = shape(A)
	sB = shape(B)
	assert(len(sA)==len(sB))
	assert(sA[0]<=sB[0])
	assert(sA[1]<=sB[1])
	if len(sA)==3:
		assert(sA[2]==sB[2])
		B[sB[0]/2-sA[0]/2:sB[0]/2+sA[0]/2,sB[1]/2-sA[1]/2:sB[1]/2+sA[1]/2,:] = A
	else:
		B[sB[0]/2-sA[0]/2:sB[0]/2+sA[0]/2,sB[1]/2-sA[1]/2:sB[1]/2+sA[1]/2] = A

def extract_from_center(A,B):
	sA = shape(A)
	sB = shape(B)
	assert(len(sA)==len(sB))
	assert(sA[0]<=sB[0])
	assert(sA[1]<=sB[1])
	if len(sA)==3:
		assert(sA[2]==sB[2])
		A[:,:,:] = B[sB[0]/2-sA[0]/2:sB[0]/2+sA[0]/2,sB[1]/2-sA[1]/2:sB[1]/2+sA[1]/2,:]
	else:
		A[:,:] = B[sB[0]/2-sA[0]/2:sB[0]/2+sA[0]/2,sB[1]/2-sA[1]/2:sB[1]/2+sA[1]/2]


