import utils.word2vec as w
import constants as c
import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':

    WORD1 = 'happy'
    WORD2 = 'unhappy'

    c.GLOVE_WORD2VEC_FILENAME = 'data/glove.6B.50d.txt'
    w2v = w.load_glove()
    input1 = w.process_word(WORD1, w2v)
    input2 = w.process_word(WORD2, w2v)
    distribution = w.dist_distribution(input1, w2v)
    val = w.l2_dist(input1, input2)
    print(val)

    print(np.mean(val < distribution))
    plt.hist(distribution)
    plt.title("Histogram")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.show()
