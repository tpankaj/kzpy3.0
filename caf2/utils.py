
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
		p = p.replace("STD","\n\t\t\tstd "+str(std))
	else:
		p = p.replace("STD","")
	return p

def relu(bottom):
	p = """
layer {
\tname: "BOTTOM_relu"
\ttype: "ReLu"
\tbottom: "BOTTOM_relu"
\ttop: "BOTTOM_relu"
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
print dummy('Dummy1',(1,9,225,300))

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
print dummy('Dummy1',(1,9,225,300))

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






# testing

p = dummy('ddata',(1,9,225,300))
p = p + dummy('ddata2',(1,60))
p = p + python('py_image_data','ddata','kz_layers2','SimpleLayer4')
p = p + python('py_target_data','ddata2','kz_layers2','SimpleLayer5')
p = p + conv_layer_set(
	c_top='conv1',c_bottom='ddata',c_num_output=96,c_group=1,c_kernel_size=11,c_stride=3,c_pad=0,
	p_type='MAX',p_kernel_size=3,p_stride=2,p_pad=0,
	weight_filler_type='gaussian',std=0.1)
p = p + conv_layer_set(
	c_top='conv2',c_bottom='conv1',c_num_output=96,c_group=1,c_kernel_size=11,c_stride=3,c_pad=0,
	p_type='MAX',p_kernel_size=3,p_stride=2,p_pad=0,
	weight_filler_type='gaussian',std=0.1)
p = p + ip_layer_set('ip1','conv2',512,'xavier')
p = p + ip_layer_set('ip2','ip1',3,'xavier')
print p






"""

#####################


#####################


"""




