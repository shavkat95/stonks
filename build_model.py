from tensorflow import keras
from tensorflow.python.keras.utils.generic_utils import get_custom_objects
from keras.layers import Activation
import numpy as np




negative_slopes = np.full(11, 0.1)

def set_leakies():
    global negative_slopes
    
    global custom_leaky
    def custom_leaky(x):
        return keras.activations.leaky_relu(x, negative_slope=negative_slopes[0])

    global custom_leaky_1
    def custom_leaky_1(x):
        return keras.activations.leaky_relu(x, negative_slope=negative_slopes[1])

    global custom_leaky_2
    def custom_leaky_2(x):
        return keras.activations.leaky_relu(x, negative_slope=negative_slopes[2])

    global custom_leaky_3
    def custom_leaky_3(x):
        return keras.activations.leaky_relu(x, negative_slope=negative_slopes[3])

    global custom_leaky_4
    def custom_leaky_4(x):
        return keras.activations.leaky_relu(x, negative_slope=negative_slopes[4])

    global custom_leaky_5
    def custom_leaky_5(x):
        return keras.activations.leaky_relu(x, negative_slope=negative_slopes[5])

    global custom_leaky_6
    def custom_leaky_6(x):
        return keras.activations.leaky_relu(x, negative_slope=negative_slopes[6])

    global custom_leaky_7
    def custom_leaky_7(x):
        return keras.activations.leaky_relu(x, negative_slope=negative_slopes[7])

    global custom_leaky_8
    def custom_leaky_8(x):
        return keras.activations.leaky_relu(x, negative_slope=negative_slopes[8])

    global custom_leaky_9
    def custom_leaky_9(x):
        return keras.activations.leaky_relu(x, negative_slope=negative_slopes[9])

    global custom_leaky_10
    def custom_leaky_10(x):
        return keras.activations.leaky_relu(x, negative_slope=negative_slopes[10])

def set_slopes_1(value = -1):
    global negative_slopes
    for sl in negative_slopes:
        if value > 0:
            sl = value
        sl = sl + np.random.normal(0, 0.04)
        sl = max(0, sl)
        
set_slopes_1()
set_leakies()

def unison_shuffled_copies(a, b):
    assert len(a) == len(b)
    p = np.random.permutation(len(a))
    return (a[p], b[p])

def build_model(model_head = "bitcoin"):
    pass

class CustomCallback(keras.callbacks.Callback):

    def on_epoch_end(self, epoch, logs=None):
        print('\n')
        print('\n')
        global x_train
        global y_train
        (x_train, y_train) = unison_shuffled_copies(x_train, y_train)


my_callbacks = [
    keras.callbacks.ModelCheckpoint(filepath='model.{val_loss:.2f}.keras'),
    CustomCallback()
]

# model = tf.keras.models.load_model('model.keras', custom_objects={'custom_leaky':custom_leaky, "custom_activation": custom_activation})