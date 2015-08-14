#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
GRU model


Karen Ullrich, Aug 2015
"""

from __future__ import print_function, division
import numpy as np
import os
import time
# import gzip
import cPickle as pickle

import theano
import theano.tensor as T
import lasagne
theano.config.mode = "FAST_RUN"
# theano.config.floatX = 'float32'
# theano.config.profile = True
floatX = theano.config.floatX
print(floatX)

from config import *


def calc_cross_ent(net_output, targets):
		# Helper function to calculate the cross entropy error
		preds = T.reshape(net_output, (BATCH_SIZE * MODEL_SEQ_LEN, vocab_size))
		preds += TOL  # add constant for numerical stability
		targets = T.flatten(targets)
		cost = T.nnet.categorical_crossentropy(preds, targets)
		return cost

#-------------------------------------------------------
# build model
#-------------------------------------------------------

print('Build model ...')
print('vocab_size', vocab_size)

# Theano symbolic vars
sym_x = T.imatrix()
sym_y = T.imatrix()

# symbolic vars for initial recurrent initial states
hid1_init_sym = T.matrix()
hid2_init_sym = T.matrix()


# BUILDING THE MODEL
# Model structure:
#
#    embedding --> GRU1 --> GRU2 --> output network --> predictions
l_inp = lasagne.layers.InputLayer((BATCH_SIZE, MODEL_SEQ_LEN))

l_emb = lasagne.layers.EmbeddingLayer(
		l_inp,
		input_size=vocab_size,       # size of embedding = number of words
		output_size=embedding_size,  # vector size used to represent each word
		W=INI)

l_drp0 = lasagne.layers.DropoutLayer(l_emb, p=dropout_frac)

# first GRU layer
l_rec1 = lasagne.layers.LSTMLayer(
		l_drp0,
		num_units=REC_NUM_UNITS,
		learn_init=False,
		hid_init=hid1_init_sym)

l_drp1 = lasagne.layers.DropoutLayer(l_rec1, p=dropout_frac)

# Second GRU layer
l_rec2 = lasagne.layers.LSTMLayer(
		l_drp1,
		num_units=REC_NUM_UNITS,
		learn_init=False,
		hid_init=hid2_init_sym)

l_drp2 = lasagne.layers.DropoutLayer(l_rec2, p=dropout_frac)

# by reshaping we can combine feed-forward and recurrent layers in the
# same Lasagne model.
l_shp = lasagne.layers.ReshapeLayer(l_drp2,
																		(BATCH_SIZE*MODEL_SEQ_LEN, REC_NUM_UNITS))
l_out = lasagne.layers.DenseLayer(l_shp,
																	num_units=vocab_size,
																	nonlinearity=lasagne.nonlinearities.softmax)
l_out = lasagne.layers.ReshapeLayer(l_out,
																		(BATCH_SIZE, MODEL_SEQ_LEN, vocab_size))

# Note the use of deterministic keyword to disable dropout during evaluation.
train_out, l_rec1_train, l_rec2_train = lasagne.layers.get_output(
		[l_out, l_rec1, l_rec2], sym_x, deterministic=False)
hidden_states_train = [l_rec1_train, l_rec2_train]

eval_out, l_rec1_eval, l_rec2_eval = lasagne.layers.get_output(
		[l_out, l_rec1, l_rec2], sym_x, deterministic=True)
hidden_states_eval = [l_rec1_eval, l_rec2_eval]

# Use cross-entropy cost
cost_train = T.mean(calc_cross_ent(train_out, sym_y))
cost_eval = T.mean(calc_cross_ent(eval_out, sym_y))

# Get list of all trainable parameters in the network.
all_params = lasagne.layers.get_all_params(l_out, trainable=True)
print(lasagne.layers.count_params(l_out))

# Calculate gradients w.r.t cost function. Note that we scale the cost with
# MODEL_SEQ_LEN. This is to be consistent with
# https://github.com/wojzaremba/lstm . The scaling is due to difference
# between torch and theano. We could have also scaled the learning rate, and
# also rescaled the norm constraint.
all_grads = T.grad(cost_train*MODEL_SEQ_LEN, all_params)

# With the gradients for each parameter we can calculate update rules for each
# parameter. Lasagne implements a number of update rules, here we'll use
# sgd and a total_norm_constraint.
all_grads, norm = lasagne.updates.total_norm_constraint(
		all_grads, max_grad_norm, return_norm=True)

# Use shared variable for learning rate. Allows us to change the learning rate
# during training.
sh_lr = theano.shared(lasagne.utils.floatX(lr))

#-------------------------------------------------------
# define learning
#-------------------------------------------------------

updates = lasagne.updates.rmsprop(all_grads, all_params, learning_rate=sh_lr)

# Define evaluation function. This graph disables dropout.
print("compiling f_eval...")
# fun_inp = [sym_x, sym_y, hid1_init_sym, hid2_init_sym]
# f_eval = theano.function(fun_inp,
# 												 [cost_eval,
# 													hidden_states_eval[0][:, -1],
# 													hidden_states_eval[1][:, -1]])

# define training function. This graph has dropout enabled.
# The update arg specifies that the parameters should be updated using the
# update rules.
print("compiling f_train...")
# f_train = theano.function(fun_inp,
# 													[cost_train,
# 													 norm,
# 													 hidden_states_train[0][:, -1],
# 													 hidden_states_train[1][:, -1]],
# 													updates=updates)

print("compiling f_pred...")
f_pred = theano.function([sym_x, hid1_init_sym, hid2_init_sym],
									[eval_out,
									hidden_states_eval[0][:, -1],
									hidden_states_eval[1][:, -1]],
									mode='FAST_RUN')
