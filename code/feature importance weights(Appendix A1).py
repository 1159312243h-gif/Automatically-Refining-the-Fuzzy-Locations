import pandas as pd
import numpy as np
import math
from numpy import array

# Read data
df = pd.read_csv('result.csv')

# Data preprocessing, remove records with null values
df.dropna()

def cal_weight(x):
    # Standardization
    x = x.apply(lambda x: ((x - np.min(x)) / (np.max(x) - np.min(x))))
    
    # Calculate the constant k for entropy
    rows = x.index.size  # Rows
    cols = x.columns.size  # Columns
    k = 1.0 / math.log(rows)

    lnf = [[None] * cols for i in range(rows)]
    
    # Matrix calculation
    # Information entropy
    x = array(x)
    lnf = [[None] * cols for i in range(rows)]
    lnf = array(lnf)
    for i in range(0, rows):
        for j in range(0, cols):
            if x[i][j] == 0:
                lnfij = 0.0
            else:
                p = x[i][j] / x.sum(axis=0)[j]
                lnfij = math.log(p) * p * (-k)
            lnf[i][j] = lnfij
            
    lnf = pd.DataFrame(lnf)
    E = lnf
    
    # Calculate redundancy
    d = 1 - E.sum(axis=0)
    
    # Calculate the weight of each indicator
    w = [[None] * 1 for i in range(cols)]
    for j in range(0, cols):
        wj = d[j] / sum(d)
        w[j] = wj

    w = pd.DataFrame(w)
    return w

weights = []

if __name__ == '__main__':
    # Calculate the weight of each field in df
    w = cal_weight(df)  # Call cal_weight function
    weights1 = np.array(w)
    weights = weights1.tolist()
    w.index = df.columns
    w.columns = ['weight']
    print(w)

# mode='a': append data to the csv file, row by row
# header=True: write the column names (header) of the dataframe
# index=None: do not add index column
w.to_csv('grades.csv', mode='w', header=True, index=None)