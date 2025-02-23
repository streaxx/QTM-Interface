import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import numpy as np
import sqlite3

# TODO Write comments for functions

def get_simulation_data(db, dataset_name):
    # Connect to the SQLite database
    conn = sqlite3.connect(db)
    # Read the data from the SQLite table into a DataFrame
    df = pd.read_sql(f'SELECT * FROM {dataset_name}', conn)

    # Close the connection
    conn.close()
    return df

def plot_results(x, y_columns, run):

    df = get_simulation_data('interfaceData.db', 'simulation_data')

    # example for Monte Carlo plots
    #monte_carlo_plot_st(df,'timestep','timestep','seed_a_tokens_vested_cum',3)

    # example for line plots of different outputs in one figure
    line_plot_st(df,x, y_columns, run)

def plot_stacked_area_graph(df):
    # pivot the dataframe to create a multi-level index with Investor_Name and timestep

    df_pivot = df.pivot(index='timestep', columns='Investor_Name', values='current_allocation')
    
    # create a list of x values (time steps)
    x = df_pivot.index
    
    # create a list of y values (token allocations for each investor)
    y = df_pivot.to_numpy().T
    
    # plot the stacked area graph using stackplot
    plt.stackplot(x, y, labels=df_pivot.columns)
    
    # set the title and labels for the plot
    plt.title('Investor Allocation Over Time')
    plt.xlabel('Time Step')
    plt.ylabel('Token Allocation')
    
    # format the y-axis labels as integers
    plt.gca().yaxis.set_major_formatter('{:.0f}'.format)
    
    # show the legend and plot
    plt.legend()
    plt.show()


def effective_token_price_plot(df):
    data = []
    for investor, values in df['investors'][0].items():
        name = investor
        price = values['effective_token_price']
        data.append((name, price))
    data = pd.DataFrame(data, columns=['Name', 'effective_token_price'])

    df_filtered = data[data['effective_token_price'] != 0]
    df_filtered = df_filtered.sort_values(by='effective_token_price', ascending=False)
    df_filtered[['effective_token_price']].plot(kind='bar', rot=0)
    plt.title('Effective Token Price by Investor Type')
    plt.xlabel('Investor Type')
    plt.ylabel('Effective Token Price')
    plt.show()

# 
def extract_allocation(df):
    investors_df = pd.DataFrame(columns=['Investor_Name', 'current_allocation', 'timestep'])
    for index, row in df.iterrows():
        timestep = row['timestep']
        investors_dict = row['investors']
        for investor_name, investor_data in investors_dict.items():
            allocation = investor_data['current_allocation']
            investors_df = pd.concat([investors_df,
                                      pd.DataFrame({'Investor_Name': [investor_name],
                                                    'current_allocation': [allocation],
                                                    'timestep': [timestep]})])
    investors_df.reset_index(drop=True, inplace=True)
    investors_df['current_allocation'] = investors_df['current_allocation'].astype(float)
    investors_df['timestep'] = investors_df['timestep'].astype(int)

    return investors_df

#
def initial_allocation_pie(df):
    sum = 0
    percentages = []
    labels = []
    for i, investor in df['investors'][0].items():
        percentage = investor['percentage_allocation']
        labels.append(i+": "+str((round(percentage*100, 2)))+"%")
        percentages.append(percentage)
        sum += percentage

    labels.append("Blank")
    percentages.append(1-sum)

    plt.pie(percentages, labels=labels, normalize=True)
    plt.show()

# 
def aggregate_runs(df,aggregate_dimension,x,y):
    '''
    Function to aggregate the monte carlo runs along a single dimension.

    Parameters:
    df: dataframe name
    aggregate_dimension: the dimension you would like to aggregate on, the standard one is timestep.

    Example run:
    mean_df,median_df,std_df,min_df = aggregate_runs(df,'timestep')
    '''
    df = df[[x,y]].copy()
    mean_df = df.astype(float).groupby(aggregate_dimension).mean().reset_index()
    median_df = df.astype(float).groupby(aggregate_dimension).median().reset_index()
    std_df = df.astype(float).groupby(aggregate_dimension).std().reset_index()
    min_df = df.astype(float).groupby(aggregate_dimension).min().reset_index()

    return mean_df,median_df,std_df,min_df

