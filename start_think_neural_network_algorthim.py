from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import SGD
import numpy as np
# fix random seed for random based process
np.random.seed(5392)

# loading dataset
dataset = np.loadtxt("data_parser/machine_learning_data.csv", delimiter=",", dtype=float)
# split into input (X) and output (Y) variables
X = dataset[:, 0:508]
Y = dataset[:, 504:508]


model = Sequential()
model.add(Dense(508, input_dim=508, activation='relu'))
model.add(Dense(254, input_dim=254, activation='relu'))
model.add(Dense(4, activation='sigmoid'))

opt = SGD(lr = 0.01)
model.compile( loss= 'categorical_crossentropy', optimizer= opt, metrics=['accuracy'])
print("Fitting Model")
model.fit(X, Y, epochs=3, batch_size=1)
scores = model.evaluate(X, Y)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

model.save("C:\Projects\StartThink\model_weights\\think_start_weights.h5")
