from load_text import Wiki_articles,Poetry,Vocab,CharMap
import lasagne


FILES = ['Goethe_620KB.txt', 'Schiller_340KB.txt']
DICT = 'charmap'
TRAINMODE = 'poetry'
MODEL = 'karneisawesomemodel.p'

vocabulary = CharMap(char2index = DICT) #load vocabulary
vocab_size = len(vocabulary)

BATCH_SIZE = 50                     # batch size
MODEL_SEQ_LEN = 50                 # how many steps to unroll
TOL = 1e-6                          # numerial stability
# model params
INI = lasagne.init.Uniform(0.08)     # initial parameter values
REC_NUM_UNITS = 128                 # number of LSTM units
embedding_size = len(vocabulary)               # Embedding size
dropout_frac = 0.5                    # optional recurrent dropout
#learning params
lr = 0.002                            # learning rate
decay = 0.97                         # decay factor
no_decay_epochs = 10                 # run this many epochs before first decay
max_grad_norm = 10                  # scale steps if norm is above this value
num_epochs = 2                     # Number of epochs to run