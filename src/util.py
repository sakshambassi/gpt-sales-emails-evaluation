import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def plot_counts(all_df, input_df, title=None, column_name='product_name',
                count_threshold=10, percent_threshold=0.2, plot=True):
    """
    Bar plotting of the unique counts based on column_name

    Args:
        all_df (pd.DataFrame): Entire dataset df - used to get total_val_counts
        input_df (pd.DataFrame): Filted dataset df
        title (str, optional): Title of plot. Defaults to None.
        column_name (str, optional): Based on the column, we count unique. Defaults to 'product_name'.
        count_threshold (int, optional): Minimum theshold of the column to be considered. Defaults to 10.
        percent_threshold (float, optional): Minimum threshold percentage to consider in plot. Defaults to 0.2.
        plot (bool, optional): Whether to plot or not. Defaults to True.

    Returns:
        pd.DataFrame: Returns the final df to do more combined graph type analysis
    """
    # Take total entries for each type in column, used to find the percentage
    total_val_counts = all_df[column_name].value_counts()
    # Do count of entries based on column_name
    df = input_df[[column_name]].apply(pd.value_counts).reset_index().rename(
        columns={column_name: 'count', 'index': column_name})
    # Make the column int type
    df['count'] = pd.to_numeric(df["count"])

    # Only consider those entries that are above this count_threshold
    df = df[df['count'] > count_threshold]
    # take the percentage
    for index, row in df.iterrows():
        df.at[index, 'count'] = row['count'] / \
            total_val_counts[row[column_name]]

    # Only consider those entries that are above this threshold
    df = df[df['count'] > percent_threshold]

    # Whether to plot or not
    if plot:
        sns.color_palette("Set2")
        sns.barplot(data=df, x=column_name, y="count")
        plt.xticks(rotation=75)
        plt.xlabel(f'product names with more than {count_threshold} entries')
        plt.ylabel('percentage of occurrence')
        plt.title(title)
        plt.show()
    return df


def plot_combined_counts(accepted_df, rejected_df, column_name):
    """
    Plot Bar plot of combined accepted and rejected outputs

    Args:
        accepted_df (pd.DataFrame): only df of accepted
        rejected_df (pd.DataFrame): only df of rejected
        column_name (str): counted column name
    """
    # Create additional column to new df for sns.hue
    accepted_df['accepted'] = True
    rejected_df['accepted'] = False

    # Concat these 2 new value count dfs
    merged_value_count_df = pd.concat([accepted_df, rejected_df])

    # Rotate x axis ticks
    plt.xticks(rotation=75)

    # Bar plot
    sns.barplot(data=merged_value_count_df,
                x=column_name, y="count", hue='accepted')
    plt.title(f'Accepted or rejected based on {column_name}')
    plt.show()
