import tensorflow as tf
import numpy as np
import pandas as pd
import sys
import os
from tensorflow.python.ops import control_flow_ops
from tqdm import tqdm
from matplotlib import pyplot as plt
from copy import deepcopy
from tensorflow.examples.tutorials.mnist import input_data
import RBM
import rnn_rbm
import time
import midi_manipulation

"""
    This file contains the code for running a tensorflow session to generate music
"""

num = 3  # The number of songs to generate


def main(saved_weights_path, songList):
    # Primer
    songList = songList.split(',')
    primer_song = songList[0]  # The path to the song to use to prime the network
    song_primer = midi_manipulation.get_song(primer_song)

    # This function takes as input the path to the weights of the network
    x, cost, generate, W, bh, bv, x, lr, Wuh, Wuv, Wvu, Wuu, bu, u0 = rnn_rbm.rnnrbm()  # First we build and get the parameters odf the network

    tvars = [W, Wuh, Wuv, Wvu, Wuu, bh, bv, bu, u0]

    saver = tf.train.Saver(tvars)  # We use this saver object to restore the weights of the model

    # check folder existence
    directory = (sys.path[0] + '/music_outputs')
    if not os.path.exists(directory):
        os.makedirs(directory)

    with tf.Session() as sess:
        init = tf.global_variables_initializer()
        sess.run(init)
        print(saved_weights_path)
        saver.restore(sess, saved_weights_path)  # load the saved weights of the network
        # #We generate num songs
        for i in tqdm(range(num)):
            generated_music = sess.run(generate(300), feed_dict={
                x: song_primer})  # Prime the network with song primer and generate an original song
            new_song_path = (sys.path[0] + "\music_outputs\Song-{}".format(i))
            midi_manipulation.write_song(new_song_path, generated_music)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
