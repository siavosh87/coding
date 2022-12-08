# Importing libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def load_data(filename):
    df = pd.read_csv(filename)
    return df


# The following generates an error, hence why commented out
# df['Date'] = pd.to_datetime(df['Date'], format="%d/%m/%Y")
# This is because we need to fix up the dates

def examine_dtype(df):
    print(df.dtypes)


def examine_incorrect_dates(df):
    date_list = df['Date'].to_list()
    # A yyyy-mm-dd format will have length 10
    incorrect_dates = [x for x in date_list if len(x) < 10]
    print(f"Top of the list: {incorrect_dates[0:5]}")
    print('\n')
    print(f"Bottom of list: {incorrect_dates[::-1][0:5]}")


def generate_correct_dates(year):
    start_date = year + "-01-01"
    end_date = year + "-12-31"
    corrected_dates = pd.date_range(start_date, end_date, freq='d')
    return corrected_dates


def dataframe_invalid_dates(df):
    df_incorrect_dates = df.loc[df['Date'].str.len() != 10]
    return df_incorrect_dates


def dataframe_valid_dates(df):
    df_valid_dates = df.loc[df['Date'].str.len() == 10]
    df_valid_dates.loc[:, 'Date'] = pd.to_datetime(df_valid_dates['Date'], format="%d/%m/%Y")
    return df_valid_dates


def fix_bad_dates(df):
    df_invalid_dates = dataframe_invalid_dates(df)
    df_valid_dates = dataframe_valid_dates(df)
    correct_dates = generate_correct_dates('2020')
    df_invalid_dates.loc[:, 'Date'] = correct_dates
    df_merged = pd.concat([df_invalid_dates, df_valid_dates])
    df_merged.sort_values(by='Date', ascending=True, inplace=True)
    return df_merged


def add_year_month_day(df):
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Day'] = df['Date'].dt.day
    return df


def add_season_column(df):
    df['Season'] = np.nan
    df_size = df.shape[0]
    for i in range(df_size):
        if (df.loc[i, 'Month'] == 3) or (df.loc[i, 'Month'] == 4) or (df.loc[i, 'Month'] == 5):
            df.loc[i, 'Season'] = 'Spring'
        if (df.loc[i, 'Month'] == 6) or (df.loc[i, 'Month'] == 7) or (df.loc[i, 'Month'] == 8):
            df.loc[i, 'Season'] = 'Summer'
        if (df.loc[i, 'Month'] == 9) or (df.loc[i, 'Month'] == 10) or (df.loc[i, 'Month'] == 11):
            df.loc[i, 'Season'] = 'Autumn'
        if (df.loc[i, 'Month'] == 12) or (df.loc[i, 'Month'] == 1) or (df.loc[i, 'Month'] == 2):
            df.loc[i, 'Season'] = 'Winter'
    df['Season'] = df['Season'].astype('category')


def set_index(df, columns):
    df2 = df.set_index(columns)
    return df2


def choose_dataframe_range(df, start_year, end_year):
    df1 = df[(df['Year'] >= start_year) & (df['Year'] <= end_year)]
    return df1


def aggregate_data(df, columns_to_group, column_to_compute, computation):
    df_grouped = df.groupby(columns_to_group, as_index=True).agg({column_to_compute: computation})
    return df_grouped


def resample_data(df, frequency, column_to_group, column_to_compute, computation):
    df = df[[column_to_group, column_to_compute]]
    if computation == 'sum':
        df2 = df.resample(frequency, on=column_to_group).sum()
    if computation == 'mean':
        df2 = df.resample(frequency, on=column_to_group).mean()
    return df2


def plot_resampled_data(df, y_value, titles, dashes=False):
    fig, ax = plt.subplots(figsize=[12,5])
    if dashes == False:
        sns.lineplot(x=df.index, y=y_value, data=df, ax=ax).set(title=titles)
    else:
        sns.lineplot(x=df.index, y=y_value, data=df, linestyle='--', ax=ax).set(title=titles)
    plt.show()


def main():
    # loading data and fixing up the dates
    df = load_data('Consumption.csv')
    df = fix_bad_dates(df)
    add_year_month_day(df)
    add_season_column(df)
    df2 = set_index(df, 'Date')

    # plotting 5 year range
    df_asked_range = choose_dataframe_range(df, 2016, 2020)
    df_resampled = resample_data(df_asked_range, 'M', 'Date', 'Consumption', 'sum')
    title1 = 'Consumption vs Date for 2016 to 2021'
    plot_resampled_data(df_resampled, 'Consumption', title1, dashes=False)

    # plotting average line
    df_average = resample_data(df_asked_range, 'Y', 'Date', 'Consumption', 'mean')
    title2 = 'Consumption vs Date average for 2016-2020'
    plot_resampled_data(df_average, 'Consumption', title2, dashes=True)

    # plotting 2021 line
    df_2021 = choose_dataframe_range(df, 2021, 2021)
    df_2021 = resample_data(df_2021, 'M', 'Date', 'Consumption', 'sum')
    title3: str = 'Consumption vs Date for 2021'
    plot_resampled_data(df_2021, 'Consumption', title3, dashes=False)

    # plotting 2022 line
    df_2022 = choose_dataframe_range(df, 2022, 2022)
    df_2022 = resample_data(df_2022, 'M', 'Date', 'Consumption', 'sum')
    title3: str = 'Consumption vs Date for 2022'
    plot_resampled_data(df_2022, 'Consumption', title3, dashes=False)


if __name__ == '__main__':
    main()


