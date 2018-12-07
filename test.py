import pandas as pd
import models as m

#def doit():
#    df = pd.read_csv("k.csv", index_col=False)
#    df['Time'] = df['Time'].apply(lambda x: (1 if (float(x) > 1.75e-06) else 0))
#    df.to_csv("test.csv", index=False)

if __name__ == "__main__":
    df = pd.read_csv("test.csv", index_col=False)

    print("bpnn accuracy:", end=" ")
    m.bpnn(df.drop('Time', axis = 1), df['Time'], epochs = 100)

    print("random forest accuracy:", end=" ")
    m.randForest(df.drop('Time', axis = 1), df['Time'])
