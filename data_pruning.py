from functools import reduce
import pandas as pd


def csv_to_dataframes(files):
    dataframes = []
    for f in files:
        df = pd.read_csv(f, sep=',')
        dataframes.append(df)
    return dataframes


def outer_join_df(dataframes):
    return reduce(
        lambda left, right: pd.merge(left, right, on='Compound ID', how='outer'),
        dataframes)


def left_join_df(df1, df2):
    return df1.merge(df2, on=['Compound ID'], how='left')[df2.columns]

dfs = csv_to_dataframes(['compound_ic50.csv', 'compound_labels.csv'])
ic50_label_df = outer_join_df(dfs)
# removes white space from the column titles
ic50_label_df.rename(columns=lambda x: x.strip(), inplace=True)
# replace spaces in assay result label with underscores
ic50_label_df['Assay Result Label'] = ic50_label_df['Assay Result Label'].str.lower().replace(' ', '_', regex=True)
# remove rows where the assay result is inactive or invalid
ic50_label_df.drop(ic50_label_df.index[(ic50_label_df['Assay Result Label'] == 'inactive') | (
ic50_label_df['Assay Result Label'] == 'invalid_concentration_range')], inplace=True)
# creates new csv showing ic50 and label together
ic50_label_df.to_csv("ic50_and_label.csv", index=False)
dfs2 = csv_to_dataframes(['assay_results.csv'])
# filters out assay results if the label is invalid
assay_filtered = left_join_df(ic50_label_df, dfs2[0])
# creates new csv
assay_filtered.to_csv("assay_filtered.csv", index=False)