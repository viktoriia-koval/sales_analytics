import pandas as pd

def bubble_sort_values(df: pd.DataFrame, by: str):
    """Sort DataFrame with bubble sort by one column."""
    if by not in df.columns:
        raise KeyError(by)

    work = df.copy()
    n = len(work)

    for i in range(n):
        for j in range(0, n - i - 1):
            if work[by].iat[j] > work[by].iat[j + 1]:
                left_row = work.iloc[j].copy()
                work.iloc[j] = work.iloc[j + 1]
                work.iloc[j + 1] = left_row

    return work
