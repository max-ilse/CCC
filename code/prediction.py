#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
What is it about


Karen Ullrich, Aug 2015
"""

import numpy as np
from os import path
import cPickle as pickle
import time

import lasagne

from config import *

from helpers import *


#-------------------------------------------------------
# load model
#-------------------------------------------------------

from model import *

# params = pickle.load(open(MODEL, "rb" ))

# lasagne.layers.set_all_param_values(l_out, params)

UNKNOWN_idx = int(vocabulary(u'xxxx'))

def predict(primetext, Temp, length = 50):
	print(BATCH_SIZE)
	hid1, hid2 = [np.zeros((BATCH_SIZE, REC_NUM_UNITS), dtype='float32') for _ in range(2)]
	batch_requ_length = (BATCH_SIZE*MODEL_SEQ_LEN)+1
	text = primetext
	for i in xrange(length):
		start = time.time()
		numerical_text  = vocabulary(unicode(text))
		pos = len(numerical_text)
		tokend_seq = np.append(numerical_text,np.asarray(np.zeros(batch_requ_length-pos),dtype='int32'))

		x_pred,_ = reorder(tokend_seq,BATCH_SIZE,MODEL_SEQ_LEN)
		end = time.time()
		print "first", end - start
		start = time.time()
		prediction, hid1, hid2 = f_pred(x_pred,hid1,hid2)
		end = time.time()
		print "f_pred", end - start
		start = time.time()
		prediction = prediction.reshape(BATCH_SIZE*MODEL_SEQ_LEN,vocab_size)[pos]
		prediction[UNKNOWN_idx] = 0
		print(prediction.sum())
		prediction = prediction.astype(np.float64)
		prediction /= prediction.sum()
		print(prediction.sum())
		new_syllable = sample_from(prediction, Temp =Temp)
		end = time.time()
		print "sample", end - start
		start = time.time()
		new_syllable = vocabulary(np.asarray([new_syllable]))
		text += new_syllable
		end = time.time()
		print "rest", end - start

	return text

#-------------------------------------------------------
# main
#-------------------------------------------------------

def main( length = 10 ):
	primetext = "Die "
	temp = 0.01

	# while True:
		# temp = raw_input('Temperature (range (0,1)): ')
		# temp = float(temp)
		# primetext = raw_input('Start peom with: ')
	primetext = unicode(primetext, "utf-8")
	print predict(primetext, temp, length=length)


if __name__ == "__main__":
	main()
