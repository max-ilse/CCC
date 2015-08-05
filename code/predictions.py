#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Loading model and predicting text

Karen, Louis  Aug 2015
"""

#-------------------------------------------------------
# libs
#-------------------------------------------------------

import numpy as np
import random
import theano, theano.tensor as T

from model import *
from load_text import *


#-------------------------------------------------------
# helpers
#-------------------------------------------------------

def softmax(x,Temp = 1.):

	e = np.exp(np.array(x) / Temp)
	return e / np.sum(e)


def sample_from(probs, Temp = 1):

	probs = softmax(probs, Temp)
	return np.random.choice(probs.shape[0], 1, p=probs)[0]

def predict(primetext, Temp, length = 50):
	if len(vocabulary(primetext)) == 1: 
		primetext += u' '

	text = primetext
	for i in xrange(length):
		prediction = model.pred_fun([vocabulary(text)])[0,-1]
		prediction[UNKNOWN_idx] = 0
		prediction = prediction/prediction.sum()
		new_syllable = sample_from(prediction, Temp =Temp)
		new_syllable = vocabulary(np.asarray([new_syllable]))
		text+= new_syllable

	return text

#-------------------------------------------------------
# load model and dictonary
#-------------------------------------------------------

DICT = "./allPoetry_4K"
model = "./model_params_GS2.p"
connections = 128

vocabulary = Vocab(syllable2index = DICT)

model = Model(
	input_size=connections,
	hidden_size=connections,
	vocab_size=len(vocabulary),
	stack_size=1, 
	celltype=LSTM,
	load_model = model,
)

UNKNOWN_idx = int(vocabulary(u'xxxx'))

#-------------------------------------------------------
# main loop: generating text
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