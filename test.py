import pandas as pd
import models as m

#def doit():
#    df = pd.read_csv("k.csv", index_col=False)
#    df['Security'] = df['Security'].apply(lambda x: (1 if (float(x) > 1.75e-06) else 0))
#    df.to_csv("test.csv", index=False)

def cleanCSV(fname):
    df = pd.read_csv(fname, index_col= False)
    df['Security'] = df['Security'].apply(lambda x: (1 if str(x) == 'B' else 0))
    df.to_csv("updated.csv", index=False)

if __name__ == "__main__":
    cleanCSV("out.csv")
    df = pd.read_csv("updated.csv", index_col=False)
    print("bpnn accuracy:", end=" ")
    m.bpnn(df.drop('Security', axis = 1), df['Security'], epochs = 100)

    print("random forest accuracy:", end=" ")
    m.randForest(df.drop('Security', axis = 1), df['Security'])
