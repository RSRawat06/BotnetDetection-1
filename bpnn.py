import numpy as np
import pandas as pd
from sklearn.neural_network import MLPClassifier as mlp
from sklearn.model_selection import train_test_split

def bpnn(data, file = False, epochs = 20):
    model = mlp(max_iter=epochs)
    if file != False:
        data = pandas.read_csv(file)
    #do one-hot encoding
    X_tr, X_te, Y_tr, Y_te = train_test_split(data)

    model.fit(X_tr, Y_tr)
    #model.
