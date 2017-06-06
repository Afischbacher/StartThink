from keras.models import load_model
import numpy as np
import csv

np.random.seed(7) # to ensure a stochastic process

actual_data = []
predicted_data = []
def test_data():

    model = load_model("../model_weights/start_think_weights_20000_100.h5") # load the model

    # loading dataset
    dataset = np.loadtxt("../testing/machine_testing_data.csv", delimiter=",", dtype=float) # use numpy to load the csv and seperate the data layers from inputs to outputs
    # split into input (X) and output (Y) variables
    X = dataset[:, 0:510]

    predictions = model.predict(X) # predict the results based on the new data of 3200 kickstarter campaigns
    predicted_data = [round(x[0]) for x in predictions] #store the data to a list
    with open("predicted_data.csv", "w+") as file:
        writer = csv.writer(file) # create the writer object
        writer.writerow([[predicted_data]]) #write results to a file


    with open("machine_testing_data.csv", "r") as results_data, open("actual_data.csv", "w+") as actual_data_file:
        reader = csv.reader(results_data) #create the reader object
        writer = csv.writer(actual_data_file) #create the writer object
        for x in reader:
            actual_data.append(float(x[510])) #append the data
            writer.writerow([x[510]]) #

    print((len([i for i, j in zip(predicted_data,actual_data) if i == j]) / len(predicted_data)))

test_data()
