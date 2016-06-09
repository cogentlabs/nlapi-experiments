from __future__ import print_function

import numpy as np

import constants as c


def load_glove():
    word2vec = {}
    print('[Word2vec] loading glove with {}'.format(c.GLOVE_WORD2VEC_FILENAME))
    i = 0
    with open(c.GLOVE_WORD2VEC_FILENAME) as f:
        for line in f:
            l = line.split()
            word2vec[l[0]] = map(float, l[1:])
            if i != 0 and i % 100000 == 0:
                print('[Word2vec] processed {} words'.format(i))
            i += 1
    print('[Word2vec] processed {} words'.format(i))
    return word2vec


def process_word(word, word2vec, silent=False):
    word_vector_size = len(word2vec.iteritems().next()[1])
    if " " in word:
        words = word.split()
        if ''.join(words) in word2vec:  # compound word
            return process_word(''.join(words), word2vec, silent)
        else:
            merged_word2vec = np.zeros(word_vector_size)
            for w in words:
                merged_word2vec += process_word(w, word2vec, silent)
            merged_word2vec /= len(words)
            return merged_word2vec
    if word not in word2vec:
        create_vector(word, word2vec, word_vector_size, silent)
    return np.array(word2vec[word])


def create_vector(word, word2vec, word_vector_size, silent=False):
    vector = np.random.uniform(0.0, 1.0, (word_vector_size,))
    word2vec[word] = vector
    if not silent:
        print('{} is missing'.format(word))
    return vector


def l2_dist(v1, v2):
    return np.sqrt(np.sum(np.array(v1 - v2) ** 2))


def dist_distribution(inp, w2v):
    dists = np.zeros(len(w2v))
    for i, key in enumerate(w2v):
        dists[i] = l2_dist(inp, w2v[key])
        # print('{} {}'.format(key, dists[i]))
    return dists
