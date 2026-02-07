import numpy as np
import tensorflow as tf

def test1():
    print("Test1: tf.gather_nd()")

    path_state_sequence = tf.constant([
        [[1, 2], [3, 4], [5, 6]],
        [[7, 8], [9, 10], [11, 12]],
        [[13, 14], [15, 16], [17, 18]]
    ])

    path_to_queue = tf.constant([
        [[0, 0], [0, 1], [0, 2]],
        [[1, 2], [1, 1], [1, 0]],
        [[2, 1], [2, 0], [2, 2]]
    ])

    result = tf.gather_nd(path_state_sequence, path_to_queue)

    print("path_state_sequence.shape: ", path_state_sequence.shape)
    print("path_to_queue.shape: ", path_to_queue.shape)
    print("result.shape: ", result.shape)
    print(result)

if __name__ == '__main__':
    print("Hello, TensorFlow!")
    test1()
