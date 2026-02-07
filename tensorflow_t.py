import numpy as np
import tensorflow as tf

class RouteNet_Fermi(tf.keras.Model):
    def __init__(self):
        self.max_num_queues = 2
        self.queue_state_dim = 8
        super(RouteNet_Fermi, self).__init__()
        self.queue_embedding = tf.keras.Sequential([
                    tf.keras.layers.Input(shape=self.max_num_queues + 1),
                    tf.keras.layers.Dense(self.queue_state_dim, activation=tf.keras.activations.relu),
                    tf.keras.layers.Dense(self.queue_state_dim, activation=tf.keras.activations.relu)
                ])
    def call(self, inputs):
        import pdb;pdb.set_trace()
        queue_size = inputs['queue_size']
        priority = tf.one_hot(inputs['priority'], self.max_num_queues)
        queue_to_path = inputs['queue_to_path']
        queue_state = self.queue_embedding(
            tf.concat([queue_size, priority], axis=1))
        
        queue_gather = tf.gather(queue_state, queue_to_path)


        queue_gather = tf.reduce_sum(queue_gather, axis=1)
        # print(queue_gather)

def generator():
    queue_to_path = [[0], [2], [1, 4], [0, 6], [2, 7, 8]]
    priority = [0, 1, 0, 1, 0, 1, 0, 1, 0]
    queue_size = [32, 32, 32, 32, 32, 32, 32, 32, 32]
    delay = [0.1, 0.2, 0.3, 0.4, 0.5]
    return ({
            "queue_size": tf.constant(np.expand_dims(queue_size, axis=1), dtype=tf.float32),
            "priority": tf.constant(priority, dtype=tf.int32),
            "queue_to_path": tf.ragged.constant(queue_to_path)
            }, tf.constant(delay, dtype=tf.float32))

def input_fn():
    ds = tf.data.Dataset.from_generator(generator,
                                        output_signature=
                                            {
                                             "queue_size": tf.TensorSpec(shape=(None, 1), dtype=tf.float32),
                                             "priority": tf.TensorSpec(shape=None, dtype=tf.int32),
                                             "queue_to_path": tf.RaggedTensorSpec(shape=(None, 1), dtype=tf.int32),
                                             }
                                        )

    ds = ds.prefetch(tf.data.experimental.AUTOTUNE)

    return ds

# def generator():
#     queue_to_path = [[0], [2], [1, 4], [0, 6], [2, 7, 8]]
#     return {"queue_to_path": tf.ragged.constant(queue_to_path)}

if __name__ == "__main__":
    # queue_state = tf.constant([[11, 21, 31, 41, 51, 61, 71, 81, 91],
    #                       [12, 22, 32, 42, 52, 62, 72, 82, 92],
    #                       [13, 23, 33, 43, 53, 63, 73, 83, 93],
    #                       [14, 24, 34, 44, 54, 64, 74, 84, 94],
    #                       [15, 25, 35, 45, 55, 65, 75, 85, 95],
    #                       [16, 26, 36, 46, 56, 66, 76, 86, 96],
    #                       [17, 27, 37, 47, 57, 67, 77, 87, 97],
    #                       [18, 28, 38, 48, 58, 68, 78, 88, 98],
    #                       [19, 29, 39, 49, 59, 69, 79, 89, 99],
    #                       [10, 20, 30, 40, 50, 60, 70, 80, 90]])

    # ds = tf.data.Dataset.from_generator(
    #     generator,
    #     output_signature=(
    #         {"queue_to_path": tf.RaggedTensorSpec(shape=(None, 1), dtype=tf.int32)}
    #     )
    # )
    tf.config.run_functions_eagerly(True)

    ds = input_fn()
    ds = ds.prefetch(tf.data.experimental.AUTOTUNE)
    ds = ds.repeat()

    optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)

    model = RouteNet_Fermi()

    loss_object = tf.keras.losses.MeanAbsolutePercentageError()

    model.compile(loss=loss_object,
                  optimizer=optimizer,
                  run_eagerly=False)
    
    # cp_callback = tf.keras.callbacks.ModelCheckpoint(
    #     filepath=filepath,
    #     verbose=1,
    #     mode="min",
    #     monitor='val_loss',
    #     save_best_only=False,
    #     save_weights_only=True,
    #     save_freq='epoch')

    model.fit(ds,
              epochs=50,
              steps_per_epoch=2000,
              validation_data=ds,
              validation_steps=200,
            #   callbacks=[cp_callback],
              use_multiprocessing=True)
    
