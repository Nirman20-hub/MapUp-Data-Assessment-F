import pandas as pd
#question 1
def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Create a pivot table to represent the distance matrix
    distance_matrix = df.pivot(index='id_start', columns='id_end', values='distance').fillna(0)

    # Add the transpose of the matrix to make it symmetric
    distance_matrix += distance_matrix.T

    # Calculate cumulative distances along known routes
    distance_matrix = distance_matrix.cumsum(axis=1)

    # Set diagonal values to 0
    distance_matrix.values[[range(len(distance_matrix))]*2] = 0

    return distance_matrix


#question 2#
def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Reset index to include 'id_start' as a column
    distance_matrix_reset = distance_matrix.reset_index()

    # Melt the DataFrame to unroll the distance matrix
    unrolled_df = pd.melt(distance_matrix_reset, id_vars='id_start', var_name='id_end', value_name='distance')

    # Filter out rows where 'id_start' is equal to 'id_end'
    unrolled_df = unrolled_df[unrolled_df['id_start'] != unrolled_df['id_end']]

    # Sort the DataFrame by 'id_start' and 'id_end'
    unrolled_df.sort_values(by=['id_start', 'id_end'], inplace=True)

    # Reset index for a clean DataFrame
    unrolled_df.reset_index(drop=True, inplace=True)

    return unrolled_df

    #question 3
    def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    # reference_rows = df[df['id_start'] == reference_value]

    # Calculate the average distance for the reference value
    reference_average_distance = reference_rows['distance'].mean()

    # Calculate the threshold values (10% of the reference average distance)
    lower_threshold = reference_average_distance - 0.1 * reference_average_distance
    upper_threshold = reference_average_distance + 0.1 * reference_average_distance

    # Filter 'id_start' values within the threshold
    within_threshold_ids = df[(df['id_start'] != reference_value) & 
                              (df['distance'] >= lower_threshold) & 
                              (df['distance'] <= upper_threshold)]['id_start'].unique()

    # Sort the list of 'id_start' values
    within_threshold_ids.sort()

    return within_threshold_ids


    #question 4

def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Create columns for toll rates based on vehicle types
    df['moto'] = df['distance'] * 0.8
    df['car'] = df['distance'] * 1.2
    df['rv'] = df['distance'] * 1.5
    df['bus'] = df['distance'] * 2.2
    df['truck'] = df['distance'] * 3.6

    return df

    #question 5
   import pandas as pd
from datetime import time

def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Create columns for start and end times as datetime.time()
    df['start_time'] = pd.to_datetime(df['startTime']).dt.time
    df['end_time'] = pd.to_datetime(df['endTime']).dt.time

    # Create columns for start and end days as strings
    df['start_day'] = pd.to_datetime(df['startDay']).dt.day_name()
    df['end_day'] = pd.to_datetime(df['endDay']).dt.day_name()

    # Define time ranges and discount factors
    weekday_ranges = [(time(0, 0), time(10, 0)), (time(10, 0), time(18, 0)), (time(18, 0), time(23, 59, 59))]
    weekend_ranges = [(time(0, 0), time(23, 59, 59))]

    weekday_discounts = [0.8, 1.2, 0.8]
    weekend_discount = 0.7

    # Apply discount factors based on time ranges
    for i, (start_range, end_range) in enumerate(weekday_ranges):
        mask = ((df['start_time'] >= start_range) & (df['start_time'] <= end_range) &
                (df['end_time'] >= start_range) & (df['end_time'] <= end_range) &
                (df['start_day'].isin(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])))
        df.loc[mask, df.columns[7:]] *= weekday_discounts[i]

    for start_range, end_range in weekend_ranges:
        mask = ((df['start_time'] >= start_range) & (df['start_time'] <= end_range) &
                (df['end_time'] >= start_range) & (df['end_time'] <= end_range) &
                (df['start_day'].isin(['Saturday', 'Sunday'])))
        df.loc[mask, df.columns[7:]] *= weekend_discount

    return df
