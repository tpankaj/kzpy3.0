from kzpy3.teg7.data.preprocess_bag_data import *

run_paths = sgg(opjD('bair_car_data','meta','*'))

for r in run_paths:
	if 'lost' not in r:

		left_filename = gg(opj(r,'left_image_bound_to_data*'))[0]
		L = load_obj(left_filename)

		ts = sorted(L.keys())

		dts = []

		for i in range(1,len(ts)):
			dt = ts[i]-ts[i-1]
			if dt > 1.2:
				dt = 1.2
			dts.append(dt)
		figure(1)
		clf()
		plot(ts[1:],dts)
		plt.title(fname(r))
		figure(5)
		clf()
		hist(dts)
		plt.title(fname(r))
		pause(1)