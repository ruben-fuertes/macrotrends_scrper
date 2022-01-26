import pandas as pd
import numpy as np

def reconstruct_table(gricells_dict, headers_dict):
    """Takes two dictionaries containing the data and the headers and
    reconstruct the table."""
    # Compute number of col and row
    col_n = len(headers_dict)
    row_n = int(len(gricells_dict) / col_n)

    # Create empty list of lists to store the data
    list_df = [[None]*col_n for _ in range(row_n)]

    # Loop the list and find the index value in the dict
    for col in range(col_n):
        for row in range(row_n):
            index = (row_n-(row+1))*col_n + (col_n-col)
            list_df[row][col] = gricells_dict[index]

    header_list = []
    # Extract the headers in order
    for _, v in sorted(headers_dict.items(), reverse=True):
        header_list.append(v)
    
    return pd.DataFrame(list_df, columns=header_list)


def clean_table(df):
    """Take the table and clean it."""
    # First col to index
    df.index = df.iloc[:,0]
    df = df.drop(df.columns[0], axis=1)
    
    # Remove empty cols
    df = df.replace(r'^\s*-*$', np.nan, regex=True)
    df = df.dropna(how='all', axis=1)
    
    # Remove the dollar symbol
    df = df.replace({'\$':'', ',':''}, regex = True)
    
    # Transform to number
    df.apply(pd.to_numeric)

    return df

# df = list(t.values())[0]
# x = clean_table(df)
