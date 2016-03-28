
import caffe
from kzpy3.utils import *

def conv(top,bottom,num_output,groups,kernel_size,stride,pad,weight_filler_type,std=0):
	p = """
layer {
\tname: "TOP"
\ttype: "Convolution"
\tbottom: "BOTTOM"
\ttop: "TOP"
\tconvolution_param {
\t\tnum_output: NUM_OUTPUT
\t\tgroup: NUM_GROUPS
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
	p = p.replace("NUM_GROUPS",str(groups))
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

def pool(bottom,pool_type,kernel_size,stride,pad=0):
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
	p = p.replace("POOL_TYPE",pool_type)
	p = p.replace("KERNEL_SIZE",str(kernel_size))
	p = p.replace("STRIDE",str(stride))
	p = p.replace("PAD",str(pad))
	return p

def conv_layer_set(
	conv_top,
	conv_bottom,
	conv_num_output,
	conv_num_groups,
	conv_kernel_size,
	conv_stride,
	conv_pad,
	pool_type,
	pool_kernel_size,
	pool_stride,
	pool_pad,
	weight_filler_type,std=0):
	p = """\n###################### Convolutional Layer Set '"""+conv_top+"""' ######################\n#"""
	p = p + conv(conv_top,conv_bottom,conv_num_output,conv_num_groups,conv_kernel_size,conv_stride,conv_pad,weight_filler_type,std)
	p = p + relu(conv_top)
	p = p + pool(conv_top,pool_type,pool_kernel_size,pool_stride,pool_pad)
	p = p + '\n############################################################\n\n'
	return p









