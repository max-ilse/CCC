#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Methods to load wikipedia into strings and build a vocabulary of syllables from it.

"""

__author__      = ["Karen Ullrich"]
__email__       = "karen.ullrich@ofai.at"

#-------------------------------------------------------
# Libraries
#-------------------------------------------------------

import numpy as np
import hyphen # syllable extraction , pip install pyhyphen
from re import findall
from os import listdir
from os.path import join
import random as r
import codecs
import cPickle as pickle

#--------------------------------------
# Methods
#--------------------------------------

## Stream Wiki article-wise (type: unicode)

class Wiki_articles:

    def __init__(self, dir = None, seed =None):

        if dir is None: #Hack for my homedir
            dir = '../data/text/'
        
        files =[]
        subdirs = [ s for s in listdir(dir)]

        for subdir in subdirs:
            tmp = [join(dir,subdir,f) for f in listdir(join(dir,subdir))]
            files.extend(tmp)
        self.files = files

    def __call__(self):
        r.shuffle(self.files)
        for file in self.files:
            f = codecs.open(file, "r", "utf-8",errors='replace')
            for line in f:
                if '<doc ' in line:
                    article = []
                elif '</doc>' in line:
                    yield ''.join(article)
                else:
                    article.append(line)

class Poetry:

    def __init__(self, files= None, dir = None, seed =None):

        if dir is None: #Hack for my homedir
            dir = '../data/poetry/'

        if files == None : self.files = [join(dir,f) for f in listdir(dir)]
        else: self.files = [join(dir,f) for f in files]

        print self.files

    def __call__(self):
        articles = []
        for file in self.files:
            f = codecs.open(file, "r", "utf-8",errors='replace')
            for line in f:
                if '<doc' in line:
                    article = []
                elif '</doc>' in line:
                    articles.append(''.join(article))
                else:
                    article.append(line)

        r.shuffle(articles)
        for article in articles:
            yield article
        


## Builds a vocabulary for the RNN from unicode(!)
class Vocab:
    __slots__ = ["syllable2index", "index2syllable", "unknown"]
    
    def __init__(self, syllable2index = None):

        self.syllable_extractor = hyphen.Hyphenator('de_DE')
        self.syllable2index = {}
        self.index2syllable = []
        
        # load old dictionary if path given
        if syllable2index is not None:
            self.syllable2index = pickle.load( open(syllable2index, "rb"))
            self.index2syllable = ["" for x in range(len(self.syllable2index))]
            for syllable in self.syllable2index.keys():
                self.index2syllable[self.syllable2index[syllable][0]] = syllable

        # add unknown syllable:
        self.add_syllables(u'xxxx')
        self.unknown = self.syllable2index[u'xxxx']
                
    def add_syllables(self, text):
        for word in findall(r"(?u)\w+|[ ,.;!?'%#-]", text.lower()):
            if len(word) < 100:
                syllables = self.syllable_extractor.syllables(word)
                if syllables == []: 
                    if word.isdigit():
                        syllables = word # for numbers
                    else:
                        syllables = [word] # for one-syllable-words and puctuation
                
                if syllables[0].isdigit(): # for years
                            syllables = syllables[0]
                
                for syllable in syllables:
                    if syllable not in self.syllable2index:
                        self.syllable2index[syllable] = [len(self.syllable2index),1] # [idx ,count]
                        self.index2syllable.append(syllable)
                    else: 
                        self.syllable2index[syllable][1] += 1
            else:
                print word, ' could not be included into library of vocabulary. its too long.'

    def __call__(self, line):
        """
        Convert from numerical representation to words
        and vice-versa.
        """
        if type(line) is np.ndarray: 
            return "".join([self.index2syllable[syllable] for syllable in line])
        if type(line) is list:
            if len(line) > 0: # got 
                if line[0] is int:
                    return "".join([self.index2syllable[syllable] for syllable in line])
            indices = np.zeros(len(line), dtype=np.int32)
        else:
            text2syllables = []
            for word in findall(r"(?u)\w+|[ ,.;!?'%#-]", line.lower()):
                if len(word) < 100:
                    syllables = self.syllable_extractor.syllables(word)
                    if syllables == []: 
                        if word.isdigit():
                            syllables = word # for numbers
                        else:
                            syllables = [word] # for one-syllable-words and puctuation
                    
                    if syllables[0].isdigit(): # for years
                                syllables = syllables[0]
                text2syllables.extend(syllables)

            indices = np.zeros(len(text2syllables), dtype=np.int32)

            for i, syllable in enumerate(text2syllables):
                indices[i] = self.syllable2index.get(syllable, self.unknown)[0]
            
            return indices
    
    @property
    def size(self):
        return len(self.index2syllable)

    def __len__(self):
        return len(self.index2syllable)

    def restrict_vocabs(self,max_syllables):
        """
        Restricts the vocabulary to 'max_syllables' available syllables.
        """
        # find threshold 
        num_syllables = len(self.syllable2index)
        if num_syllables <= max_syllables: return

        # sort syllables by occurence
        # probably not hte most clever way to do that
        threshold = np.sort(np.transpose(self.syllable2index.values()))[1][::-1][max_syllables]
        # keep the 'max_syllables' most occuerent syllables
        
        for syllable in self.syllable2index.keys():
            if syllable != u'xxxx':
                if self.syllable2index[syllable][1] < threshold:
                    self.syllable2index.pop(syllable)

        self.index2syllable = [ ]
        for syllable in self.syllable2index.keys():
                self.syllable2index[syllable][0] = len(self.index2syllable)
                self.index2syllable.append(syllable)
                

        # I am aware that the current implementation may yield more than max_syllables 
        # but that seems reasonable to me.

    def show_occurence(self,ylim=10):
        ''' Shows an n-occurence plot

        '''
        import pylab as plt
        plt.plot(np.sort(np.transpose(self.syllable2index.values()))[1][::-1])
        plt.ylim([0,ylim])
        plt.show()

    def save(self, outdir=None):
        '''Saves vocabulary dictionary to file

        '''
        pickle.dump(self.syllable2index, 
            open( join(outdir,'vocabulary'), "wb" ))


class CharMap:
    __slots__ = ["char2index", "index2char", "unknown"]
    
    def __init__(self, char2index = None):

        self.char2index = {}
        self.index2char = []
        
        # load old dictionary if path given
        if char2index is not None:
            self.char2index = pickle.load( open(char2index, "rb"))
            self.index2char = ["" for x in range(len(self.char2index))]
            for char in self.char2index.keys():
                self.index2char[self.char2index[char][0]] = char

            
    def add_char(self, text):
        for char in list(unicode(text)):
            if char not in self.char2index:
                self.char2index[char] = [len(self.char2index),1] # [idx ,count]
                self.index2char.append(char)
            else: 
                self.char2index[char][1] += 1


    def __call__(self, line):
        """
        Convert from numerical representation to words
        and vice-versa.
        """
        #  ints to text
        if type(line) is np.ndarray: 
            return "".join([self.index2char[char] for char in line])
        if type(line) is list:
            if len(line) > 0: # got 
                if line[0] is int:
                    return "".join([self.index2char[char] for char in line])
            indices = np.zeros(len(line), dtype=np.int32)
        # text 2 chars
        else:
            text2chars = list(line)
            indices = np.zeros(len(text2chars), dtype=np.int32)

            for i, char in enumerate(text2chars):
                indices[i] = self.char2index[char][0]
            
            return indices
    
    @property
    def size(self):
        return len(self.index2char)

    def __len__(self):
        return len(self.index2char)


    def save(self, outdir=None):
        '''Saves vocabulary dictionary to file

        '''
        pickle.dump(self.char2index, 
            open( join(outdir,'charmap'), "wb" ))


def main():
    '''
    Go through the wiki corpus and create (and save) a 
    library of all occurring syllables
    '''
    counter = 0
    articles = Wiki_articles()
    vocabulary = Vocab()
    for article in articles():
        counter +=1
        print '\rprogress ', counter
        vocabulary.add_char(article)

    vocabulary.save(outdir='../data/')    

if __name__=="__main__":
    main()