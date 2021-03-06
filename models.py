import numpy as np
import pandas as pd
from sklearn.neural_network import MLPClassifier as mlp
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier as rf

def bpnn(X, Y, epochs = 20):
    model = mlp(max_iter=epochs, verbose=True)
    X_tr, X_te, Y_tr, Y_te = train_test_split(X, Y)
    model.fit(X_tr, Y_tr)
    print(model.score(X_te, Y_te))

def randForest(X, Y, n = 20, c = "entropy"):
    model = rf(verbose=1, criterion = c, n_estimators = n)
    X_tr, X_te, Y_tr, Y_te = train_test_split(X, Y)
    model.fit(X_tr, Y_tr)
    print(model.score(X_te, Y_te))
