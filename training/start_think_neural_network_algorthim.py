from keras.models import Sequential
from keras.layers import Dense
from keras.models import load_model
import numpy as np


def train_data_on_neural_network():
    # fix random seed for stochastic random based process
    np.random.seed(7)

    # loading dataset
    dataset = np.loadtxt("machine_learning_data.csv", delimiter=",", dtype=float)
    # split into input (X) and output (Y) variables
    X = dataset[:,0:510]
    Y = dataset[:,510]
    model = Sequential()
    model.add(Dense(510, input_dim=510, activation='sigmoid'))
    model.add(Dense(255, input_dim=255, activation='sigmoid'))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    print("Fitting Model")
    model.fit(X, Y, epochs=20000, batch_size=100)
    scores = model.evaluate(X, Y)
    print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))
    model.save("C:\Projects\StartThink\model_weights\\start_think_weights_20000_100.h5")

train_data_on_neural_network()
