from kzpy3.utils import *

def start_gstreamter():
	img_path = opjh('Desktop/RPi_data',time_str())
	unix(d2s('mkdir -p',img_path))
	p = subprocess.Popen(["gsomesomethings","test2.py"])
	return p


