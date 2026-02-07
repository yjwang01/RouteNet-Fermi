import tensorflow as tf

RNN_DIM = 10

input_tensor = tf.constant([[[1, 2, 3], [4, 5, 6]],
                            [[1, 2, 3], [4, 5, 6]]], dtype=tf.float32)
print("input_tensor shape: ", input_tensor.shape)

path_update = tf.keras.layers.GRUCell(RNN_DIM,
                                      kernel_initializer='ones',
                                      recurrent_initializer='ones',
                                      bias_initializer='ones')
path_update_rnn = tf.keras.layers.RNN(path_update,
                                      return_sequences=True,
                                      return_state=True)

output, final_state = path_update_rnn(input_tensor)

print("output shape: ", output.shape)
print(output)
print("final_state shape: ", final_state.shape)
print(final_state)

# 查看 GRUCell 的权重
for variable in path_update.trainable_variables:
    print(variable.name, variable.shape)
    print(variable.numpy())