# 
def monte_carlo_plot(df,aggregate_dimension,x,y,runs):
    '''
    A function that generates timeseries plot of Monte Carlo runs.

    Parameters:
    df: dataframe name
    aggregate_dimension: the dimension you would like to aggregate on, the standard one is timestep.
    x = x axis variable for plotting
    y = y axis variable for plotting
    run_count = the number of monte carlo simulations

    Example run:
    monte_carlo_plot(df,'timestep','timestep','revenue',run_count=100)
    '''
    mean_df,median_df,std_df,min_df = aggregate_runs(df,aggregate_dimension,x,y)

    plt.figure(figsize=(10,6))
    for r in range(1,runs+1):
        legend_name = 'Run ' + str(r)
        plt.plot(df[df.run==r].timestep, df[df.run==r][y], label = legend_name )
    
    plt.plot(mean_df[x], mean_df[y], label = 'Mean', color = 'black')
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.xlabel(x)
    plt.ylabel(y)
    title_text = 'Performance of ' + y + ' over ' + str(runs) + ' Monte Carlo Runs'
    plt.title(title_text)

def monte_carlo_plot_st(df,aggregate_dimension,x,y,runs):
    '''
    A function that generates timeseries plot of Monte Carlo runs.

    Parameters:
    df: dataframe name
    aggregate_dimension: the dimension you would like to aggregate on, the standard one is timestep.
    x = x axis variable for plotting
    y = y axis variable for plotting
    run_count = the number of monte carlo simulations

    Example run:
    monte_carlo_plot(df,'timestep','timestep','revenue',run_count=100)
    '''
    fig = plt.figure(figsize=(10,6))
    if runs > 1:
        for r in range(1,runs+1):
            legend_name = 'Run ' + str(r)
            plt.plot(np.asarray(df[df['run'].astype(int)==r].timestep, float), np.asarray(df[df['run'].astype(int)==r][y], float), label = legend_name )
        mean_df,median_df,std_df,min_df = aggregate_runs(df,aggregate_dimension,x,y)
        plt.plot(np.asarray(mean_df[x], float), np.asarray(mean_df[y], float), label = 'Mean', color = 'black')
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    
    else:
        plt.plot(np.asarray(df[df['run'].astype(int)==1].timestep, float), np.asarray(df[df['run'].astype(int)==1][y], float))
    plt.xlabel(x)
    plt.ylabel(y)
    title_text = 'Performance of ' + y + ' over ' + str(runs) + ' Monte Carlo Runs'
    plt.title(title_text)

    st.pyplot(fig)

def line_plot_st(df,x,y_series,run):
    '''
    A function that generates a line plot from a series of data series in a frame in streamlit
    '''
    fig = plt.figure(figsize=(10,6))
    plt.plot(np.asarray(df[df['run'].astype(int)==run][x], float), np.asarray(df[df['run'].astype(int)==run][y_series], float), label = y_series)
    plt.xlabel(x)
    #plt.ylabel(y_series)
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

    st.pyplot(fig)

def plot_line_chart(dataframe, x_column, y_columns, title=''):
    """
    Plots a simple line chart using the specified columns from a dataframe.

    Args:
        dataframe (pd.DataFrame): The input dataframe.
        x_column (str): The column name for the x-axis values.
        y_columns (list): The list of column names for the y-axis values.
        title (str, optional): The title for the chart (default is empty string).
    """
    x_values = dataframe[x_column]
    
    for column in y_columns:
        y_values = dataframe[column]
        plt.plot(x_values, y_values, label=column)
    
    plt.xlabel(x_column)
    plt.ylabel('Y-axis')
    plt.title(title)
    plt.grid(True)
    plt.legend()
    plt.show()
