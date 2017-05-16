from keras.models import Sequential
from keras.layers import Dense
import numpy as np

# fix random seed for stoischastic process
np.random.seed(5392)

# loading dataset
dataset = np.loadtxt("data_parser/machine_learning_data_kickstarter.csv", delimiter=",", dtype=str)
# split into input (X) and output (Y) variables
X = dataset[:,0:5931]
Y = dataset[:5931]

model = Sequential()
model.add(Dense(5932, input_dim=5932 activation='relu'))
model.add(Dense(2966, ))
model.add(Dense(1, activation='sigmoid'))

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
print("Fitting Model")
model.fit(X,Y, epochs=20000, batch_size = 25)
scores = model.evaluate(X,Y)
print("\n%s: %.2f%%" %(model.metrics_names[10, scores[1] * 100]))

