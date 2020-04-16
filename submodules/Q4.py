import pandas as pd

def Q4():    
    pd.set_option('display.min_rows', 999)
    pd.set_option('display.max_rows', 999)

    df = pd.read_csv("csv/FinalAuthorData.csv")

    df_count = df.groupby("Country").count()[["Name"]]
    df_count = df_count.rename(columns = {"Name" : "NumberOfAuthors"})

    temp = df.groupby("Country").mean()[["Success"]]
    temp = temp.rename(columns = {"Success" : "AvgSuccess"})

    temp2 = df.groupby("Country").sum()[["Success"]]
    temp2 = temp2.rename(columns = {"Success" : "TotalSuccess"})

    df_agg = pd.merge(temp, df_count, on = "Country")
    df_agg = pd.merge(df_agg, temp2, on = "Country")
    df_agg = df_agg.sort_values("AvgSuccess").reset_index().round(3)

    return df_agg.sort_values("AvgSuccess", ascending = False).head(10)


if __name__ == "__main__":
    df_agg = Q4()
    print("You can use the variable, df_agg, to see the dataframe")
    print(df_agg)

