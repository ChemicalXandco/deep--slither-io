import numpy as np
import pandas as pd

dummy = np.array(pd.get_dummies([0., 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.]))

def getdummy(value):
    if value == 0.:
        return dummy[0]
    elif value == 0.1:
        return dummy[1]
    elif value == 0.2:
        return dummy[2]
    elif value == 0.3:
        return dummy[3]
    elif value == 0.4:
        return dummy[4]
    elif value == 0.5:
        return dummy[5]
    elif value == 0.6:
        return dummy[6]
    elif value == 0.7:
        return dummy[7]
    elif value == 0.8:
        return dummy[8]
    elif value == 0.9:
        return dummy[9]
    elif value == 1.:
        return dummy[10]

def getmaxpos(matrix):
    maxof = np.amax(matrix)
    count = 0
    for i in matrix.flatten():
        if i == maxof:
            break
        else:
            count +=1
    return count
