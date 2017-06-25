from keras.models import load_model
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

np.random.seed(7)  # to ensure a stochastic process

predicted_data = []


def plot_model_histogram():
    model = load_model("../model_weights/start_think_weights_25000_100.h5")  # load the model
    # loading dataset
    dataset = np.loadtxt("../testing/Test 2017-06-16/machine_testing_data_2017_06_16.csv", delimiter=",",
                         dtype=float)
    X = dataset[:, 0:510]

    predictions = model.predict(X)  # predict the results based on the new data of kickstarter campaigns
    predicted_data = [x[0] for x in predictions]  # add the data to a list
    print(predicted_data, len(predicted_data))
    n, bins, patches = plt.hist(predicted_data, 500, normed=1, facecolor='green', alpha=1)

    mu, sigma = 0.5, 0.1
    y = mlab.normpdf(bins, mu, sigma)
    l = plt.plot(bins, y, 'w--', linewidth=2)

    plt.xlabel('Neural Network Output Score')
    plt.ylabel('Number of Occurrences')
    plt.title('Accuracy of Machine Learning Predictions for Kickstarter Campaigns')
    plt.axis([0.0, 1.0, 0, 500])
    plt.grid(True)

    plt.show()


plot_model_histogram()
