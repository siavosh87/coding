# Importing libraries
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go


def load_data(file):
    df = pd.read_csv(file)
    return df


def format_dates(df):
    df['TradeDateTime'] = pd.to_datetime(df['TradeDateTime'], format='%d/%m/%Y %H:%M')
    return df


# We combine the products like the question asked us to
def combine_products(df):
    df.loc[df['Product'] == 'Emission - Venue A', 'Product'] = 'Emission'
    df.loc[df['Product'] == 'Emission - Venue B', 'Product'] = 'Emission'
    return df


def add_year_month_day(df, column):
    df['Year'] = df[column].dt.year
    df['Month'] = df[column].dt.month
    df['Day'] = df[column].dt.day
    df['Hour'] = df[column].dt.hour
    df['Minute'] = df[column].dt.minute
    return df


def check_product_with_multiple_contracts(df):
    """
    We will go through the unique products, and see if there are
    more than one contract associated with that product. If there is,
    then we will just rename the product to 'product + contract'
    """
    products = df['Product'].unique()
    for product in products.tolist():
        contracts = df.loc[df['Product'] == product, 'Contract'].unique()
        if len(contracts) == 1:
            break
        if len(contracts) > 1:
            print(f"There are {len(contracts)} products for your option\n")
            print("The available options are: \n")
            for contract in contracts.tolist():
                new_product_name = str(product) + " - " + str(contract)
                print(f"{new_product_name} \n")
                df.loc[(df['Product'] == product) & (df['Contract'] == contract), 'Product'] = new_product_name
    return df


def get_dataframe_by_product(df, products):
    """
    Filters the dataframe to only those rows with the specified product.
    product variable can be a string, or a list of strings (if there is more than
    one product)
    """
    if type(products) == str:
        df2 = df[df["Product"] == products]
    if type(products) == list and len(products) > 1:
        df2 = df[df["Product"].isin(products)]
    df3 = df2.sort_values(by='TradeDateTime')
    return df3


def choose_dataframe_range(df, start, end):
    """
    start and end are arguments chosen by user
    """
    start = pd.to_datetime(start)
    end = pd.to_datetime(end)
    df1 = df.loc[(df['TradeDateTime'] >= start) & (df['TradeDateTime'] < end), :]
    return df1


def show_null_values(data):
    """
    Useful for checking to see if there are any NaN or Null values
    at the end
    """
    null_counts = data.isnull().sum()
    null_counts_percentage = null_counts / data.shape[0] * 100
    null_data = pd.DataFrame({'null_counts': null_counts, 'null_percentage': null_counts_percentage})
    null_data = null_data.T.astype(int)
    return null_data


def resample_with_chosen_frequency(df, frequency):
    df2 = df.resample(frequency, base=1, on="TradeDateTime").agg(
        {
            "Price": ['first', 'max', 'min', 'last'],  # aka OHLC
            "Quantity": ['sum']
        })
    return df2


def filter_working_hours(df, start_hour, end_hour):
    """
    After resampling has been done, we will need to refilter
    the data to keep it within the working hours. The 'TradeDateTime'
    column will now automatically be the index after resampling.
    """
    df.index = pd.to_datetime(df.index)
    df["Temp"] = df.index.hour
    df["Temp"] = df["Temp"].astype(int)
    df1 = df.loc[(df["Temp"] >= start_hour) & (df["Temp"] < end_hour), :]
    df1.drop(columns="Temp", inplace=True)
    return df1


def rename_cols_after_resampling(df):
    df.columns = df.columns.values
    renaming = {
        ('Price', 'first'): ('Price', 'Open'),
        ('Price', 'max'): ('Price', 'High'),
        ('Price', 'min'): ('Price', 'Low'),
        ('Price', 'last'): ('Price', 'Close'),
        ('Quantity', 'sum'): ('Quantity', 'Total Volume')}
    df.columns = pd.MultiIndex.from_tuples(df.rename(columns=renaming))
    return df


def generate_dataframe(start, end, products, frequency):
    start_date = start
    end_date = end
    resample_freq = frequency
    START_HOUR = 7
    END_HOUR = 17
    filename = 'Trades.csv'

    # Loading data from csv into dataframe
    df = load_data(filename)

    # Fixing the dates
    df = format_dates(df)

    # Combine products like the question asks us to
    df = combine_products(df)

    # Filter dataframe for products specified in argument
    df = get_dataframe_by_product(df, products)

    # Check to see if a product is associated
    # with multiple contracts
    df = check_product_with_multiple_contracts(df)

    print(type(df["TradeDateTime"]))
    # restrict data to between start and end
    df2 = choose_dataframe_range(df, start_date, end_date)

    # Applying resampling
    df_resample = resample_with_chosen_frequency(df2, resample_freq)

    # Restricting to within working hours
    df_resample = filter_working_hours(df_resample, START_HOUR, END_HOUR)

    # Renaming columns
    df_final = rename_cols_after_resampling(df_resample)

    return df_final


def create_ohlc_plot(df):
    fig = go.Figure(data=[
        go.Candlestick(x=df.index, open=df['Price']['Open'], high=df['Price']['High'], low=df['Price']['Low'],
                       close=df['Price']['Close'])])
    fig.show()


def main():
    final = generate_dataframe('2022-04-18', '2022-04-21', 'Emission', '20min')
    create_ohlc_plot(final2)


if __name__ == '__main__':
    main()
