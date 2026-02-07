import tensorflow as tf
import numpy as np

def generator():
    queue_to_path = [[0], [2], [1, 4], [0, 6], [2, 7, 8]]
    priority = [0, 1, 0, 1, 0]
    queue_size = [32, 32, 32, 32, 32]
    delay = [0.1, 0.2, 0.3, 0.4, 0.5]
    return ({
            "queue_size": tf.constant(np.expand_dims(queue_size, axis=1), dtype=tf.float32),
            "priority": tf.constant(priority, dtype=tf.int32),
            "queue_to_path": tf.ragged.constant(queue_to_path, dtype=tf.int32)
            })

def input_fn():
    ds = tf.data.Dataset.from_generator(generator,
                                        output_signature=
                                            {
                                             "queue_size": tf.TensorSpec(shape=(None, 1), dtype=tf.float32),
                                             "priority": tf.TensorSpec(shape=(None,), dtype=tf.int32),
                                             "queue_to_path": tf.RaggedTensorSpec(shape=(None, 1), dtype=tf.int32)
                                             }
                                        )
                                        # , tf.TensorSpec(shape=(None,), dtype=tf.float32)

    ds = ds.prefetch(tf.data.experimental.AUTOTUNE)

    return ds

# 获取数据集中的第一个元素
for sample in input_fn().take(1):
    data, label = sample
    print(data)
    print(label)