
from load_text import Wiki_articles,Poetry,Vocab
import lasagne


FILES = ['Goethe_620KB.txt', 'Schiller_340KB.txt']
DICT = './allPoetry_4K'
TRAINMODE = 'poetry'
MODEL = 'karneisawesomemodel.p'

vocabulary = Vocab(syllable2index = DICT) #load vocabulary
vocab_size = len(vocabulary)

BATCH_SIZE = 10                     # batch size
MODEL_SEQ_LEN = 20                 # how many steps to unroll
TOL = 1e-6                          # numerial stability
# model params
INI = lasagne.init.Uniform(0.1)     # initial parameter values
REC_NUM_UNITS = 100                 # number of LSTM units
embedding_size = 10                # Embedding size
dropout_frac = 0.5                    # optional recurrent dropout
#learning params
lr = 0.1                            # learning rate
decay = 2.0                         # decay factor
no_decay_epochs = 5                 # run this many epochs before first decay
max_grad_norm = 10                  # scale steps if norm is above this value
num_epochs = 1                     # Number of epochs to run
