
import caffe
from kzpy3.utils import *

def conv(top,bottom,num_output,group,kernel_size,stride,pad,weight_filler_type,std=0):
	p = """
layer {
\tname: "TOP"
\ttype: "Convolution"
\tbottom: "BOTTOM"
\ttop: "TOP"
\tconvolution_param {
\t\tnum_output: NUM_OUTPUT
\t\tgroup: NUM_GROUP
\t\tkernel_size: KERNEL_SIZE
\t\tstride: STRIDE
\t\tpad: PAD
\t\tweight_filler {
\t\t\ttype: "WEIGHT_FILLER_TYPE" STD
\t\t}
\t}
}
	"""
	p = p.replace("TOP",top)
	p = p.replace("BOTTOM",bottom)
	p = p.replace("NUM_OUTPUT",str(num_output))
	p = p.replace("NUM_GROUP",str(group))
	p = p.replace("KERNEL_SIZE",str(kernel_size))
	p = p.replace("STRIDE",str(stride))
	p = p.replace("PAD",str(pad))
	p = p.replace("WEIGHT_FILLER_TYPE",weight_filler_type)
	if weight_filler_type == 'gaussian':
		p = p.replace("STD","\n\t\t\tstd: "+str(std))
	else:
		p = p.replace("STD","")
	return p

def relu(bottom):
	p = """
layer {
\tname: "BOTTOM_relu"
\ttype: "ReLU"
\tbottom: "BOTTOM"
\ttop: "BOTTOM"
}
	"""
	p = p.replace("BOTTOM",bottom)
	return p

def pool(bottom,p_type,kernel_size,stride,pad=0):
	p = """
layer {
\tname: "BOTTOM_pool"
\ttype: "Pooling"
\tbottom: "BOTTOM"
\ttop: "BOTTOM_pool"
\tpooling_param {
\t\tpool: POOL_TYPE
\t\tkernel_size: KERNEL_SIZE
\t\tstride: STRIDE
\t\tpad: PAD
\t}
}
	"""
	p = p.replace("BOTTOM",bottom)
	p = p.replace("POOL_TYPE",p_type)
	p = p.replace("KERNEL_SIZE",str(kernel_size))
	p = p.replace("STRIDE",str(stride))
	p = p.replace("PAD",str(pad))
	return p

def conv_layer_set(
	c_top,
	c_bottom,
	c_num_output,
	c_group,
	c_kernel_size,
	c_stride,
	c_pad,
	p_type,
	p_kernel_size,
	p_stride,
	p_pad,
	weight_filler_type,std=0):
	p = """\n###################### Convolutional Layer Set '"""+c_top+"""' ######################\n#"""
	p = p + conv(c_top,c_bottom,c_num_output,c_group,c_kernel_size,c_stride,c_pad,weight_filler_type,std)
	p = p + relu(c_top)
	p = p + pool(c_top,p_type,p_kernel_size,p_stride,p_pad)
	p = p + '\n############################################################\n\n'
	return p

def dummy(top,dims):
	p = """
layer {
\tname: "TOP"
\ttype: "DummyData"
\ttop: "TOP"
\tdummy_data_param {
\t\tshape {
DIMS
    }
  }
}
	"""
	p = p.replace('TOP',top)
	d = ""
	for i in range(len(dims)):
		d = d + d2s('\t\t\tdim:',dims[i],'\n')
	p = p.replace('DIMS',d)
	return p

def python(top,bottom,module,layer):
	p = """
layer {
\ttype: 'Python'
\tname: 'TOP'
\tbottom: 'BOTTOM'
\ttop: 'TOP'
\tpython_param {
\t\tmodule: 'MODULE'
\t\tlayer: 'LAYER'
\t}
}
	"""
	p = p.replace('TOP',top)
	p = p.replace('BOTTOM',bottom)
	p = p.replace('MODULE',module)
	p = p.replace('LAYER',layer)
	return p

def dummy(top,dims):
	p = """
layer {
\tname: "TOP"
\ttype: "DummyData"
\ttop: "TOP"
\tdummy_data_param {
\t\tshape {
DIMS
    }
  }
}
	"""
	p = p.replace('TOP',top)
	d = ""
	for i in range(len(dims)):
		d = d + d2s('\t\t\tdim:',dims[i],'\n')
	p = p.replace('DIMS',d)
	return p

def python(top,bottom,module,layer):
	p = """
layer {
\ttype: 'Python'
\tname: 'TOP'
\tbottom: 'BOTTOM'
\ttop: 'TOP'
\tpython_param {
\t\tmodule: 'MODULE'
\t\tlayer: 'LAYER'
\t}
}
	"""
	p = p.replace('TOP',top)
	p = p.replace('BOTTOM',bottom)
	p = p.replace('MODULE',module)
	p = p.replace('LAYER',layer)
	return p

def ip(top,bottom,num_output,weight_filler_type,std=0):
	p = """
layer {
\tname: "TOP"
\ttype: "InnerProduct"
\tbottom: "BOTTOM"
\ttop: "TOP"
\tinner_product_param {
\t\tnum_output: NUM_OUTPUT
\t\tweight_filler {
\t\t\ttype: "WEIGHT_FILLER_TYPE" STD
\t\t}
\t}
}
	"""
	p = p.replace("TOP",top)
	p = p.replace("BOTTOM",bottom)
	p = p.replace("NUM_OUTPUT",str(num_output))
	p = p.replace("WEIGHT_FILLER_TYPE",weight_filler_type)
	if weight_filler_type == 'gaussian':
		p = p.replace("STD","\n\t\t\tstd "+str(std))
	else:
		p = p.replace("STD","")
	return p

def ip_layer_set(top,bottom,num_output,weight_filler_type,std=0):
	p = """\n###################### IP Layer Set '"""+top+"""' ######################\n#"""
	p = p + ip(top,bottom,num_output,weight_filler_type,std)
	p = p + relu(top)
	p = p + '\n############################################################\n\n'
	return p

def euclidian(top,bottom1,bottom2):
	p = """
layer {
\tname: "TOP"
\ttype: "EuclideanLoss"
\tbottom: "BOTTOM1"
\tbottom: "BOTTOM2"
\ttop: "TOP"
\tloss_weight: 1
}
	"""
	p = p.replace("TOP",top)
	p = p.replace("BOTTOM1",bottom1)
	p = p.replace("BOTTOM2",bottom2)
	return p



def solver(model_name):
	p = """
net: "Desktop/train_val.prototxt"
test_iter: 1
test_interval: 1000000
test_initialization: false
base_lr: 0.0001  # 0.00005
momentum: 0.01
weight_decay: 0.0005
lr_policy: "inv"
gamma: 0.0001
power: 0.75
display: 10000
max_iter: 1000000
snapshot: 100000
snapshot_prefix: "scratch/2016/caffemodels/MODEL_NAME"
	"""
	p = p.replace('MODEL_NAME',model_name)
	return p



