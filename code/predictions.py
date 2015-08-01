#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
NOT DONE YET

Karen Ullrich Jun 2015
"""

import numpy as np
import random

import theano, theano.tensor as T

from model import *
from load_text import *
#-------------------------------------------------------
# helpers
#-------------------------------------------------------

#def text2unicode(text):


def softmax(x,Temp = 1.):

	x = np.asarray(x)
	x = np.exp(x/Temp)
	Z = x.sum()

	return x/Z


def sample_from(probs, Temp = 1):

    probs = softmax(probs, Temp)

    totals = []
    running_total = 0

    for w in probs:
        running_total += w
        totals.append(running_total)

    rnd = random.random() * running_total
    for i, total in enumerate(totals):
        if rnd < total:
            return i

#-------------------------------------------------------
# sampling
#-------------------------------------------------------
DICT = './allPoetry_4K'
vocabulary = Vocab(syllable2index = DICT)

model = Model(
        input_size=128,
        hidden_size=128,
        vocab_size=len(vocabulary),
        stack_size=1, # make this bigger, but makes compilation slow
        celltype=LSTM, # use RNN or LSTM
        load_model = "./model_params_GS2.p",
    )
# params
UNKNOWN_idx = int(vocabulary(u'xxxx'))###EINBINDEN
TEMP = 0.003
primetext = u'Du kommst des Weges '


#primetext = text2unicode(text)
text = primetext
for i in xrange(50):
	prediction = model.pred_fun([vocabulary(text)])[0,-1]
	prediction[UNKNOWN_idx] = 0
	new_syllable = sample_from(prediction, Temp =TEMP)
	new_syllable = vocabulary(np.asarray([new_syllable]))
	text+= new_syllable
	

print text 