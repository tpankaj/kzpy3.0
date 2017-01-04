
matplotlib.rcParams.update({'font.size': 22})
matplotlib.rcParams.update({'lines.linewidth': 5})
matplotlib.rcParams.update({'axes.linewidth': 5})
matplotlib.rcParams.update({'lines.markersize': 5})
m = 20
figure(Subject,facecolor="white")
clf()
title(Subject)
#plt.axis((-0.2,1.2,-0.2,1.2))
#plt.axis((-0.2,2.2,-0.2,2.2))
L,H = -0.05,1.1
plt.axis((L,H,L,H))
plt.errorbar(read_letters_face.mean(),read_letters_vase.mean(),xerr=read_letters_face.std()/2.,yerr=read_letters_vase.std()/2.,fmt='go',markersize=m)
plt.errorbar(attend_face_face.mean(),attend_face_vase.mean(),xerr=attend_face_face.std()/2.,yerr=attend_face_vase.std()/2.,fmt='ro',markersize=m)
plt.errorbar(attend_vase_face.mean(),attend_vase_vase.mean(),xerr=attend_vase_face.std()/2.,yerr=attend_vase_vase.std()/2.,fmt='bo',markersize=m)
plt_square()

from matplotlib.backends.backend_pdf import PdfPages

fig = figure(Subject)
pp = PdfPages(opjD(Subject.replace(' ','-')+'.pdf'))
pp.savefig(fig)
pp.close()


"""
http://stackoverflow.com/questions/11328958/matplotlib-pyplot-save-the-plots-into-a-pdf
http://mple.m-artwork.eu/home/posts/plotwithdefinedmarkersizesmatplotlib
http://stackoverflow.com/questions/2553521/setting-axes-linewidth-without-changing-the-rcparams-global-dict
http://stackoverflow.com/questions/3777861/setting-y-axis-limit-in-matplotlib
http://matplotlib.org/1.2.1/examples/pylab_examples/errorbar_demo.html
"""


"""
read_letters_face = [ 0.41259727,  0.34680247,  0.44683756,  0.42942347]
read_letters_vase = [ 0.0590887 , -0.03820697,  0.32833673, -0.01936636]


"""







"""
print read_letters_face
print read_letters_vase
print attend_face_face
print attend_face_vase
print attend_vase_face
print attend_vase_vase

Subject 3
[ 0.41259727  0.34680247  0.44683756  0.42942347]
[ 0.0590887  -0.03820697  0.32833673 -0.01936636]
[ 0.58808767  0.52039153  0.61492028  0.52111527]
[ 0.06834217 -0.00714903  0.40446827 -0.09564282]
[ 0.3674254   0.51343389  0.22434237  0.43945747]
[ 0.73370941  0.52757693  1.52474785  0.5059559 ]


Subject 4
In [31]: print read_letters_face
[ 0.39584415  0.39559313  0.24617282  0.60957163]
In [32]: print read_letters_vase
[ 0.60678831  0.50064961  0.09614785  0.0981875 ]
In [33]: print attend_face_face
[ 0.58843379  0.47088934  0.50833088  0.92941886]
In [34]: print attend_face_vase
[ 0.61504483  0.73635441  0.22892707  0.18019044]
In [35]: print attend_vase_face
[ 0.77063619  0.73204904  0.3962581   1.0288344 ]
In [36]: print attend_vase_vase
[ 1.40933191  1.64137505  0.71286831  0.87557664]


Subject 2
In [33]: print read_letters_face
[ 0.71763869  0.42159721 -0.03216476  1.44424315]
In [34]: print read_letters_vase
[ 0.96532241  1.3443304   0.76276565 -0.56984142]
In [35]: print attend_face_face
[ 0.95569782  1.22139487  1.80024316  2.3008411 ]
In [36]: print attend_face_vase
[ 1.1450332   1.35565584  0.76058068 -0.58213361]
In [37]: print attend_vase_face
[ 0.70857913  0.65094698 -0.31881422  0.71306476]
In [38]: print attend_vase_vase
[ 1.93320083  2.22705538  1.5947047   1.7403502 ]


a=[[ 0.71763869  0.42159721 -0.03216476  1.44424315];
[ 0.96532241  1.3443304   0.76276565 -0.56984142];
[ 0.95569782  1.22139487  1.80024316  2.3008411 ];
[ 1.1450332   1.35565584  0.76058068 -0.58213361]]
d=[[ 0.70857913  0.65094698 -0.31881422  0.71306476];
[ 1.93320083  2.22705538  1.5947047   1.7403502 ]
];





% Subject 3
read_letters =[[ 0.41259727  0.34680247  0.44683756  0.42942347]
				[ 0.0590887  -0.03820697  0.32833673 -0.01936636]]'
attend_face =[[ 0.58808767  0.52039153  0.61492028  0.52111527]
	[ 0.06834217 -0.00714903  0.40446827 -0.09564282]]'
attend_vase =[[ 0.3674254   0.51343389  0.22434237  0.43945747]
		[ 0.73370941  0.52757693  1.52474785  0.5059559 ]]'
[H, pValue, KSstatistic] = kstest_2s_2d(read_letters,attend_face) % p = 0.0257
[H, pValue, KSstatistic] = kstest_2s_2d(read_letters,attend_vase) % p = 0.0257
[H, pValue, KSstatistic] = kstest_2s_2d(attend_face,attend_vase) % p = 0.0257




% Subject 2
read_letters =[[ 0.71763869  0.42159721 -0.03216476  1.44424315]
				[ 0.96532241  1.3443304   0.76276565 -0.56984142]]'
attend_face =[[ 0.95569782  1.22139487  1.80024316  2.3008411 ]
	[ 1.1450332   1.35565584  0.76058068 -0.58213361]]'
attend_vase =[[ 0.70857913  0.65094698 -0.31881422  0.71306476]
		[ 1.93320083  2.22705538  1.5947047   1.7403502 ]]'
[H, pValue, KSstatistic] = kstest_2s_2d(read_letters,attend_face) % p = 0.200
[H, pValue, KSstatistic] = kstest_2s_2d(read_letters,attend_vase) % p = 0.0257
[H, pValue, KSstatistic] = kstest_2s_2d(attend_face,attend_vase) % p = 0.0257




% Subject 4
read_letters =[[ 0.39584415  0.39559313  0.24617282  0.60957163]
[ 0.60678831  0.50064961  0.09614785  0.0981875 ]]'
attend_face =[[ 0.58843379  0.47088934  0.50833088  0.92941886]
[ 0.61504483  0.73635441  0.22892707  0.18019044]]'
attend_vase =[[ 0.77063619  0.73204904  0.3962581   1.0288344 ]
[ 1.40933191  1.64137505  0.71286831  0.87557664]]'
[H, pValue, KSstatistic] = kstest_2s_2d(read_letters,attend_face) % p = 0.200
[H, pValue, KSstatistic] = kstest_2s_2d(read_letters,attend_vase) % p = 0.0257
[H, pValue, KSstatistic] = kstest_2s_2d(attend_face,attend_vase) % p = 0.0257

"""
