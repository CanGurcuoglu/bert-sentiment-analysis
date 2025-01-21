import pandas as pd
def clean(x):
    df = pd.read_csv(x+".csv")
    df["length"] = df["yorum"].apply(lambda x: len (x))
    aa = df[ df["length"] > 35]
    aa.drop_duplicates().iloc[:,:2].to_csv(x+".csv",index=False)
