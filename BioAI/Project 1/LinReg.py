import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import PolynomialFeatures
from math import sqrt
import random

class LinReg():
    def __init__(self):
        pass

    def train(self, data, y):
        model  = LinearRegression().fit(data, y)
        return model

    def get_fitness(self, x, y, random_state=42):
        if random_state==0:
            x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.2)
        else:
            x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.2, random_state=random_state)
        model = self.train(x_train, y_train)
        predictions = model.predict(x_test)
        error = sqrt(mean_squared_error(predictions, y_test))

        return  error

    def get_columns(self,x,bitstring):
        # Function to filter data based on a bitstring
        indexes = []
        for i, s in enumerate(bitstring):
            if s=='0':
                indexes.append(i)
        arr = np.asarray(x)
        arr = np.delete(arr, indexes, axis=1)
        return arr

