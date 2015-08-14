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

params = pickle.load(open(MODEL, "rb" ))

lasagne.layers.set_all_param_values(l_out, params)



def predict(primetext, Temp, length = 50):
	hid1, hid2 = [np.zeros((BATCH_SIZE, REC_NUM_UNITS), dtype='float32') for _ in range(2)]
	batch_requ_length = (BATCH_SIZE*MODEL_SEQ_LEN)+1
	text = unicode(primetext)
	for i in xrange(length):
		numerical_text  = vocabulary(unicode(text))	
		pos = len(numerical_text)
		tokend_seq = np.append(numerical_text,np.asarray(np.zeros(batch_requ_length-pos),dtype='int32'))

		x_pred,_ = reorder(tokend_seq,BATCH_SIZE,MODEL_SEQ_LEN)
		prediction, hid1, hid2 = f_pred(x_pred,hid1,hid2)
		prediction = prediction.reshape(BATCH_SIZE*MODEL_SEQ_LEN,vocab_size)[pos]
		new_syllable = sample_from(prediction, Temp =Temp)
		new_syllable = vocabulary(np.asarray([new_syllable]))
		text += new_syllable

	return text

#-------------------------------------------------------
# main 
#-------------------------------------------------------

def main( length = 100 ):

	while True:
		temp = raw_input('Temperature (range (0,1)): ')
		temp = float(temp)
		primetext = raw_input('Start peom with: ')
		primetext = unicode(primetext, "utf-8")	
		print predict(primetext, temp, length=length)


if __name__ == "__main__":
	main()   