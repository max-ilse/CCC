import sys
import numpy as np
import theano
import time
import theano.tensor as T
from os import path
import cPickle as pickle
import lasagne

from config import *

def save_model(network, save_model):
    
    params = lasagne.layers.get_all_param_values(network)
    pickle.dump(params ,open(save_model, "wb" ))


def load_model(save_dir = '.', save_model = sys.argv[0]):
    
    params = pickle.load(open(path.join(save_dir,save_model ), "rb" ))
    return params


def create_pred_fun(l_out):
	# Theano symbolic vars
	sym_x = T.imatrix()

	# symbolic vars for initial recurrent initial states
	hid1_init_sym = T.matrix()
	hid2_init_sym = T.matrix()

	eval_out = lasagne.layers.get_output(l_out, sym_x, deterministic=True)

	predict = theano.function([sym_x, hid1_init_sym, hid2_init_sym],eval_out)

	return  predict

def softmax(x,Temp = 1.):

	e = np.exp(np.array(x) / Temp)
	return e / np.sum(e)


def sample_from(probs, Temp = 1):

	probs = softmax(probs, Temp)
	probs = probs/np.sum(probs) #numerical stability
	#print probs.shape
	#print probs.sum()
	return np.random.choice(probs.shape[0], 1, p=probs)[0]

def reorder(x_in, batch_size, model_seq_len):
		"""
		Rearranges data set so batches process sequential data.
		If we have the dataset:
		x_in = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
		and the batch size is 2 and the model_seq_len is 3. Then the dataset is
		reordered such that:
					   Batch 1    Batch 2
					------------------------
		batch pos 1  [1, 2, 3]   [4, 5, 6]
		batch pos 2  [7, 8, 9]   [10, 11, 12]
		This ensures that we use the last hidden state of batch 1 to initialize
		batch 2.
		Also creates targets. In language modelling the target is to predict the
		next word in the sequence.
		Parameters
		----------
		x_in : 1D numpy.array
		batch_size : int
		model_seq_len : int
				number of steps the model is unrolled
		Returns
		-------
		reordered x_in and reordered targets. Targets are shifted version of x_in.
		"""
		if x_in.ndim != 1:
				raise ValueError("Data must be 1D, was", x_in.ndim)

		if x_in.shape[0] % (batch_size*model_seq_len) == 0:
				print(" x_in.shape[0] % (batch_size*model_seq_len) == 0 -> x_in is "
							"set to x_in = x_in[:-1]")
				x_in = x_in[:-1]

		x_resize =  \
				(x_in.shape[0] // (batch_size*model_seq_len))*model_seq_len*batch_size
		n_samples = x_resize // (model_seq_len)
		n_batches = n_samples // batch_size

		targets = x_in[1:x_resize+1].reshape(n_samples, model_seq_len)
		x_out = x_in[:x_resize].reshape(n_samples, model_seq_len)

		out = np.zeros(n_samples, dtype=int)
		for i in range(n_batches):
				val = range(i, n_batches*batch_size+i, n_batches)
				out[i*batch_size:(i+1)*batch_size] = val

		x_out = x_out[out]
		targets = targets[out]

		return x_out.astype('int32'), targets.astype('int32')