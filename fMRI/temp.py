roi,voxIdx,snr,data,good_voxels = load_subject('S3','/Users/karlzipser/scratch/2015/8/20/KK2008_part/subject-S3')

selected_voxels = load_obj('/Users/karlzipser/scratch/2015/8/20/KK2008_part/subject-S3/rfs/exclude_0.120/selected_voxels')

for roi_id in range(1,3):

	V_count = 0
	V_selected_count = 0



	for i in range(len(roi)):
		r = roi[i]
		if r == roi_id:
			V_count += 1
			if i in selected_voxels:
				V_selected_count += 1

	print (roi_id,V_count,V_selected_count,V_selected_count/(1.0*V_count))



	"""
S1
	V1
		2858 voxels
		1501 selected
		53%

	V2
		4531 voxels
		1789 selected
		39%

S2
	V1
		3281 voxels
		1119 selected
		34%

	V2
		4381 voxels
		1024 selected
		23%

S3
	V1
		2818 voxels
		1277 selected
		45%

	V2
		4157 voxels
		1121 selected
		27%



	"""


#

