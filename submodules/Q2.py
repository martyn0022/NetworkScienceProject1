import pandas as pd

pd.set_option('display.min_rows', 999)
pd.set_option('display.max_rows', 999)


def Q2_1():
    
    df = pd.read_csv("FinalAuthorData.csv")
    df["InstitutionTier"] = pd.np.nan

    tier_1_10 = df[(df["Institution Rank"] > 0) & (df["Institution Rank"] < 11)].index
    df.loc[tier_1_10, "InstitutionTier"] = 1

    tier_95_105 = df[(df["Institution Rank"] > 94) & (df["Institution Rank"] < 106)].index
    df.loc[tier_95_105, "InstitutionTier"] = 100

    tier_195_205 = df[(df["Institution Rank"] > 194) & (df["Institution Rank"] < 206)].index
    df.loc[tier_195_205, "InstitutionTier"] = 200

    tier_290_305 = df[(df["Institution Rank"] > 290) & (df["Institution Rank"] < 305)].index
    df.loc[tier_290_305, "InstitutionTier"] = 300

    tier_395_405 = df[(df["Institution Rank"] > 394) & (df["Institution Rank"] < 405)].index
    df.loc[tier_395_405, "InstitutionTier"] = 400

    tier_495_505 = df[(df["Institution Rank"] > 494) & (df["Institution Rank"] < 506)].index
    df.loc[tier_495_505, "InstitutionTier"] = 500



    return df.groupby("InstitutionTier").mean()[["Tier 1 Count"]]

def Q2_2():
    pass

if __name__ == "__main__":
    Q4_1_df = Q4_1()
    






