from pprint import pprint
import pandas as pd
import json
from pprint import pprint

pd.set_option('display.min_rows', 999)
pd.set_option('display.max_columns', 999)


def retrieveInitialTier(author):
    X_CONFERENCES = 5 ##Denotes taking first/last X number of conferences to evaluate initial/final reputation of author
    FIRST_SLICE_INT = X_CONFERENCES
    LAST_SLICE_INT = X_CONFERENCES * -1 - 1

    if(author[1]["size"] < X_CONFERENCES*1):
        return

    ##Retrieve first / last X publications
    first = author[1]['publ'][0:FIRST_SLICE_INT:1]
    last = author[1]['publ'][-1:LAST_SLICE_INT:-1]

    initialTiers = sum(pub['tier'] for pub in first)
    finalTiers = sum(pub['tier'] for pub in last)

    data = {'Name' : author[0],
            ('initialRep' + "_" + str(X_CONFERENCES))  : X_CONFERENCES * 3 - initialTiers,
            ('FinalRep' + "_" + str(X_CONFERENCES)) : X_CONFERENCES * 3 - finalTiers,
            'Success' : author[1]['success'],
            'NumberOfPublications' : author[1]["size"],
            'Tier 1 Count' : author[1]["tier1cnt"],
            'Reputation' : author[1]["reputation"]
            }
    
    return data

## Development function, can ignore during production
def findAuthor(name, authorSet):
    for x in range(len(authorSet)):
        if authorSet[x][0] == name:
            found = x

    return authorSet[found]

def Q6():
    with open('json/authorNodes.json') as f:
        authorSet = json.load(f)

    qn6Parameters = []
    for author in authorSet:
        temp = retrieveInitialTier(author)
        if (temp):
            qn6Parameters.append(temp)
        
    df_Q6 = pd.DataFrame(qn6Parameters)

    df_Q6 = df_Q6[["Name", "initialRep_5", "Success", "NumberOfPublications", "Tier 1 Count"]]
    return df_Q6.sort_values("Success", ascending = False).head(10)

if __name__ == "__main__":
    df_Q6 = Q6()
    print("you can use the variable, df_Q6, to look at the dataframe")
    print(df_Q6.head(10))
