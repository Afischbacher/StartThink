from keras.models import load_model
import numpy as np
import csv

np.random.seed(7)  # to ensure a stochastic process

actual_data = []
predicted_data = []


def test_data():
    model = load_model("../model_weights/start_think_weights_25000_100.h5")  # load the model

    # loading dataset
    dataset = np.loadtxt("../testing/Test 2017-06-16/machine_testing_data_2017_06_16.csv", delimiter=",",
                         dtype=float)  # use numpy to load the csv and seperate the data layers from inputs to outputs
    # split into input (X) and output (Y) variables
    X = dataset[:, 0:510]

    predictions = model.predict(X)  # predict the results based on the new data of kickstarter campaigns
    predicted_data = [round(x[0]) for x in predictions]  # the data to a list and round

    with open("../testing/Test 2017-06-16/machine_testing_data_2017_06_16.csv", "r") as results_data, open("../testing/Test 2017-06-16/actual_data_2017_06_16.csv", "w+") as actual_data_file:
        reader = csv.reader(results_data)  # create the reader object
        for x in reader:
            actual_data.append(float(x[510]))  # append the data

    print((len([i for i, j in zip(predicted_data, actual_data) if i == j]) / len(predicted_data)))


test_data()
